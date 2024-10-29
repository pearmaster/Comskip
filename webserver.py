from flask import Flask, request, jsonify, Response
from queue import Queue
import subprocess
import threading

app = Flask(__name__)
q = Queue()
current_output = None

def background_job():
    global current_output
    while True:
        print("Waiting for next file")
        path = q.get()
        print(f"Converting {path}")
        proc = subprocess.Popen(["/usr/local/bin/comskip", "--ini=/app/comskip.ini", path], stdout=subprocess.PIPE)
        current_output = proc.stdout

@app.route('/add-job', methods=['POST'])
def add_job():
    global q
    data = request.get_json()
    if arg := data.get('path'):
        q.put(arg)
        return f"There are {q.qsize()} jobs queued", 200
    return "Invalid Argument", 401

@app.route('/status')
def get_current():
    def gen():
        global current_output
        while chunk := current_output.read(128):
            yield chunk

    if current_output:
        return Response(gen(), mimetype='text/plain')
    else:
        return "Nothing", 200

if __name__ == '__main__':
    print("Running on port 5000")
    thread = threading.Thread(target=background_job)
    thread.start()
    app.run(host='0.0.0.0', port=5000)
