from flask import Flask, render_template, request, jsonify, make_response
from config import Config
from utils.helpers import create_user_session, generate_session_id
from backend.openai import generate_summaries, misinfo_categories 
import time

app = Flask(__name__)
app.config.from_object(Config)

# In-memory storage for demo purposes (use database in production)
sessions = {}
stories_db = [
    {
        'id': 1,
        'image': 'https://picsum.photos/800/400',
        'true_summary': 'Official data shows GDP grew 3.4% in Q2 2023...',
        'fake_summary': 'Government reports secret 5.1% GDP decline...',
        'explanation': 'The fake story uses exaggerated numbers...',
        'fake_position': 2
    }
]

def purgeDB():
    pass

def dispDB():
    print(sessions)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login/email', methods=['POST'])
def login_email():
    email = request.form.get('email')
    session_data = create_user_session(email=email)
    sessions[session_data['session_id']] = session_data
    
    resp = make_response(render_template('index.html'))
    resp.set_cookie(
        app.config['SESSION_COOKIE_NAME'],
        session_data['session_id'],
        max_age=app.config['PERMANENT_SESSION_LIFETIME'].seconds
    )
    return resp

@app.route('/login/guest', methods=['POST', 'GET'])
def login_guest():
    dispDB()
    session_id = request.cookies.get(app.config['SESSION_COOKIE_NAME'])

    if session_id and session_id in sessions:
        session_data = sessions[session_id]
        print(f"[INFO] Returning existing session for {session_id}")
        return render_template('index.html', session_data=session_data)

    ### Create new session
    session_data = create_user_session()
    sessions[session_data['session_id']] = session_data
    
    resp = make_response(render_template('index.html', session_data=session_data))
    resp.set_cookie(
        app.config['SESSION_COOKIE_NAME'],
        session_data['session_id'],
        max_age=app.config['PERMANENT_SESSION_LIFETIME'].seconds
    )
    return resp


@app.route('/api/next-story', methods=['GET'])
def next_story():
    session_id = request.cookies.get(app.config['SESSION_COOKIE_NAME'])

    # Sample article (this should be fetched dynamically in production)
    sample_news_article = """
    Scientists have discovered a new Earth-like exoplanet that may support life.
    The exoplanet, located in the habitable zone of its star, has a similar atmosphere to Earth.
    """

    fake_level = 3  # You can randomize or let users set the difficulty

    # Call OpenAI's API to generate real and fake summaries
    result = generate_summaries(sample_news_article, fake_level)

    # Parse the response
    try:
        summaries = result if isinstance(result, dict) else eval(result)  # Convert string JSON to dict
    except Exception as e:
        return jsonify({"error": f"Failed to parse AI response: {str(e)}"}), 500

    # Return the dynamically generated story
    return jsonify({
        "image": "https://picsum.photos/800/400",  # Placeholder image, can be dynamic
        "trueSummary": summaries.get("real_summary", "Failed to generate summary."),
        "fakeSummary": summaries.get("fake_summary", "Failed to generate summary."),
        "explanation": summaries.get("explanation", "No explanation provided."),
        "fakePosition": 2 if fake_level % 2 == 0 else 1  # Randomize position of fake news
    })

@app.route('/api/submit-answer', methods=['POST'])
def submit_answer():
    session_id = request.cookies.get(app.config['SESSION_COOKIE_NAME'])
    data = request.json
    selected_position = data['selectedPosition']
    start_time = data.get('startTime', time.time())
    
    # Calculate response time
    response_time = time.time() - start_time
    
    # Get current story (demo implementation)
    story = stories_db[0]
    
    # Update session metrics
    session = sessions.get(session_id)
    if session:
        session['metrics']['history'].append({
            'story_id': story['id'],
            'selected_position': selected_position,
            'response_time': response_time,
            'timestamp': time.time()
        })
        
        correct = selected_position == story['fake_position']
        if correct:
            session['metrics']['score'] += 100
            session['metrics']['correct'] += 1
        else:
            session['metrics']['incorrect'] += 1
            
        # Update average response time
        total_responses = session['metrics']['correct'] + session['metrics']['incorrect']
        session['metrics']['avg_response_time'] = (
            (session['metrics']['avg_response_time'] * (total_responses - 1) + response_time) 
            / total_responses
        )
    
    return jsonify({
        'correct': correct,
        'explanation': story['explanation'],
        'score': session['metrics']['score'] if session else 0
    })

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        news_article = data.get("news_article", "Default news story.")
        fake_level = int(data.get("difficulty", 3))  # Fake level (1-9)

        if fake_level < 1 or fake_level > 9:
            return jsonify({"error": "Difficulty must be between 1 and 9"}), 400

        # Generate summaries
        result = generate_summaries(news_article, fake_level)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)