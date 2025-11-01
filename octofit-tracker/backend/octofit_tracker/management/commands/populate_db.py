from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models
from pymongo import MongoClient

# Sample data for users, teams, activities, leaderboard, and workouts
USERS = [
    {"username": "ironman", "email": "ironman@marvel.com", "team": "marvel"},
    {"username": "captainamerica", "email": "cap@marvel.com", "team": "marvel"},
    {"username": "spiderman", "email": "spiderman@marvel.com", "team": "marvel"},
    {"username": "superman", "email": "superman@dc.com", "team": "dc"},
    {"username": "batman", "email": "batman@dc.com", "team": "dc"},
    {"username": "wonderwoman", "email": "wonderwoman@dc.com", "team": "dc"},
]

TEAMS = [
    {"name": "marvel", "members": ["ironman", "captainamerica", "spiderman"]},
    {"name": "dc", "members": ["superman", "batman", "wonderwoman"]},
]

ACTIVITIES = [
    {"user": "ironman", "activity": "run", "distance": 5},
    {"user": "superman", "activity": "fly", "distance": 100},
    {"user": "batman", "activity": "cycle", "distance": 20},
]

LEADERBOARD = [
    {"user": "superman", "score": 1000},
    {"user": "ironman", "score": 800},
    {"user": "batman", "score": 700},
]

WORKOUTS = [
    {"name": "Morning Cardio", "type": "cardio", "duration": 30},
    {"name": "Strength Training", "type": "strength", "duration": 45},
]

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Insert data
        db.users.insert_many(USERS)
        db.teams.insert_many(TEAMS)
        db.activities.insert_many(ACTIVITIES)
        db.leaderboard.insert_many(LEADERBOARD)
        db.workouts.insert_many(WORKOUTS)

        # Create unique index on email for users
        db.users.create_index([("email", 1)], unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
