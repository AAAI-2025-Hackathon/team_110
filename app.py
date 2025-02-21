from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for
from config import Config
from utils.helpers import create_user_session, make_serializable
from utils.db import MongoDBHandler, Story, Session
from backend.gpt import generate_summaries, MISINFO_CAT, TOPIC_CAT
import random, time, os, json
from apscheduler.schedulers.background import BackgroundScheduler
from urllib.parse import urlparse

## Add the ability to automatically store those reponses that fooled the humans.
## Add event listener in GPT code to auto retrain after it reaches 50 or so new responses. ### Very important. 
## Also, we have data regarding every users category that they were weak at so focus more on that. 

## Initialize the flask app
app = Flask(__name__)
app.config.from_object(Config)

## Initialize the Mongo DB handler
#### ENV variable looks like mongodb://localhost:27017/mydatabase
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/mydatabase")
parsed_uri = urlparse(MONGO_URI)
mongo_host = parsed_uri.hostname  # Extracts hostname or IP
mongo_port = parsed_uri.port      # Extracts port
mongo_database = parsed_uri.path.strip("/")  # Extracts database name
print("[INFO] MONGODB URI:", MONGO_URI)
#db_handler = MongoDBHandler("mongo_news", mongo_host, mongo_port)
db_handler = MongoDBHandler(MONGO_URI, "mongo_news")

## Home page
@app.route('/')
def home():
    return render_template('login.html')

## Lost or missing session ID
@app.route('/login/email', methods=['GET'])
def login_missing_email():
    session_id = request.cookies.get(app.config['SESSION_COOKIE_NAME'])
    #print(session_id)
    existing_session = Session.search(db_handler, {"session_id": session_id})
    #print(existing_session)
    
    if len(existing_session) > 0:
        user_session = existing_session[0]
        template = "singleCard.html" if random.random() < 0.5 else "doubleCard.html"
        resp = make_response(render_template(template))
        resp.set_cookie(
            app.config['SESSION_COOKIE_NAME'],
            user_session.session_id,
            max_age=app.config['PERMANENT_SESSION_LIFETIME'].seconds
        )
        return resp
    else:
        print("[INFO] User has no coockie go back to login") 
        return render_template('login.html')

## Login via EMAIL, works across systems.
@app.route('/login/email', methods=['POST'])
def login_email():
    email = request.form.get('email')
    existing_session = Session.search(db_handler, {"email": email})
    
    if existing_session:
        user_session = existing_session[0]
    else:
        user_session = Session.create_from_user(db_handler, email, True)
    
    template = "singleCard.html" if random.random() < 0.5 else "doubleCard.html"
    resp = make_response(render_template(template))
    resp.set_cookie(
        app.config['SESSION_COOKIE_NAME'],
        user_session.session_id,
        max_age=app.config['PERMANENT_SESSION_LIFETIME'].seconds
    )
    print(f"[DEBUG] Set cookie: {app.config['SESSION_COOKIE_NAME']} = {user_session.session_id}")
    return resp

@app.route('/login/guest', methods=['POST', 'GET'])
def login_guest():
    session_id = request.cookies.get(app.config['SESSION_COOKIE_NAME'])
    #print(session_id)
    existing_session = Session.search(db_handler, {"session_id": session_id})
    #print(existing_session)
    
    if len(existing_session) > 0:
        print("[INFO] Returning guest user has no coockie go back to login") 
        user_session = existing_session[0]
    else:
        print("[INFO] New guest user has no coockie go back to login") 
        user_session = Session.create_from_user(db_handler, "", True)
    template = "singleCard.html" if random.random() < 0.5 else "doubleCard.html"
    resp = make_response(render_template(template))
    resp.set_cookie(
        app.config['SESSION_COOKIE_NAME'],
        user_session.session_id,
        max_age=app.config['PERMANENT_SESSION_LIFETIME'].seconds
    )
    return resp

@app.route('/generate', methods=['POST'])
def generate():
    session_id = request.cookies.get(app.config['SESSION_COOKIE_NAME'])
    existing_session = Session.search(db_handler, {"session_id": session_id})
    
    if len(existing_session) > 0:
        user_session = existing_session[0]
        seen_stories = [story_id for story_id in user_session.metrics.get("history", [])]
        
        available_stories = db_handler.find_by_query("stories_database", {})
        unseen_stories = [story for story in available_stories if str(story["_id"]) not in seen_stories]
        
        ## With a small propbability always try and generate new and exciting fake stories.
        print("[INFO] User has not seen stories count:",len(unseen_stories))
        if len(unseen_stories) > 0 and random.random() > 0.9: ## Try and force new generations of stories now
            print("[INFO] Reusing an exsisting story")
            unseen_story = make_serializable(unseen_stories[0])
            ###print(unseen_story)
            return jsonify(unseen_story)
        else:
            print("[INFO] Creating a new story")
            ## Have a function to generate a new input_json by looking at the user data. If the user selects a particular type 
            ## focus on those. Not always one just a single one.
            input_json = {
                "topic": random.choice(TOPIC_CAT),
                "manipulation_methods": 
                    random.sample(MISINFO_CAT, 2)
            }
            result = generate_summaries(input_json)
            
            new_story = {
                "real_summary": result["real_summary"],
                "fake_summary": result["fake_summary"],
                "explanation": result["explanation"],
                "num_occurances": 0,
                "num_success": 0,
                "tags": result.get("tags", {})
            }
            story_id = db_handler.insert("stories_database", new_story)
            new_story["_id"] = story_id
            return jsonify(new_story)
    else:
        print("[INFO] Unknown user cannot give personalized stuff")
        input_json = {
            "topic": "Science",
            "manipulation_methods": [
                "Basic factual inaccuracies",
                "Causation vs Correlation confusion",
                "Bad math/Incorrect science"
            ]
        }
        result = generate_summaries(input_json)
        
        new_story = {
            "real_summary": result["real_summary"],
            "fake_summary": result["fake_summary"],
            "explanation": result["explanation"],
            "num_occurances": 0,
            "num_success": 0,
            "tags": result.get("tags", {})
        }
        story_id = db_handler.insert("stories_database", new_story)
        new_story["_id"] = story_id
        return jsonify(new_story)


