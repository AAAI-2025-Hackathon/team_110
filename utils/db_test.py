from db import *

# Usage Example
if __name__ == "__main__":
    db = MongoDBHandler("mongo_news")
    
    # Create and save a story
    story = Story(db, "Real Summary Example", "Fake Summary Example", "Explanation Example", 10, 5, {"category": "fiction"})
    story.save()
    
    # Retrieve a story by ID
    retrieved_story = Story.get_by_id(db, story._id)
    print(retrieved_story.real_summary if retrieved_story else "Story not found")
    
    # Search stories by tag
    matching_stories = Story.search(db, {"tags.category": "fiction"})
    print([s.real_summary for s in matching_stories])
    
    # Create and save a session
    session = Session(db, "session_123", "user@example.com", {"score": 100, "correct": 5, "incorrect": 2, "avg_response_time": 3.2, "history": [], "tags": {}})
    session.save()
    
    # Retrieve a session
    retrieved_session = Session.get_by_id(db, session._id)
    print(retrieved_session.email if retrieved_session else "Session not found")

    db.purge_database("stories_database")
    db.purge_database("session_db")