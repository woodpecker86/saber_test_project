import pytest as pytest
from starlette.config import environ
from starlette.testclient import TestClient

environ['TESTING'] = 'True'

from src import settings
from src.main import build_app


@pytest.fixture()
def client():
    """
    Make a 'client' fixture available to test cases.
    """
    with TestClient(build_app) as test_client:
        yield test_client