@app.route('/submit-answer', methods=['POST'])
def submit_answer():
    try:
        session_id = request.cookies.get(app.config['SESSION_COOKIE_NAME'])
        data = request.json
        if not session_id or not data:
            return jsonify({"error": "Missing session ID or request data"}), 400

        selected_position = data.get('selectedPosition')
        correct_fake_position = data.get("correctFakePosition")
        story_id = data.get("story_id")
        
        if not story_id:
            return jsonify({"error": "Missing story ID"}), 400
        
        existing_session = Session.search(db_handler, {"session_id": session_id})
        if not existing_session:
            return jsonify({"error": "Session not found"}), 404
        
        user_session = existing_session[0]
        story_data = db_handler.find_by_id("stories_database", story_id)
        if not story_data:
            return jsonify({"error": "Story not found"}), 404
        
        correct = selected_position == correct_fake_position
        #### Handle DB updates over different versions
        user_session.metrics.setdefault("score", 0)
        user_session.metrics.setdefault("history", [])
        
        user_session.metrics["score"] += 100 if correct else 0
        user_session.metrics["history"].append({"story_id": story_id, "correct": correct})
        
        if not db_handler.update("session_db", user_session._id, {"metrics": user_session.metrics}):
            return jsonify({"error": "Failed to update session"}), 500
        
        story_data["num_occurances"] = story_data.get("num_occurances", 0) + 1
        if correct:
            story_data["num_success"] = story_data.get("num_success", 0) + 1
        
        if not db_handler.update("stories_database", story_id, story_data):
            return jsonify({"error": "Failed to update story"}), 500
        
        return jsonify({
            "correct": correct,
            "score": user_session.metrics["score"],
            "explanation": "You selected the wrong summary. The fake summary used misleading statistics." if not correct else ""
        })
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
    

@app.route('/login/new_question', methods=['POST'])
def new_question():
    session_id = request.cookies.get(app.config['SESSION_COOKIE_NAME'])
    existing_session = Session.search(db_handler, {"session_id": session_id})
    
    if existing_session:
        user_session = existing_session[0]
        if user_session.isGuest():
            # Redirect to the login email route
            return redirect(url_for('login_missing_email'))
        else:
            # Redirect to the guest login route
            return redirect(url_for('login_guest'))
    else:
        return jsonify({"error": "An unexpected error occurred"}), 500  # Removed 'e' as it's not defined


def updateTrainingSet(minCount=10, minSuccess=6, maxFileSizeMB=100):
    """Updates a json file with all the training generated texts that were able to trick humans with an accuracy over 60%"""
    print(f"[INFO] Scheduled task executed at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    stories = Story.search(db_handler, {})
    if not stories:
        print("[INFO] No stories found in the database.")
        return

    outputFileData = []
    total_size = 0  # Track total file size in bytes

    # Ensure dataset directory exists
    dataset_dir = "./dataset"
    os.makedirs(dataset_dir, exist_ok=True)

    for story_data in stories:
        if story_data.get("num_occurances", 0) > minCount and story_data["num_success"] > minSuccess:
            output = {
                "real_summary": story_data["real_summary"],
                "fake_summary": story_data["fake_summary"],
                "explanation": story_data["explanation"]
            }
            json_data = json.dumps(output, ensure_ascii=False) + "\n"  # JSON line per story
            json_size = len(json_data.encode("utf-8"))  # Get size in bytes

            # Stop if estimated file size exceeds the limit (100MB)
            if total_size + json_size > maxFileSizeMB * 1024 * 1024:
                print(f"[WARNING] Reached file size limit ({maxFileSizeMB}MB). Stopping.")
                break
            
            outputFileData.append(output)
            total_size += json_size

    # Construct filename with timestamp
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_filename = os.path.join(dataset_dir, f"{timestamp}_FinetuningSet.json")

    # Write collected data to file
    try:
        with open(output_filename, "w", encoding="utf-8") as file:
            json.dump(outputFileData, file, ensure_ascii=False, indent=4)
        print(f"[INFO] Saved training data to {output_filename} ({total_size / (1024 * 1024):.2f} MB)")
    except Exception as e:
        print(f"[ERROR] Failed to save training data: {e}")
        time.sleep(120)
        ## Wait 2 mins and restart with half the max size.
        updateTrainingSet(minCount, minSuccess, maxFileSizeMB/2)

scheduler = BackgroundScheduler()
scheduler.add_job(updateTrainingSet, 'interval', hours=2)
scheduler.start()

if __name__ == '__main__':
    try:
        app.run(host="0.0.0.0", debug=True, use_reloader=False)
    except (KeyboardInterrupt, SystemError, SystemExit):
        scheduler.shutdown()