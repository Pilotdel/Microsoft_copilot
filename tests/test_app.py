"""Tests for the Mergington High School API"""
import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_activities_success(self, client, reset_activities):
        """Test that activities are returned successfully"""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        
        # Check that activities are returned
        assert isinstance(data, dict)
        assert len(data) == 9
        
        # Check that specific activities exist
        assert "Chess Club" in data
        assert "Programming Class" in data
        
    def test_get_activities_structure(self, client, reset_activities):
        """Test that activity structure is correct"""
        response = client.get("/activities")
        data = response.json()
        
        activity = data["Chess Club"]
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        
    def test_get_activities_has_participants(self, client, reset_activities):
        """Test that activities have expected participants"""
        response = client.get("/activities")
        data = response.json()
        
        chess_club = data["Chess Club"]
        assert len(chess_club["participants"]) == 2
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_success(self, client, reset_activities):
        """Test successful signup for an activity"""
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "Signed up" in data["message"]
        assert "newstudent@mergington.edu" in data["message"]
        
        # Verify the participant was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]

    def test_signup_to_nonexistent_activity(self, client, reset_activities):
        """Test signup fails for non-existent activity"""
        response = client.post(
            "/activities/Nonexistent Club/signup",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_duplicate_email(self, client, reset_activities):
        """Test that duplicate signups are rejected"""
        # First signup should succeed
        response1 = client.post(
            "/activities/Chess Club/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        assert response1.status_code == 200
        
        # Duplicate signup should fail
        response2 = client.post(
            "/activities/Chess Club/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        assert response2.status_code == 400
        assert "already signed up" in response2.json()["detail"]

    def test_signup_multiple_activities(self, client, reset_activities):
        """Test that a student can sign up for multiple activities"""
        email = "versatile_student@mergington.edu"
        
        # Sign up for Chess Club
        response1 = client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Sign up for Programming Class
        response2 = client.post(
            "/activities/Programming Class/signup",
            params={"email": email}
        )
        assert response2.status_code == 200
        
        # Verify both signups
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities["Chess Club"]["participants"]
        assert email in activities["Programming Class"]["participants"]


class TestRemoveParticipant:
    """Tests for DELETE /activities/{activity_name}/participants/{email} endpoint"""

    def test_remove_participant_success(self, client, reset_activities):
        """Test successful removal of a participant"""
        response = client.delete(
            "/activities/Chess Club/participants/michael@mergington.edu"
        )
        assert response.status_code == 200
        data = response.json()
        assert "Removed" in data["message"]
        assert "michael@mergington.edu" in data["message"]
        
        # Verify the participant was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]

    def test_remove_participant_from_nonexistent_activity(self, client, reset_activities):
        """Test removal fails for non-existent activity"""
        response = client.delete(
            "/activities/Nonexistent Club/participants/student@mergington.edu"
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_remove_nonexistent_participant(self, client, reset_activities):
        """Test removal fails for non-participant"""
        response = client.delete(
            "/activities/Chess Club/participants/nonexistent@mergington.edu"
        )
        assert response.status_code == 400
        assert "not a participant" in response.json()["detail"]

    def test_remove_multiple_participants(self, client, reset_activities):
        """Test removing multiple participants"""
        # Remove first participant
        response1 = client.delete(
            "/activities/Chess Club/participants/michael@mergington.edu"
        )
        assert response1.status_code == 200
        
        # Remove second participant
        response2 = client.delete(
            "/activities/Chess Club/participants/daniel@mergington.edu"
        )
        assert response2.status_code == 200
        
        # Verify all participants were removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert len(activities["Chess Club"]["participants"]) == 0


class TestIntegration:
    """Integration tests for the full workflow"""

    def test_signup_and_remove_workflow(self, client, reset_activities):
        """Test complete signup and removal workflow"""
        email = "workflow_test@mergington.edu"
        activity = "Chess Club"
        
        # Check initial participant count
        initial = client.get("/activities").json()
        initial_count = len(initial[activity]["participants"])
        
        # Sign up
        signup_response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert signup_response.status_code == 200
        
        # Verify signup
        after_signup = client.get("/activities").json()
        assert len(after_signup[activity]["participants"]) == initial_count + 1
        assert email in after_signup[activity]["participants"]
        
        # Remove participant
        remove_response = client.delete(
            f"/activities/{activity}/participants/{email}"
        )
        assert remove_response.status_code == 200
        
        # Verify removal
        after_removal = client.get("/activities").json()
        assert len(after_removal[activity]["participants"]) == initial_count
        assert email not in after_removal[activity]["participants"]
