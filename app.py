from flask import Flask, request, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)

DATA_FOLDER = "data"  # Folder containing your text files
LOG_FILE = "search_log.json"

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form.get('keyword')
    results = []
    for filename in os.listdir(DATA_FOLDER):
        if filename.endswith(".txt"):  # Only search .txt files
            filepath = os.path.join(DATA_FOLDER, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f: # Handle potential encoding issues
                    for i, line in enumerate(f, 1):
                        if keyword.lower() in line.lower():
                            results.append({"file": filename, "line": i, "content": line.strip()})
            except Exception as e:
                print(f"Error reading file {filename}: {e}") # Log file reading errors

    log_search(keyword)
    return jsonify({"results": results})

def log_search(keyword):
    

    log_entry = {
        "ip": request.remote_addr,
        "keyword": keyword,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        # Add more details as needed (screen resolution, etc. - these are harder to get from the backend reliably)
    }

    try:
        with open(LOG_FILE, 'r') as f:
            logs = json.load(f)
    except FileNotFoundError:
        logs = []

    logs.append(log_entry)

    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=4)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)  # For local testing