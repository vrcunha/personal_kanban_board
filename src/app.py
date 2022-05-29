from datetime import datetime
from http import HTTPStatus
from flask import Flask, jsonify, request, Response
from src.utils.setting import setting
from tinydb import TinyDB, Query
from uuid import uuid4
db = TinyDB('tasks_db.json')

# from flask import Blueprint, jsonify, redirect, request, 
def create_app():

    app = Flask(__name__)

    @app.route('/', methods=['GET'], strict_slashes=False)
    def health_check():
        resp = {
            'app_name': setting.APP_NAME,
            'app_version': setting.APP_VERSION
        }
        return jsonify(resp), HTTPStatus.OK
    
    @app.route('/create_task', methods=['POST'], strict_slashes=False)
    def create_task():
        body = request.json
        column = body.get('column')
        task_name = body.get('task_name')
        task_description = body.get('task_description', '')

        db.insert(
            {
                "task_column": column,
                "task_id": str(uuid4()),
                "task_name": task_name,
                "task_description": task_description,
                "metadata":{
                    "creation_time": datetime.now().timestamp(),
                    "modification_time": datetime.now().timestamp(),
                    "finalization_time": None
                }
            }
        )
        return jsonify(body), HTTPStatus.CREATED

    @app.route('/list_tasks', methods=['GET'], strict_slashes=False)
    def list_tasks():
        todos = db.search(Query()['task_column'] == 'todo')
        in_progress = db.search(Query()['task_column'] == 'in_progress')
        done = db.search(Query()['task_column'] == 'done')

        return jsonify([todos, in_progress, done]), HTTPStatus.OK
    
    @app.route('/remove_task', methods=['POST'], strict_slashes=False)
    def remove_task():
        body = request.json
        task_id = body.get('task_id')

        db.remove(
            Query().task_id == task_id
        )
        return Response('', HTTPStatus.NO_CONTENT)

    @app.route('/move_task', methods=['POST'], strict_slashes=False)
    def move_tasks():
        body = request.json
        task_id = body.get('task_id')
        next_column = body.get('next_column')
        if next_column == 'done':
            task = db.search(
                Query().task_id == task_id
            )[0]
            
            task['task_column'] = next_column
            task['metadata']['finalization_time'] = datetime.now().timestamp()
            db.update(task, Query().task_id == task_id)
            return jsonify({"status": "Task done"}), HTTPStatus.OK

        db.update(
            {
                "task_column": next_column
            },
            Query()['task_id'] == task_id
        )
        return jsonify(f"Task {task_id} was moved to {next_column}"), HTTPStatus.OK

    return app
