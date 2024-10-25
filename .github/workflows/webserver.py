from flask import Flask, request, jsonify
from queue import Queue
import subprocess

app = Flask(__name__)
q = Queue()

def background_job(arg):
    while True:
        path = q.get()
        subprocess.run(["/usr/local/bin/comskip", path])

@app.route('/add-job', methods=['POST'])
def add_job():
    data = request.get_json()
    arg = data.get('path')
    q.put(arg)
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
