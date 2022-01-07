import os
import time
import uuid
from threading import Thread
from flask import Flask, jsonify, render_template

app = Flask(__name__)
app.secret_key = os.urandom(42)

# Define a global variable to store the current status of all threads
status = {}

def threaded_task(task_count, thread_key):
    ''' Main thread function that run the thread process '''
    global status
    for task_no in range(task_count):
        print("Thread {},Working on task {}/{}".format(thread_key, task_no, task_count))
        status[str(thread_key)] = task_no
        time.sleep(5)


@app.route("/start")
def start():
    ''' Starts a process '''
    global status
    #Define total task to be executed
    TOTAL_TASK_COUNT = 100
    #initializing the thread
    thread_key = uuid.uuid1()
    thread = Thread(target=threaded_task, args=(TOTAL_TASK_COUNT,thread_key,))
    thread.daemon = True
    #starting the thread
    thread.start()
    # returning to the page while the thread is running in background
    res = {'thread_key': str(thread_key), 'thread_name': str(thread.name)}
    return render_template('index.html', value=res)

@app.route("/status/<string:thread_key>")
def current_status(thread_key):
    thread_current_status = status[thread_key]
    return jsonify({'status': thread_current_status})

if __name__ == '__main__':
    app.run(debug=True)