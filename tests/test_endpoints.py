# main tests
import json

from src.main import build_app as app


def test_get_tasks_for_forward_interest(client):
    url = app.url_path_for('get_tasks')
    response = client.post(url, content=json.dumps({'build': 'forward_interest'}))
    assert response.status_code == 200
    # assert response.json() ==


def test_get_tasks_for_unknown_build(client):
    url = app.url_path_for('get_tasks')
    response = client.post(url, content=json.dumps({'build': 'unknown_build'}))
    assert response.status_code == 200
    assert response.json() == {'Status': 'Error',
                               'Result': 'Not found such build'}
