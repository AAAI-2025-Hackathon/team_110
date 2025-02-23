from pymongo import MongoClient
from bson import ObjectId
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime

class MongoDBHandler:
    def __init__(self, uri: str, db_name: str):
        """Initialize MongoDB connection"""
        self.client = MongoClient(uri)  # Use the full URI
        self.db = self.client[db_name]
    
    def insert(self, collection: str, data: dict) -> str:
        """Insert a document into a collection and return its ID."""
        result = self.db[collection].insert_one(data)
        return str(result.inserted_id)
    
    def find_by_id(self, collection: str, obj_id: str) -> Optional[dict]:
        """Find a document by its ID."""
        return self.db[collection].find_one({"_id": ObjectId(obj_id)})
    
    def find_by_query(self, collection: str, query: dict) -> List[dict]:
        """Find documents matching a query."""
        return list(self.db[collection].find(query))
    
    def update(self, collection: str, obj_id: str, update_data: dict) -> bool:
        """Update a document by its ID."""
        result = self.db[collection].update_one({"_id": ObjectId(obj_id)}, {"$set": update_data})
        #print(result)
        return result.modified_count > 0
    
    def delete(self, collection: str, obj_id: str) -> bool:
        """Delete a document by its ID."""
        result = self.db[collection].delete_one({"_id": ObjectId(obj_id)})
        return result.deleted_count > 0

    def purge_database(self, collectionName):
        """Delete all documents from all collections in the database."""
        if  collectionName in self.db.list_collection_names():
            self.db[collectionName].delete_many({})

class Story:
    def __init__(self, db_handler: MongoDBHandler, real_summary: str, fake_summary: str,
                 explanation: str, num_occurances: int, num_success: int, tags: Dict[str, Any]):
        self.db_handler = db_handler
        self.real_summary = real_summary
        self.fake_summary = fake_summary
        self.explanation = explanation
        self.num_occurances = num_occurances
        self.num_success = num_success
        self.tags = tags
        self._id: Optional[str] = None

    def save(self):
        """Save or update the story in the database."""
        data = {
            "real_summary": self.real_summary,
            "fake_summary": self.fake_summary,
            "explanation": self.explanation,
            "num_occurances": self.num_occurances,
            "num_success": self.num_success,
            "tags": self.tags
        }
        if self._id:
            self.db_handler.update("stories_database", self._id, data)
        else:
            self._id = self.db_handler.insert("stories_database", data)

    @classmethod
    def get_by_id(cls, db_handler: MongoDBHandler, story_id: str):
        """Retrieve a story by its ID."""
        data = db_handler.find_by_id("stories_database", story_id)
        if data:
            story = cls(
                db_handler,
                real_summary=data["real_summary"],
                fake_summary=data["fake_summary"],
                explanation=data["explanation"],
                num_occurances=data["num_occurances"],
                num_success=data["num_success"],
                tags=data["tags"]
            )
            story._id = str(data["_id"])
            return story
        return None

    @classmethod
    def search(cls, db_handler: MongoDBHandler, query: Dict[str, Any]) -> List['Story']:
        """Retrieve stories matching a query."""
        data_list = db_handler.find_by_query("stories_database", query)
        stories = []
        for data in data_list:
            story = cls(
                db_handler,
                real_summary=data["real_summary"],
                fake_summary=data["fake_summary"],
                explanation=data["explanation"],
                num_occurances=data["num_occurances"],
                num_success=data["num_success"],
                tags=data["tags"]
            )
            story._id = str(data["_id"])
            stories.append(story)
        return stories


class Session:
    def __init__(self, db_handler: MongoDBHandler, session_id: str, email: str, metrics: Dict[str, Any], tags: Dict[str, Any]):
        self.db_handler = db_handler
        self.session_id = session_id
        self.email = email
        self.metrics = metrics
        self._id: Optional[str] = None
        self.tags = tags if len(tags) != 0 else dict()

    def save(self):
        """Save or update the session in the database."""
        data = {
            "session_id": self.session_id,
            "email": self.email,
            "metrics": self.metrics,
            "tags": self.tags
        }
        if self._id:
            self.db_handler.update("session_db", self._id, data)
        else:
            self._id = self.db_handler.insert("session_db", data)

    @classmethod
    def get_by_id(cls, db_handler: MongoDBHandler, session_id: str):
        """Retrieve a session by its ID."""
        data = db_handler.find_by_id("session_db", session_id)
        if data:
            session = cls(
                db_handler,
                session_id=data["session_id"],
                email=data["email"],
                metrics=data["metrics"],
                tags=data["tags"]
            )
            session._id = str(data["_id"])
            return session
        return None

    @classmethod
    def search(cls, db_handler: MongoDBHandler, query: Dict[str, Any]) -> List['Session']:
        """Retrieve sessions matching a query."""
        data_list = db_handler.find_by_query("session_db", query)
        sessions = []
        for data in data_list:
            session = cls(
                db_handler,
                session_id=data["session_id"],
                email=data["email"],
                metrics=data["metrics"],
                tags=data.get("tags", dict())
            )
            session._id = str(data["_id"])
            sessions.append(session)
        return sessions
    
    @classmethod
    def create_from_user(cls, db_handler: MongoDBHandler, email: Optional[str] = None, save: Optional[bool] = False) -> 'Session':
        """Create a new Session object from user details."""
        session_data = {
            'session_id': str(uuid.uuid4()),
            'email': email,
            'created_at': datetime.now().isoformat(),
            'metrics': {
                'score': 0,
                'correct': 0,
                'incorrect': 0,
                'avg_response_time': 0,
                'history': [],
                'tags': dict()
            }
        }
        session = cls(db_handler, session_id=session_data['session_id'], email=session_data['email'], metrics=session_data['metrics'])
        if save:
            session.save()
        return session
    
    def isGuest(self):
        return self.email == None or self.email == ""     
