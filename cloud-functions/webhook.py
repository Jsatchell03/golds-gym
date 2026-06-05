import functions_framework
from flask import jsonify
from google.cloud import firestore
import re
import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
db = firestore.Client(project=PROJECT_ID) if PROJECT_ID else firestore.Client()


# ---------------------------
# Entry Point
# ---------------------------
@functions_framework.http
def cx_webhook(request):
    req = request.get_json(silent=True, force=True)
    tag = req.get("fulfillmentInfo", {}).get("tag", "")

    if tag == "authenticate":
        return handle_authenticate(req)
    elif tag == "activate_membership":
        return handle_activate_membership(req)
    elif tag == "deactivate_membership":
        return handle_deactivate_membership(req)
    else:
        return handle_default(req)


# ---------------------------
# Helpers
# ---------------------------
def normalize_email(email):
    return email.strip().lower() if email else ""


def normalize_phone(phone):
    return re.sub(r"\D", "", phone) if phone else ""


def find_member(email, phone):
    members = db.collection("members")
    query = (
        members.where("email", "==", email).where("phone_number", "==", phone).limit(1)
    )
    docs = list(query.stream())
    return docs[0] if docs else None


def simple_response(text):
    return {"fulfillmentResponse": {"messages": [{"text": {"text": [text]}}]}}


# ---------------------------
# Handlers
# ---------------------------
def handle_authenticate(req):
    session_params = req.get("sessionInfo", {}).get("parameters", {})

    email = normalize_email(session_params.get("email", ""))
    phone = normalize_phone(session_params.get("phone_number", ""))

    if not email or not phone:
        return jsonify(simple_response("Email and phone number are required."))

    member_doc = find_member(email, phone)

    if member_doc:
        member_data = member_doc.to_dict()

        message = f"Welcome back, {member_data.get('first_name', '')}!"

        session_update = {
            "is_authenticated": True,
            "member_id": member_doc.id,
            "email": member_data.get("email"),
            "phone_number": member_data.get("phone_number"),
            "first_name": member_data.get("first_name"),
            "last_name": member_data.get("last_name"),
            "membership_status": member_data.get("membership_status"),
            "member_since": str(member_data.get("member_since")),
        }
    else:
        message = "No matching account found. Please check your email and phone number."
        session_update = {"is_authenticated": False}

    return jsonify(
        {
            "fulfillmentResponse": {"messages": [{"text": {"text": [message]}}]},
            "sessionInfo": {"parameters": session_update},
        }
    )


def handle_activate_membership(req):
    session_params = req.get("sessionInfo", {}).get("parameters", {})

    first_name = session_params.get("first_name", "")
    last_name = session_params.get("last_name", "")
    email = normalize_email(session_params.get("email", ""))
    phone = normalize_phone(session_params.get("phone_number", ""))

    if not email or not phone:
        return jsonify(simple_response("Email and phone number are required."))

    member_doc = find_member(email, phone)

    if member_doc:
        # Existing member → update
        member_ref = member_doc.reference
        member_ref.update(
            {
                "membership_status": "active",
                "first_name": first_name,
                "last_name": last_name,
            }
        )

        updated_doc = member_ref.get()
        member_data = updated_doc.to_dict()

        message = f"Welcome back {member_data.get('first_name', '')}, your membership is now active."

    else:
        # New member → create (deterministic ID prevents duplicates)
        doc_id = f"{email}_{phone}"
        member_ref = db.collection("members").document(doc_id)

        new_member = {
            "email": email,
            "phone_number": phone,
            "first_name": first_name,
            "last_name": last_name,
            "member_since": firestore.SERVER_TIMESTAMP,
            "membership_status": "active",
        }

        member_ref.set(new_member)

        created_doc = member_ref.get()
        member_data = created_doc.to_dict()

        message = (
            f"Welcome {first_name}, your membership has been created and activated!"
        )

    session_update = {
        "is_authenticated": True,
        "member_id": member_ref.id,
        "email": member_data.get("email"),
        "phone_number": member_data.get("phone_number"),
        "first_name": member_data.get("first_name"),
        "last_name": member_data.get("last_name"),
        "membership_status": member_data.get("membership_status"),
        "member_since": str(member_data.get("member_since")),
    }

    return jsonify(
        {
            "fulfillmentResponse": {"messages": [{"text": {"text": [message]}}]},
            "sessionInfo": {"parameters": session_update},
        }
    )


def handle_deactivate_membership(req):
    session_params = req.get("sessionInfo", {}).get("parameters", {})

    if not session_params.get("is_authenticated"):
        return jsonify(
            simple_response("You must log in before deactivating your membership.")
        )

    member_id = session_params.get("member_id")

    if not member_id:
        return jsonify(simple_response("Session expired. Please log in again."))

    member_ref = db.collection("members").document(member_id)
    member_ref.update({"membership_status": "inactive"})

    updated_doc = member_ref.get()
    member_data = updated_doc.to_dict()

    return jsonify(
        {
            "fulfillmentResponse": {
                "messages": [
                    {"text": {"text": ["Your membership has been deactivated."]}}
                ]
            },
            "sessionInfo": {
                "parameters": {
                    "membership_status": member_data.get("membership_status")
                }
            },
        }
    )


def handle_default(req):
    tag = req.get("fulfillmentInfo", {}).get("tag", "unknown")
    return jsonify(simple_response(f"No handler found for tag: {tag}"))
