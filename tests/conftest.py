import pytest
from app import create_app

application = create_app()

@pytest.fixture
def app():
    yield application

@pytest.fixture
def client(app):
    print(app.static_url_path)
    return app.test_client()