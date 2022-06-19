from http import HTTPStatus

import pytest
from src.app import create_app
from src.utils.setting import setting
from tinydb import Query

@pytest.fixture()
def db(app):
    return app.config['DATABASE']

@pytest.fixture()
def app():
    app = create_app('testing')

    yield app

    app.config['DATABASE'].drop_tables()

@pytest.fixture()
def client(app):
    return app.test_client()

def test_health_check_status(client):
    response = client.get("/")
    assert HTTPStatus.OK == response.status_code

def test_health_check_json(client):
    response = client.get("/")
    resp = {
            'app_name': setting.APP_NAME,
            'app_version': setting.APP_VERSION
        }
    assert resp == response.json

def test_create_task(client, db):
    db.drop_tables()

    body={
        "task_column": "todo",
        "task_name": "Testar a API",
        "task_description": ""
    }
    response = client.post("/create_task", json=body)

    assert db.search(Query()['task_column'] == 'todo')[0] == response.json


def test_list_task(client, db):
    db.drop_tables()

    column_name = "todo"
    body={
        "task_column": column_name,
        "task_name": "Testar a API",
        "task_description": ""
    }
    response = client.post("/create_task", json=body)

    response = client.get("/list_tasks")
    assert [
        db.search(Query()['task_column'] == column_name), 
        list(), 
        list()
        ] == response.json

def test_remove_task(client, db):
    db.drop_tables()

    column_name = "todo"
    body = {
        "task_column": column_name,
        "task_name": "Testar a API",
        "task_description": ""
    }
    client.post("/create_task", json=body)

    body = {
        'task_id': db.search(
            Query()['task_column'] == column_name
        )[0]['task_id']
    }
    client.post("/remove_task", json=body)

    assert len(db.search(Query()['task_column'] == column_name)) == 0

def test_move_task_to_in_progress(client, db):
    db.drop_tables()

    column_name = "todo"
    body = {
        "task_column": column_name,
        "task_name": "Testar a API",
        "task_description": ""
    }
    client.post("/create_task", json=body)

    task_id = db.search(
            Query()['task_column'] == column_name
        )[0]['task_id']
    next_column = 'in_progress'
    body = {
        'task_id': task_id,
        'next_column': next_column
    }
    client.post("/move_task", json=body)

    todo = db.search(
            Query()['task_column'] == column_name
        )
    
    in_progress = db.search(
            Query()['task_column'] == next_column
        )

    assert len(todo) == 0 and len(in_progress) == 1

def test_move_task_to_done(client, db):
    db.drop_tables()

    column_name = "todo"
    body = {
        "task_column": column_name,
        "task_name": "Testar a API",
        "task_description": ""
    }
    client.post("/create_task", json=body)

    task_id = db.search(
            Query()['task_column'] == column_name
        )[0]['task_id']
    next_column = 'done'
    body = {
        'task_id': task_id,
        'next_column': next_column
    }
    client.post("/move_task", json=body)

    todo = db.search(
            Query()['task_column'] == column_name
        )
    
    done = db.search(
            Query()['task_column'] == next_column
        )

    assert len(todo) == 0 and len(done) == 1
