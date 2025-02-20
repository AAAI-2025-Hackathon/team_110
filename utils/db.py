from pymongo import MongoClient, ReturnDocument
import os
from datetime import datetime
from bson.objectid import ObjectId

# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "news_game"

CATEGORIES = {
    1: "Politics",
    2: "Technology",
    3: "Science",
    4: "Health",
    5: "Finance",
    6: "Sports",
    7: "Entertainment"
}

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections
sessions_collection = db["sessions"]
stories_collection = db["stories"]


def init_db():
    """
    Initialize the database with any required indexes, default data, or other setup.
    """
    # Example: create an index on session_id since we query by it frequently
    sessions_collection.create_index("session_id", unique=True)
    
    # Example: if stories have a unique 'slug' or 'id' field, you could index that.
    # stories_collection.create_index("id", unique=True)
    
    # Optionally, insert any default data if needed
    # e.g. stories_collection.insert_one({...})

    print("Database initialized (indexes created, etc.)")


def format_session_data(session_id, email=None, existing_data=None):
    """
    Ensure session data follows our schema. 
    If we have existing data (from the DB), start with that and update fields.
    Otherwise, create a new session dictionary.
    """
    if existing_data is None:
        # Create new if not found
        existing_data = {
            "session_id": session_id,
            "email": email if email else "",
            "created_at": datetime.utcnow(),
            "metrics": {
                "score": 0,
                "correct": 0,
                "incorrect": 0,
                "avg_response_time": 0,
                "history": []
            }
        }
    else:
        # If we have existing data, we ensure required fields exist
        existing_data.setdefault("session_id", session_id)
        existing_data.setdefault("email", email if email else existing_data.get("email", ""))
        existing_data.setdefault("created_at", datetime.utcnow())
        existing_data.setdefault("metrics", {})
        existing_data["metrics"].setdefault("score", 0)
        existing_data["metrics"].setdefault("correct", 0)
        existing_data["metrics"].setdefault("incorrect", 0)
        existing_data["metrics"].setdefault("avg_response_time", 0)
        existing_data["metrics"].setdefault("history", [])

    return existing_data


def format_story_data(story_data):
    """
    Ensure story data follows our desired schema, 
    setting defaults where fields are missing.
    """
    formatted = story_data.copy()

    # Default text fields
    formatted["fake_summary"] = story_data.get("fake_summary", "")
    formatted["real_summary"] = story_data.get("real_summary", "")
    formatted["explanation"] = story_data.get("explanation", "")

    # Default numeric fields
    formatted["numberOfAppearences"] = story_data.get("numberOfAppearences", 0)
    formatted["numberOfTimesTrciked"] = story_data.get("numberOfTimesTrciked", 0)

    # New: Default category types as an empty list
    formatted["type"] = story_data.get("type", [])  # Ensure it's a list

    return formatted



def save_session(session_id, email=None, session_data=None):
    """
    Save or update a session in MongoDB. 
    If a session with this session_id exists, update. Otherwise, insert a new one.
    """
    existing = sessions_collection.find_one({"session_id": session_id})
    if existing:
        # Format the new data on top of existing data
        updated_data = format_session_data(session_id, email, existing_data=existing)
        # If we passed in session_data, update the fields
        if session_data and isinstance(session_data, dict):
            updated_data["metrics"].update(session_data.get("metrics", {}))
        result = sessions_collection.find_one_and_replace(
            {"session_id": session_id},
            updated_data,
            return_document=ReturnDocument.AFTER
        )
        return result
    else:
        # Insert new document
        new_data = format_session_data(session_id, email, existing_data=None)
        if session_data and isinstance(session_data, dict):
            new_data["metrics"].update(session_data.get("metrics", {}))
        sessions_collection.insert_one(new_data)
        return new_data


def get_session(session_id):
    """
    Retrieve a session from MongoDB by session_id.
    """
    return sessions_collection.find_one({"session_id": session_id})


def save_story(story_data):
    """
    Save a story to MongoDB (insert only).
    If you'd like to allow upsert by a unique key, you can modify accordingly.
    """
    formatted = format_story_data(story_data)
    return stories_collection.insert_one(formatted).inserted_id


def get_story_by_objectid(_id):
    """
    Retrieve a specific story from MongoDB by _id (ObjectId).
    """
    if not isinstance(_id, ObjectId):
        # If _id comes in as a string, convert
        _id = ObjectId(_id)
    return stories_collection.find_one({"_id": _id})


def get_story_by_custom_id(story_id):
    """
    If your stories have a unique 'id' field (not the ObjectId),
    retrieve that story here. 
    """
    return stories_collection.find_one({"id": story_id})


def get_random_story():
    """
    Retrieve a random story from MongoDB.
    """
    return stories_collection.aggregate([{"$sample": {"size": 1}}]).next()


def purge_sessions():
    """
    Remove all session data (for debugging).
    """
    result = sessions_collection.delete_many({})
    print(f"Deleted {result.deleted_count} session documents.")


def purge_stories():
    """
    Remove all stored stories (for debugging).
    """
    result = stories_collection.delete_many({})
    print(f"Deleted {result.deleted_count} story documents.")


def purge_db():
    """
    Purge entire DB (both sessions and stories). For debugging or dev convenience.
    """
    purge_sessions()
    purge_stories()
    print("All collections purged.")

def format_story_data(story_data):
    """
    Ensure story data follows our desired schema, 
    setting defaults where fields are missing.
    """
    # Copy to avoid mutating the original
    formatted = story_data.copy()

    # Default text fields
    formatted["fake_summary"] = story_data.get("fake_summary", "")
    formatted["real_summary"] = story_data.get("real_summary", "")
    formatted["explanation"] = story_data.get("explanation", "")

    # Default numeric fields
    formatted["numberOfAppearences"] = story_data.get("numberOfAppearences", 0)
    formatted["numberOfTimesTrciked"] = story_data.get("numberOfTimesTrciked", 0)

    return formatted

def bulk_save_stories(stories_list):
    """
    Accepts a list of story dicts, formats them, 
    and inserts them into the 'stories' collection.
    """
    # Format each story using the helper
    formatted_stories = [format_story_data(story) for story in stories_list]
    
    # Insert them all at once
    result = stories_collection.insert_many(formatted_stories)
    return result.inserted_ids
