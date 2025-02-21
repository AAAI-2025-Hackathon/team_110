## This script initializes the stories DB with some generated responses from a fine tuned GPT 4 model.

from db import *
from tqdm import tqdm
from mock_db import MOCK_RESPONSES


if __name__ == "__main__":
    db_handler = MongoDBHandler("mongo_news")
    
    for story in tqdm(MOCK_RESPONSES):
        try:
            new_story = {
                "real_summary": story["real_summary"],
                "fake_summary": story["fake_summary"],
                "explanation": story["explanation"],
                "num_occurances": 0,
                "num_success": 0,
                "tags": {}
            }
            story_id = db_handler.insert("stories_database", new_story)
        except:
            print("[WARN] Skipping a mock write: ", new_story)