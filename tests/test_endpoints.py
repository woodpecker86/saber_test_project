# main tests
import json

from src.main import build_app as app


def test_get_tasks(client):
    url = app.url_path_for('get_tasks')
    response = client.post(url, content=json.dumps({'build': 'make_tests'}))
    assert response.status_code == 200
    assert response.json() == {'build': 'make_tests'}
