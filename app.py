from flask import Flask, render_template, request, jsonify, make_response
from config import Config
from utils.helpers import create_user_session
from backend.openai import generate_summaries
from utils.db import save_session, get_session, save_story, get_random_story, format_story_data, CATEGORIES
import random
import time


## Add the ability to automatically store those reponses that fooled the humans.
## Add event listener in GPT code to auto retrain after it reaches 50 or so new responses. ### Very important. 
## Also, we have data regarding every users category that they were weak at so focus more on that. 

CATEGORIES = list(range(1, len(CATEGORIES)+1))

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login/email', methods=['GET'])
def login_email_error():
    return render_template('login.html')

@app.route('/login/email', methods=['POST'])
def login_email():
    email = request.form.get('email')
    session_data = create_user_session(email=email)
    save_session(session_data['session_id'], session_data)

    template = "singleCard.html" if random.random() < 0.5 else "doubleCard.html"
    resp = make_response(render_template(template))
    resp.set_cookie(
        app.config['SESSION_COOKIE_NAME'],
        session_data['session_id'],
        max_age=app.config['PERMANENT_SESSION_LIFETIME'].seconds
    )
    return resp

@app.route('/login/guest', methods=['POST', 'GET'])
def login_guest():
    session_id = request.cookies.get(app.config['SESSION_COOKIE_NAME'])

    if session_id:
        session_data = get_session(session_id)
        if session_data:
            print(f"[INFO] Returning existing session for {session_id}")
            template = "singleCard.html" if random.random() < 0.5 else "doubleCard.html"
            return render_template(template, session_data=session_data)

    session_data = create_user_session()
    save_session(session_data['session_id'], session_data)

    template = "singleCard.html" if random.random() < 0.5 else "doubleCard.html"
    resp = make_response(render_template(template, session_data=session_data))
    resp.set_cookie(
        app.config['SESSION_COOKIE_NAME'],
        session_data['session_id'],
        max_age=app.config['PERMANENT_SESSION_LIFETIME'].seconds
    )
    return resp

@app.route('/api/next-story', methods=['GET'])
def next_story():
    session_id = request.cookies.get(app.config['SESSION_COOKIE_NAME'])
    session_data = get_session(session_id)

    if not session_data:
        return jsonify({"error": "Session not found"}), 400

    fake_level = session_data.get("difficulty", 3)  # Get difficulty from session

    # Call OpenAI's API to generate real and fake summaries
    result = generate_summaries("Random news article", fake_level)

    # Parse the response
    try:
        summaries = result if isinstance(result, dict) else eval(result)  # Convert string JSON to dict
    except Exception as e:
        return jsonify({"error": f"Failed to parse AI response: {str(e)}"}), 500

    # Create a story entry and store it in MongoDB
    story_data = {
        "image": "https://picsum.photos/800/400",
        "fake_summary": summaries.get("fake_summary", "Failed to generate summary."),
        "real_summary": summaries.get("real_summary", "Failed to generate summary."),
        "explanation": summaries.get("explanation", "No explanation provided."),
        "fakePosition": 2 if fake_level % 2 == 0 else 1,
        "numberOfAppearences": 0,
        "numberOfTimesTrciked": 0,
        "type": assigned_category  # Store the assigned categories
    }
    formatted_story = format_story_data(story_data)
    story_id = save_story(formatted_story)
    formatted_story["_id"] = str(story_id)  # Convert ObjectId to string for JSON

    return jsonify(formatted_story)

@app.route('/submit-answer', methods=['POST'])
def submit_answer():
    session_id = request.cookies.get(app.config['SESSION_COOKIE_NAME'])
    data = request.json
    selected_position = data['selectedPosition']
    correct_fake_position = data.get("correctFakePosition")
    story_id = data.get("story_id")

    session_data = get_session(session_id)

    if not session_data:
        return jsonify({"error": "Session not found"}), 400

    # Determine if the user was correct
    correct = selected_position == correct_fake_position

    # Update metrics
    if correct:
        session_data['metrics']['score'] += 100
        session_data['metrics']['correct'] += 1
    else:
        session_data['metrics']['incorrect'] += 1

    # Update session history
    session_data['metrics']['history'].append({
        "story_id": story_id,
        "answeredCorrect": correct
    })

    save_session(session_id, session_data)

    return jsonify({
        "correct": correct,
        "score": session_data['metrics']['score'],
        "explanation": "You selected the wrong summary. The fake summary used misleading statistics." if not correct else ""
    })
    
##### Not used remove after dev.
@app.route('/log-click', methods=['POST'])
def log_click():
    try:
        data = request.get_json()
        selected_news = data.get("selected_news", None)
        correct_fake_position = data.get("correct_fake_position", None)

        if selected_news not in [1, 2]:
            return jsonify({"error": "Invalid selection"}), 400

        print(f"[INFO] User clicked on news {selected_news}. Correct position was: {correct_fake_position}")

        return jsonify({"message": f"User clicked on news {selected_news}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate():
    try:
        fake_level = 3  # Hardcoded for now, should be fetched from session later
        result = generate_summaries("Default news story.", fake_level)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)