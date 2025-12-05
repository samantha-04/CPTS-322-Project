from flask import Flask, jsonify, request
from flask_cors import CORS
import csv
import os
import json
import hashlib
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from Matching import Matching

app = Flask(__name__)
CORS(app)

# Paths
CSV_FILE_PATH_SURVEY_ANSWERS = Path(__file__).parent.parent / 'data' / 'survey_answers.csv'
USERS_FILE_PATH = Path(__file__).parent / 'users.json'

# Question definitions for the questionnaire
QUESTIONS = {
    "q_smoking": {"type": "yes_no", "label": "Do you smoke?", "weight": 1.0},
    "q_pets": {"type": "yes_no", "label": "Do you have pets?", "weight": 1.0},
    "q_clean_freq": {"type": "frequency_4", "label": "How often do you clean?", "weight": 1.0},
    "q_social": {"type": "likert_5", "label": "I like having friends over.", "weight": 1.0},
    "q_noise": {"type": "likert_5", "label": "I don't mind loud music.", "weight": 1.0},
    "q_quiet_hours": {"type": "yes_no", "label": "Should we have quiet hours?", "weight": 1.0},
    "q_shared_food": {"type": "yes_no", "label": "Are you ok with shared groceries?", "weight": 1.0},
    "q_sleep_schedule": {"type": "likert_5", "label": "I prefer to go to bed early.", "weight": 1.0},
    "q_noise_tolerance": {"type": "likert_5", "label": "I am comfortable with background noise.", "weight": 1.0},
    "q_alcohol": {"type": "yes_no", "label": "Are you okay with alcohol being consumed in the home?", "weight": 1.0},
    "q_share_chores": {"type": "yes_no", "label": "Are you willing to share chores fairly?", "weight": 1.0},
    "q_temperature_pref": {"type": "likert_5", "label": "I prefer a cooler apartment (lower thermostat).", "weight": 1.0},
    "q_overnight_guests": {"type": "frequency_4", "label": "How often do you have overnight guests?", "weight": 1.0},
    "q_shared_groceries": {"type": "likert_5", "label": "I am open to sharing kitchen appliances and cookware.", "weight": 0.8},
    "q_work_from_home": {"type": "frequency_4", "label": "How often do you work/study from home?", "weight": 0.9},
    "q_morning_routine": {"type": "likert_5", "label": "I need the bathroom for a long time in the morning.", "weight": 0.7},
    "q_social_events": {"type": "frequency_4", "label": "How often do you attend social events outside the home?", "weight": 0.8},
    "q_tv_music": {"type": "likert_5", "label": "I often play music or watch TV in common areas.", "weight": 0.9},
    "q_visitors_notice": {"type": "yes_no", "label": "Should roommates give advance notice before having visitors?", "weight": 1.0},
    "q_decorating": {"type": "likert_5", "label": "I like to personalize and decorate shared spaces.", "weight": 0.6},
    "q_conflict_style": {"type": "likert_5", "label": "I prefer to address conflicts directly rather than avoid them.", "weight": 1.0},
    "q_budget_conscious": {"type": "likert_5", "label": "I am budget-conscious with utilities and shared expenses.", "weight": 0.9}
}

# Response mappings for converting to numeric values
RESPONSE_MAPPINGS = {
    'yes_no': {'Yes': 1.0, 'No': -1.0},
    'likert_5': {
        'Strongly Disagree': -1.0,
        'Disagree': -0.5,
        'Neutral': 0,
        'Agree': 0.5,
        'Strongly Agree': 1.0
    },
    'frequency_4': {
        'Never': -1.0,
        'Sometimes': -0.33,
        'Often': 0.33,
        'Always': 1.0
    }
}


