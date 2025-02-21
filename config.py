import os
from datetime import timedelta

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/mydatabase")
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hackathon-secret-key'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    SESSION_COOKIE_NAME = 'truth_detector_session'
    