"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and play basketball with the school team",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging problems and participate in math competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "henry@mergington.edu"]
    }
}

# In-memory timetable data for academic schedule integration
timetables = {
    "Monday": [
        {"period": "8:00 AM - 9:00 AM", "subject": "English"},
        {"period": "9:15 AM - 10:15 AM", "subject": "Mathematics"},
        {"period": "10:30 AM - 11:30 AM", "subject": "Biology"},
        {"period": "11:45 AM - 12:45 PM", "subject": "History"},
        {"period": "1:30 PM - 2:30 PM", "subject": "Physical Education"}
    ],
    "Tuesday": [
        {"period": "8:00 AM - 9:00 AM", "subject": "Chemistry"},
        {"period": "9:15 AM - 10:15 AM", "subject": "Mathematics"},
        {"period": "10:30 AM - 11:30 AM", "subject": "Study Skills"},
        {"period": "11:45 AM - 12:45 PM", "subject": "Art"},
        {"period": "1:30 PM - 2:30 PM", "subject": "Computer Science"}
    ],
    "Wednesday": [
        {"period": "8:00 AM - 9:00 AM", "subject": "Physics"},
        {"period": "9:15 AM - 10:15 AM", "subject": "Mathematics"},
        {"period": "10:30 AM - 11:30 AM", "subject": "Language Arts"},
        {"period": "11:45 AM - 12:45 PM", "subject": "Geography"},
        {"period": "1:30 PM - 2:30 PM", "subject": "Music"}
    ],
    "Thursday": [
        {"period": "8:00 AM - 9:00 AM", "subject": "Biology"},
        {"period": "9:15 AM - 10:15 AM", "subject": "Mathematics"},
        {"period": "10:30 AM - 11:30 AM", "subject": "Art"},
        {"period": "11:45 AM - 12:45 PM", "subject": "Computer Science"},
        {"period": "1:30 PM - 2:30 PM", "subject": "Health"}
    ],
    "Friday": [
        {"period": "8:00 AM - 9:00 AM", "subject": "English"},
        {"period": "9:15 AM - 10:15 AM", "subject": "Mathematics"},
        {"period": "10:30 AM - 11:30 AM", "subject": "Chemistry"},
        {"period": "11:45 AM - 12:45 PM", "subject": "Drama"},
        {"period": "1:30 PM - 2:30 PM", "subject": "Physical Education"}
    ]
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.get("/timetable")
def get_timetable():
    return timetables


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is signed up
    if email not in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    # Remove student
    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
