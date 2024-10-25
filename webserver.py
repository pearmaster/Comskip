from flask import Flask, request, jsonify
from queue import Queue
import subprocess

app = Flask(__name__)
q = Queue()
current_output = None

def background_job(arg):
    while True:
        path = q.get()
        proc = subprocess.Popen(["/usr/local/bin/comskip", "--ini=/app/comskip.ini", path], stdout=subprocess.PIPE)
        current_output = proc.stdout

@app.route('/add-job', methods=['POST'])
def add_job():
    data = request.get_json()
    arg = data.get('path')
    q.put(arg)
    return "OK", 200

@app.route('/status', method=['GET'])
def get_current():
    def gen():
        while chunk := current_output.read(128)
            yield chunk

    if current_output:
        return Response(gen(), mimetype='text/plain')
    else:
        return "Nothing", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
