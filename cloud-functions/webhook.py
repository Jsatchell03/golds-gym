import functions_framework
from flask import jsonify

PROJECT_ID = "golds-gym-492816"
AGENT_ID = "5722b372-1354-49f1-8704-bb991c25a041"
LOCATION = "global"
FLOW_IDS = {"activate_membership": "bd5fe207-7700-4a1b-88cc-d728ef66e2c4"}
PAGE_IDS = {"collect_user_information": "8a482c09-e929-470e-b519-2447d00dff5c"}


@functions_framework.http
def cx_webhook(request):
    """Dialogflow CX Webhook Entry Point."""
    req = request.get_json(silent=True, force=True)

    # Extract the webhook tag
    tag = req.get("fulfillmentInfo", {}).get("tag", "")

    # Route to handler based on tag
    if tag == "activate_membership":
        return activate_membership(req)
    elif tag == "deactivate_membership":
        return deactivate_membership(req)
    elif tag == "authenticate":
        return handle_authenticate(req)
    elif tag == "update_member_details":
        return update_member_details(req)
    else:
        return handle_default(req)


def activate_membership(req):
    """Reactivate existing user's membership and create new user memberships."""
    # Extract session parameters
    session_params = req.get("sessionInfo", {}).get("parameters", {})
    email = session_params.get("email", None)
    phone_number = session_params.get("phone_number", None)
    full_name = session_params.get("full_name", None)
    if not email or not phone_number or not full_name:
        response = {
            "fulfillmentResponse": {
                "messages": [
                    {
                        "text": {
                            "text": [
                                "I wasn't able to activate your membership with the information you gave me. Confirm your information and please try again."
                            ]
                        }
                    }
                ]
            },
            "targetPage": f"projects/{PROJECT_ID}/locations/{LOCATION}/agents/{AGENT_ID}/flows/{FLOW_IDS["activate_membership"]}/pages/{PAGE_IDS["collect_user_information"]}",
        }

    # Business logic (simulate DB lookup)
    balance = lookup_balance(account_number)

    # Build response
    response = {
        "fulfillmentResponse": {
            "messages": [
                {
                    "text": {
                        "text": [
                            f"{customer_name}, your balance for account {account_number} is ${balance:.2f}."
                        ]
                    }
                }
            ]
        },
        "sessionInfo": {"parameters": {"membership_activated": "true"}},
    }
    return jsonify(response)


def lookup_balance(account_number):
    """Simulate database lookup."""
    balances = {12345: 245.50, 67890: 1024.00, 11111: 0.00}
    return balances.get(int(account_number), 0.00)


def handle_make_payment(req):
    session_params = req.get("sessionInfo", {}).get("parameters", {})
    amount = session_params.get("payment_amount", 0)
    return jsonify(
        {
            "fulfillmentResponse": {
                "messages": [
                    {
                        "text": {
                            "text": [f"Payment of ${amount} processed successfully!"]
                        }
                    }
                ]
            },
            "sessionInfo": {
                "parameters": {"payment_status": "completed", "payment_amount": amount}
            },
        }
    )


def handle_authenticate(req):
    intent_params = req.get("intentInfo", {}).get("parameters", {})
    account = intent_params.get("account_number", {}).get("resolvedValue", "")
    # Simulate auth
    authenticated = account in [12345, 67890, 11111]
    return jsonify(
        {
            "fulfillmentResponse": {
                "messages": [
                    {
                        "text": {
                            "text": [
                                (
                                    "Authentication successful!"
                                    if authenticated
                                    else "Account not found."
                                )
                            ]
                        }
                    }
                ]
            },
            "sessionInfo": {
                "parameters": {
                    "authenticated": authenticated,
                    "customer_name": "Alice" if authenticated else None,
                }
            },
        }
    )


def handle_default(req):
    tag = req.get("fulfillmentInfo", {}).get("tag", "unknown")
    return jsonify(
        {
            "fulfillmentResponse": {
                "messages": [
                    {
                        "text": {
                            "text": [
                                f"Webhook received tag: {tag}, but no handler found."
                            ]
                        }
                    }
                ]
            }
        }
    )
