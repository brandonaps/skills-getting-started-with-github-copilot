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
"Basketball Team": {
    "description": "Practice basketball skills and compete in school tournaments",
    "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
    "max_participants": 15,
    "participants": []
},
"Swimming Club": {
    "description": "Improve swimming technique and endurance",
    "schedule": "Wednesdays and Fridays, 4:00 PM - 5:30 PM",
    "max_participants": 20,
    "participants": []
},
"Art Club": {
    "description": "Explore drawing, painting, and other visual arts",
    "schedule": "Mondays, 3:30 PM - 5:00 PM",
    "max_participants": 15,
    "participants": []
},
"Drama Club": {
    "description": "Develop acting skills and perform stage productions",
    "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
    "max_participants": 20,
    "participants": []
},
"Debate Club": {
    "description": "Practice public speaking, argumentation, and critical thinking",
    "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
    "max_participants": 20,
    "participants": []
},
"Science Club": {
    "description": "Conduct experiments and explore scientific topics",
    "schedule": "Thursdays, 3:30 PM - 5:00 PM",
    "max_participants": 20,
    "participants": []
}
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")


    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/signup/{email}")
def unregister_from_activity(activity_name: str, email: str):
    """Remove a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]
    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Student is not signed up for this activity")

    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
