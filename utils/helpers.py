import uuid
from datetime import datetime

def generate_session_id():
    return str(uuid.uuid4())

def create_user_session(email=None):
    return {
        'session_id': generate_session_id(),
        'email': email,
        'created_at': datetime.now().isoformat(),
        'metrics': {
            'score': 0,
            'correct': 0,
            'incorrect': 0,
            'avg_response_time': 0,
            'history': []
        }
    }