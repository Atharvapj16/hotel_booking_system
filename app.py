from flask import Flask, request, jsonify, render_template
import pandas as pd
import json
import os

from analytics import generate_insights
from rag import answer_question, initialize_faiss_index
from database import update_database

app = Flask(__name__)

# Load dataset
df = pd.read_csv('data/hotel_bookings.csv')

# Initialize FAISS index
initialize_faiss_index(df)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analytics', methods=['GET', 'POST'])
def analytics():
    if request.method == 'POST':
        insights = generate_insights(df)
        return jsonify(insights)
    return render_template('analytics.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get('question')
    if not question:
        return jsonify({'error': 'Question is required'}), 400
    
    answer = answer_question(question, df)
    log_query(question, answer)
    return jsonify({'answer': answer})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

@app.route('/update', methods=['POST'])
def update():
    new_record = request.json
    update_database(new_record)
    return jsonify({'message': 'Database updated successfully'})

def log_query(question, answer):
    history_file = 'queries_history.json'

    # Ensure the file exists
    if not os.path.exists(history_file):
        with open(history_file, 'w') as f:
            json.dump({}, f)

    with open(history_file, 'r') as f:
        try:
            history = json.load(f)
        except json.JSONDecodeError:
            history = {}

    history[question] = answer

    with open(history_file, 'w') as f:
        json.dump(history, f, indent=4)

if __name__ == '__main__':
    app.run(debug=True)
