import os

import pandas as pd
from flask import Flask, jsonify, render_template, request

app = Flask(__name__, static_folder='static', static_url_path='')
df = pd.read_csv('../data/merged_dataset.csv')

# Determine the starting row based on existing recordings
def get_starting_row():
    audio_files = os.listdir('../audio')
    completed_rows = [int(f.split('.')[0]) for f in audio_files if f.endswith('.wav')]
    max_completed = max(completed_rows + [0])  # + [0] to handle empty directory
    return max_completed + 1 # Start with the next row

starting_row = get_starting_row()
print("starting_row: ", starting_row)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/get_sentence/<int:row_num>', methods=['GET'])
def get_sentence(row_num):
    sentence = df.iloc[row_num]['text']
    return jsonify(sentence=sentence)

@app.route('/save_recording/<int:row_num>', methods=['POST'])
def save_recording(row_num):
    audio_file = request.files['audio']
    audio_file.save(f'../audio/{row_num}.wav')
    with open(f'../audio/{row_num}.txt', 'w') as f:
        f.write(request.form['sentence'])
    return jsonify(success=True)

@app.route('/script.js')
def script():
    starting_row = get_starting_row()
    return render_template('script.js', starting_row=starting_row)

if __name__ == '__main__':
    if not os.path.exists('../audio'):
        os.makedirs('../audio')
    app.run(debug=True)