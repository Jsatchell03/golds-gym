from google.cloud import firestore
import os
from dotenv import load_dotenv
import random

load_dotenv()

first_names = [
    "James",
    "Mary",
    "John",
    "Patricia",
    "Robert",
    "Jennifer",
    "Michael",
    "Linda",
    "William",
    "Elizabeth",
    "David",
    "Barbara",
    "Richard",
    "Susan",
    "Joseph",
    "Jessica",
    "Thomas",
    "Sarah",
    "Charles",
    "Karen",
    "Christopher",
    "Nancy",
    "Daniel",
    "Lisa",
    "Matthew",
    "Betty",
    "Anthony",
    "Margaret",
    "Mark",
    "Sandra",
    "Donald",
    "Ashley",
    "Steven",
    "Kimberly",
    "Paul",
    "Emily",
    "Andrew",
    "Donna",
    "Joshua",
    "Michelle",
    "Kenneth",
    "Dorothy",
    "Kevin",
    "Carol",
    "Brian",
    "Amanda",
    "George",
    "Melissa",
    "Jean-Luc",
    "Mary-Anne",
]
last_names = [
    "Smith",
    "Johnson",
    "Williams",
    "Brown",
    "Jones",
    "Garcia",
    "Miller",
    "Davis",
    "Rodriguez",
    "Martinez",
    "Hernandez",
    "Lopez",
    "Gonzalez",
    "Wilson",
    "Anderson",
    "Thomas",
    "Taylor",
    "Moore",
    "Jackson",
    "Martin",
    "Lee",
    "Perez",
    "Thompson",
    "White",
    "Harris",
    "Sanchez",
    "Clark",
    "Ramirez",
    "Lewis",
    "Robinson",
    "Walker",
    "Young",
    "Allen",
    "King",
    "Wright",
    "Scott",
    "Torres",
    "Nguyen",
    "Hill",
    "Flores",
    "Green",
    "Adams",
    "Nelson",
    "Baker",
    "Hall",
    "Rivera",
    "Campbell",
]
machines = [
    "Treadmill",
    "Elliptical",
    "Stationary Bike",
    "Rowing Machine",
    "Stair Climber",
    "Leg Press",
    "Chest Press",
    "Lat Pulldown",
    "Seated Row",
    "Shoulder Press",
    "Cable Crossover",
    "Smith Machine",
    "Hack Squat",
    "Leg Extension",
    "Leg Curl",
    "Hip Abductor",
    "Hip Adductor",
    "Glute Kickback",
    "Calf Raise",
    "Pec Deck",
    "Assisted Pull-Up",
    "Back Extension",
    "Ab Crunch",
    "Rotary Torso",
    "Functional Trainer",
    "Chest Fly",
    "Dip Assist",
    "Preacher Curl",
    "Belt Squat",
    "Sled Push",
]
amenities = [
    "Locker Rooms",
    "Showers",
    "Sauna",
    "Swimming Pool",
    "Hot Tub",
    "Towel Service",
    "Shake Bar",
    "Free Wi-Fi",
    "Basketball Court",
    "Ice Tub",
    "Massage Therapy",
    "Rock Wall",
]
weekdays = [
    "sunday",
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
]

PROJECT_ID = os.getenv("PROJECT_ID", "Not Working")
db = firestore.Client(project=PROJECT_ID)
members = db.collection("members")
locations = db.collection("locations")


def random_phone_number():
    area_code = str(random.randint(200, 999))
    central_office = str(random.randint(200, 999))
    line_number = str(random.randint(1000, 9999))
    return area_code + central_office + line_number


def random_email(first_name, last_name):
    domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com"]
    splits = [".", "-", "_", "", "__"]
    if random.randint(1, 10) > 5:
        start = first_name
        end = last_name
    else:
        start = last_name
        end = first_name
    format = random.randint(1, 3)
    return f"{start[0] if format == 1 else start}{splits[random.randint(0, len(splits) -1)]}{end[0] if format == 2 else end}@{domains[random.randint(0, len(domains) - 1)]}"


