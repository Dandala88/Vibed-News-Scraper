from flask import Flask, render_template, request, jsonify
import json
from agent import NewsAgent
import threading
import time

app = Flask(__name__)

# Global agent instance
agent = NewsAgent()
current_task = None
task_results = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/run_agent', methods=['POST'])
def run_agent():
    global current_task, task_results
    
    data = request.get_json()
    query = data.get('query', 'Get me the latest news and summarize it')
    
    # Check if agent is already running
    if current_task and current_task.is_alive():
        return jsonify({'error': 'Agent is already running'}), 400
    
    # Reset previous results
    task_results = None
    
    # Start agent in background thread
    def run_agent_task():
        global task_results
        try:
            print(f"Starting agent with query: {query}")
            task_results = agent.run(query)
            print(f"Agent completed. Results keys: {list(task_results.keys()) if task_results else 'None'}")
        except Exception as e:
            print(f"Agent error: {e}")
            task_results = {'error': str(e)}
    
    current_task = threading.Thread(target=run_agent_task)
    current_task.start()
    
    return jsonify({'message': 'Agent started', 'query': query})

@app.route('/api/status')
def get_status():
    global current_task, task_results
    
    if current_task and current_task.is_alive():
        return jsonify({'status': 'running', 'progress': 'Agent is working...'})
    elif task_results:
        return jsonify({'status': 'completed', 'results': task_results})
    else:
        return jsonify({'status': 'idle'})

@app.route('/api/results')
def get_results():
    global task_results
    
    if task_results:
        return jsonify(task_results)
    else:
        return jsonify({'error': 'No results available'}), 404

if __name__ == '__main__':
    print("Starting News Agent Web Interface...")
    print("Visit http://localhost:5000 to interact with the agent")
    app.run(debug=True, host='0.0.0.0', port=5000)