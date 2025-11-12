"""Pytest configuration and fixtures"""
import sys
from pathlib import Path

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from fastapi.testclient import TestClient
from app import app, activities


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to initial state before each test"""
    initial_activities = {
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
            "description": "Competitive soccer team training and matches",
            "schedule": "Practice: Tuesdays and Thursdays, 4:00 PM - 6:00 PM; Games on weekends",
            "max_participants": 22,
            "participants": ["noah@mergington.edu", "liam@mergington.edu"]
        },
        "Basketball Club": {
            "description": "Pickup games, skill development, and intramural tournaments",
            "schedule": "Wednesdays and Fridays, 4:15 PM - 6:00 PM",
            "max_participants": 15,
            "participants": ["ava@mergington.edu", "isabella@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore drawing, painting, and mixed media projects",
            "schedule": "Mondays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["charlotte@mergington.edu", "amelia@mergington.edu"]
        },
        "Drama Club": {
            "description": "Acting workshops, rehearsals, and school productions",
            "schedule": "Thursdays, 4:00 PM - 6:30 PM",
            "max_participants": 25,
            "participants": ["elijah@mergington.edu", "mia@mergington.edu"]
        },
        "Debate Team": {
            "description": "Prepare for competitive debates and public speaking events",
            "schedule": "Tuesdays, 5:00 PM - 6:30 PM",
            "max_participants": 16,
            "participants": ["logan@mergington.edu", "grace@mergington.edu"]
        },
        "Science Club": {
            "description": "Hands-on experiments, science fairs, and research projects",
            "schedule": "Fridays, 3:45 PM - 5:15 PM",
            "max_participants": 20,
            "participants": ["jackson@mergington.edu", "zoe@mergington.edu"]
        }
    }
    
    # Clear and reset activities
    activities.clear()
    activities.update(initial_activities)
    yield activities
    # Cleanup after test
    activities.clear()
    activities.update(initial_activities)
