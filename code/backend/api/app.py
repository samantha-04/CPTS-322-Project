from flask import Flask, jsonify, request
from flask_cors import CORS
import csv
import os
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Path to the CSV file
CSV_FILE_PATH_SURVEY_ANSWERS = Path(__file__).parent.parent / 'data' / 'survey_answers.csv'

@app.route('/health')
def hello():
    return jsonify({'status': 200, 'message': 'API is live'})

@app.route('/api/survey/submit', methods=['POST'])
def submit_survey():
    """
    Submit survey answers. Expects JSON payload with:
    {
        "username": "user123",
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
        
        # Extract username
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
            # File exists - read existing data to check for new columns
            with open(CSV_FILE_PATH_SURVEY_ANSWERS, 'r', newline='') as readfile:
                reader = csv.DictReader(readfile)
                existing_header = reader.fieldnames
                existing_rows = list(reader)
            
            # Check if we have new columns
            new_columns = [key for key in sorted_keys if key not in existing_header]
            
            if new_columns:
                # New columns detected - must rewrite entire file with updated header
                updated_header = list(existing_header) + new_columns
                
                with open(CSV_FILE_PATH_SURVEY_ANSWERS, 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=updated_header)
                    writer.writeheader()
                    # Write all existing rows (new columns will be empty for them)
                    for row in existing_rows:
                        writer.writerow(row)
                    # Write the new row
                    writer.writerow(new_row_data)
            else:
                # No new columns - simple append
                with open(CSV_FILE_PATH_SURVEY_ANSWERS, 'a', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=existing_header)
                    writer.writerow(new_row_data)
        
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5646, debug=True)