def hash_password(password):
    """Simple password hashing using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def load_users():
    """Load users from JSON file"""
    if not USERS_FILE_PATH.exists():
        return {}
    try:
        with open(USERS_FILE_PATH, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_users(users):
    """Save users to JSON file"""
    with open(USERS_FILE_PATH, 'w') as f:
        json.dump(users, f, indent=2)


def load_survey_data():
    """Load survey answers from CSV file"""
    if not CSV_FILE_PATH_SURVEY_ANSWERS.exists():
        return {}
    
    survey_data = {}
    try:
        with open(CSV_FILE_PATH_SURVEY_ANSWERS, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                username = row.get('username')
                if username:
                    survey_data[username] = {k: v for k, v in row.items() if k != 'username'}
    except FileNotFoundError:
        pass
    return survey_data


def convert_answers_to_vector(answers):
    """Convert survey answers to numeric vector for matching algorithm"""
    vector = []
    for q_key in sorted(QUESTIONS.keys()):
        q_meta = QUESTIONS[q_key]
        answer = answers.get(q_key, '')
        q_type = q_meta.get('type')
        weight = q_meta.get('weight', 1.0)
        
        if q_type and q_type in RESPONSE_MAPPINGS:
            numeric_value = RESPONSE_MAPPINGS[q_type].get(answer, 0)
            vector.append(numeric_value * weight)
        else:
            # For free-text questions, use 0
            vector.append(0)
    
    return vector


# ==================== HEALTH CHECK ====================

@app.route('/health')
def health():
    return jsonify({'status': 200, 'message': 'API is live'})


# ==================== AUTH ENDPOINTS ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """
    Register a new user. Expects JSON payload:
    {
        "email": "user@example.com",
        "password": "password123",
        "name": "User Name" (optional)
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'status': 400, 'message': 'No data provided'}), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        name = data.get('name', '').strip()
        
        # Validation
        if not email:
            return jsonify({'status': 400, 'message': 'Email is required'}), 400
        if not password:
            return jsonify({'status': 400, 'message': 'Password is required'}), 400
        if len(password) < 8:
            return jsonify({'status': 400, 'message': 'Password must be at least 8 characters'}), 400
        
        # Load existing users
        users = load_users()
        
        # Check if user already exists
        if email in users:
            return jsonify({'status': 409, 'message': 'User already exists'}), 409
        
        # Create new user
        users[email] = {
            'email': email,
            'password': hash_password(password),
            'name': name or email.split('@')[0],
            'profile': {
                'age': None,
                'major': None,
                'bio': ''
            },
            'surveyCompleted': False
        }
        
        save_users(users)
        
        # Return user data (without password)
        user_response = {k: v for k, v in users[email].items() if k != 'password'}
        
        return jsonify({
            'status': 200,
            'message': 'Registration successful',
            'user': user_response
        }), 200
        
    except Exception as e:
        return jsonify({'status': 500, 'message': f'Registration error: {str(e)}'}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """
    Login user. Expects JSON payload:
    {
        "email": "user@example.com",
        "password": "password123"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'status': 400, 'message': 'No data provided'}), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'status': 400, 'message': 'Email and password are required'}), 400
        
        # Load users
        users = load_users()
        
        # Check if user exists
        if email not in users:
            return jsonify({'status': 401, 'message': 'Invalid credentials'}), 401
        
        # Verify password
        if users[email]['password'] != hash_password(password):
            return jsonify({'status': 401, 'message': 'Invalid credentials'}), 401
        
        # Check if survey is completed
        survey_data = load_survey_data()
        users[email]['surveyCompleted'] = email in survey_data
        
        # Return user data (without password)
        user_response = {k: v for k, v in users[email].items() if k != 'password'}
        
        return jsonify({
            'status': 200,
            'message': 'Login successful',
            'user': user_response
        }), 200
        
    except Exception as e:
        return jsonify({'status': 500, 'message': f'Login error: {str(e)}'}), 500


# ==================== QUESTIONS ENDPOINT ====================

@app.route('/api/questions', methods=['GET'])
@app.route('/questions', methods=['GET'])  # Also support the old endpoint
def get_questions():
    """Return the questionnaire questions"""
    return jsonify(QUESTIONS), 200


# ==================== SURVEY ENDPOINT ====================

@app.route('/api/survey/submit', methods=['POST'])
def submit_survey():
    """
    Submit survey answers. Expects JSON payload:
    {
        "username": "user@example.com",
        "answers": {
            "question1": "answer1",
            "question2": "answer2",
            ...
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'status': 400, 'message': 'No data provided'}), 400
        
        username = data.get('username')
        if not username:
            return jsonify({'status': 400, 'message': 'Username is required'}), 400
        
        answers = data.get('answers', {})
        if not answers:
            return jsonify({'status': 400, 'message': 'No answers provided'}), 400
        
        # Ensure the data directory exists
        CSV_FILE_PATH_SURVEY_ANSWERS.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if file exists and if it's empty
        file_exists = CSV_FILE_PATH_SURVEY_ANSWERS.exists() and CSV_FILE_PATH_SURVEY_ANSWERS.stat().st_size > 0
        
        # Sort answer keys to ensure consistent column order
        sorted_keys = sorted(answers.keys())
        
        # Prepare new row data
        new_row_data = {'username': username}
        new_row_data.update(answers)
        
        if not file_exists:
            # File doesn't exist - create it with header and first row
            header = ['username'] + sorted_keys
            with open(CSV_FILE_PATH_SURVEY_ANSWERS, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=header)
                writer.writeheader()
                writer.writerow(new_row_data)
        else:
            # File exists - read existing data
            with open(CSV_FILE_PATH_SURVEY_ANSWERS, 'r', newline='') as readfile:
                reader = csv.DictReader(readfile)
                existing_header = list(reader.fieldnames)
                existing_rows = list(reader)
            
            # Check if user already has a submission - update it
            user_found = False
            for i, row in enumerate(existing_rows):
                if row.get('username') == username:
                    existing_rows[i] = new_row_data
                    user_found = True
                    break
            
            if not user_found:
                existing_rows.append(new_row_data)
            
            # Check for new columns
            new_columns = [key for key in sorted_keys if key not in existing_header]
            updated_header = existing_header + new_columns
            
            # Rewrite file
            with open(CSV_FILE_PATH_SURVEY_ANSWERS, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=updated_header)
                writer.writeheader()
                for row in existing_rows:
                    writer.writerow(row)
        
        # Update user's surveyCompleted status
        users = load_users()
        if username in users:
            users[username]['surveyCompleted'] = True
            save_users(users)
        
        return jsonify({
            'status': 200,
            'message': 'Survey answers saved successfully',
            'username': username,
            'answers_count': len(answers)
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error saving survey answers: {str(e)}'
        }), 500


# ==================== MATCHES ENDPOINT ====================

@app.route('/api/matches/<user_id>', methods=['GET'])
def get_matches(user_id):
    """
    Get potential roommate matches for a user.
    Returns matches sorted by compatibility score.
    """
    try:
        user_id = user_id.lower()
        
        # Load all survey data
        survey_data = load_survey_data()
        
        if user_id not in survey_data:
            return jsonify({
                'status': 404,
                'message': 'User has not completed the survey',
                'matches': []
            }), 404
        
        # Get user's answers and convert to vector
        user_answers = survey_data[user_id]
        user_vector = convert_answers_to_vector(user_answers)
        
        # Load user profiles
        users = load_users()
        
        # Calculate compatibility with all other users
        matches = []
        for other_id, other_answers in survey_data.items():
            if other_id == user_id:
                continue
            
            other_vector = convert_answers_to_vector(other_answers)
            
            # Use the Matching algorithm to calculate compatibility
            try:
                compatibility_score = Matching.Match(user_vector, other_vector)
                # Convert to percentage (0-100 scale)
                compatibility_percent = round((compatibility_score + 1) / 2 * 100)
            except:
                compatibility_percent = 50  # Default if calculation fails
            
            # Get user profile info
            profile = users.get(other_id, {}).get('profile', {})
            name = users.get(other_id, {}).get('name', other_id.split('@')[0])
            
            matches.append({
                'id': other_id,
                'name': name,
                'age': profile.get('age'),
                'major': profile.get('major'),
                'bio': profile.get('bio', ''),
                'compatibility': compatibility_percent,
                'profileImage': None,
                'status': 'pending'
            })
        
        # Sort by compatibility (highest first)
        matches.sort(key=lambda x: x['compatibility'], reverse=True)
        
        return jsonify({
            'status': 200,
            'message': 'Matches retrieved successfully',
            'matches': matches
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error retrieving matches: {str(e)}',
            'matches': []
        }), 500


# ==================== USER PROFILE ENDPOINTS ====================

@app.route('/api/user/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get user profile"""
    try:
        user_id = user_id.lower()
        users = load_users()
        
        if user_id not in users:
            return jsonify({'status': 404, 'message': 'User not found'}), 404
        
        # Check survey status
        survey_data = load_survey_data()
        users[user_id]['surveyCompleted'] = user_id in survey_data
        
        # Return user data (without password)
        user_response = {k: v for k, v in users[user_id].items() if k != 'password'}
        
        return jsonify({
            'status': 200,
            'user': user_response
        }), 200
        
    except Exception as e:
        return jsonify({'status': 500, 'message': f'Error: {str(e)}'}), 500


@app.route('/api/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update user profile. Expects JSON payload:
    {
        "name": "New Name",
        "profile": {
            "age": 21,
            "major": "Computer Science",
            "bio": "Looking for a quiet roommate"
        }
    }
    """
    try:
        user_id = user_id.lower()
        users = load_users()
        
        if user_id not in users:
            return jsonify({'status': 404, 'message': 'User not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'status': 400, 'message': 'No data provided'}), 400
        
        # Update allowed fields
        if 'name' in data:
            users[user_id]['name'] = data['name']
        
        if 'profile' in data:
            current_profile = users[user_id].get('profile', {})
            profile_updates = data['profile']
            
            if 'age' in profile_updates:
                current_profile['age'] = profile_updates['age']
            if 'major' in profile_updates:
                current_profile['major'] = profile_updates['major']
            if 'bio' in profile_updates:
                current_profile['bio'] = profile_updates['bio']
            
            users[user_id]['profile'] = current_profile
        
        save_users(users)
        
        # Return updated user data (without password)
        user_response = {k: v for k, v in users[user_id].items() if k != 'password'}
        
        return jsonify({
            'status': 200,
            'message': 'Profile updated successfully',
            'user': user_response
        }), 200
        
    except Exception as e:
        return jsonify({'status': 500, 'message': f'Error: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5646, debug=True)