def random_classes():
    class_names = [
        "Zumba",
        "Spin",
        "Pilates",
        "Yoga",
        "Mobility",
        "Weight Training",
        "Calisthenics",
        "Postnatal Fitness",
        "Kickboxing",
        "Boxing",
        "CrossFit",
        "Bootcamp",
        "HIIT",
    ]
    classes = []
    for class_name in random.sample(class_names, random.randint(0, len(class_names))):
        start_time = random.randint(6, 19) * 100
        end_time = start_time + random.randint(1, 2) * 100
        days = random.sample(weekdays, random.randint(1, 3))
        classes.append(
            {
                "name": class_name,
                "days": days,
                "start_time": start_time,
                "end_time": end_time,
                "spots": random.randint(1, 5) * 5,
            }
        )

    return classes


def random_address():
    locations = [
        # USA
        {"city": "New York", "region": "NY", "country": "USA"},
        {"city": "Los Angeles", "region": "CA", "country": "USA"},
        {"city": "Chicago", "region": "IL", "country": "USA"},
        # Canada
        {"city": "Toronto", "region": "ON", "country": "Canada"},
        {"city": "Vancouver", "region": "BC", "country": "Canada"},
        # UK
        {"city": "London", "region": "ENG", "country": "UK"},
        {"city": "Manchester", "region": "ENG", "country": "UK"},
        # Australia
        {"city": "Sydney", "region": "NSW", "country": "Australia"},
        {"city": "Melbourne", "region": "VIC", "country": "Australia"},
        # Germany
        {"city": "Berlin", "region": "BE", "country": "Germany"},
        {"city": "Munich", "region": "BY", "country": "Germany"},
    ]

    street_names = [
        "Main St",
        "High St",
        "King St",
        "Queen St",
        "Park Ave",
        "Station Rd",
        "Church St",
        "George St",
        "Market St",
        "Broadway",
        "Victoria Rd",
        "Elizabeth St",
        "1st Ave",
        "41st St",
    ]

    loc = random.choice(locations)

    address = {
        "building_number": str(random.randint(1, 9999)),
        "street_name": random.choice(street_names),
        "city": loc["city"],
        "region": loc["region"],
        "country": loc["country"],
    }

    return address


def batch_write(func):
    def wrap(count):

        while count > 0:
            if count > 500:
                func(500)
                count -= 500
            else:
                func(count)
                count -= count

    return wrap


@batch_write
def add_sample_member_docs(count):
    batch = db.batch()
    for _ in range(count):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        email = random_email(first_name, last_name)
        batch.set(
            members.document(),
            {
                "first_name": first_name,
                "last_name": last_name,
                "phone_number": random_phone_number(),
                "email": email,
                "member_since": firestore.SERVER_TIMESTAMP,
                "membership_status": (
                    "active" if random.randint(0, 9) > 3 else "inactive"
                ),
            },
        )
    batch.commit()


@batch_write
def add_sample_location_docs(count):
    batch = db.batch()
    for _ in range(count):
        batch.set(
            locations.document(),
            {
                "address": random_address(),
                "phone_number": random_phone_number(),
                "machines": random.sample(machines, random.randint(5, len(machines))),
                "amenities": random.sample(
                    amenities, random.randint(1, len(amenities))
                ),
                "hours": (
                    {}
                    if random.randint(0, 2) == 0
                    else {
                        "sunday": {"open_time": 400, "close_time": 2200},
                        "monday": {"open_time": 400, "close_time": 2200},
                        "tuesday": {"open_time": 400, "close_time": 2200},
                        "wednesday": {"open_time": 400, "close_time": 2200},
                        "thursday": {"open_time": 400, "close_time": 2200},
                        "friday": {"open_time": 400, "close_time": 2200},
                        "saturday": {"open_time": 400, "close_time": 2200},
                    }
                ),
                "classes": random_classes(),
            },
        )
    batch.commit()


add_sample_location_docs(25)
