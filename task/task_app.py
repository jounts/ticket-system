import datetime
import re

from flask import Flask, render_template
from flask import jsonify
from flask import make_response
from flask import request

from tasks import get_tasks, task_exists
from tasks import db_check
from tasks import get_task_by_name

app = Flask(__name__)


def main():
    db_check()
    app.run('localhost', port=8080)


@app.route("/tasks")
def task_list():
    tasks = get_tasks()
    return render_template("task.html", tasks=tasks)


@app.route("/tasks/<task_name>")
def task_by_name(task_name):
    if task_exists(task_name):
        tasks = get_task_by_name(task_name)
        return render_template("task.html", tasks=tasks)


if __name__ == '__main__':
    main()
