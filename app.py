import os
import time
import uuid
from threading import Thread
from flask import Flask, jsonify, render_template

app = Flask(__name__)
app.secret_key = os.urandom(42)

# Define a global variable to store the current status of all threads
status = {}

def threaded_task(duration, thread_key):
    ''' Main thread function that run the thread process '''
    global status
    for i in range(duration):
        print("Working...{} {}/{}".format(thread_key, i + 1, duration))
        status[str(thread_key)] +=1
        time.sleep(5)


@app.route("/start")
def start():
    ''' Starts a process '''
    global status
    thread_key = uuid.uuid1()
    thread = Thread(target=threaded_task, args=(100,thread_key,))
    thread.daemon = True
    thread.start()
    status[str(thread_key)] = 0
    res = {'thread_key': str(thread_key), 'thread_name': str(thread.name)}
    return render_template('index.html', value=res)

@app.route("/status/<string:thread_key>")
def current_status(thread_key):
    return jsonify({'thread_key': thread_key,
                    'status': status[thread_key]})

if __name__ == '__main__':
    app.run(debug=True)
