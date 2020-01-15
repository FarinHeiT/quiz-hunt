import pytest
import os
import tempfile
import sys
from app import app
from app import db
from models import *

@pytest.fixture
def client():
    file = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file[1]
    app.config['TESTING'] = True

    client = app.test_client()

    db.create_all()
    os.close(file[0])
    yield client

    os.unlink(file[1])


def test_index_renders(client):
    """ Index page renders correctly """
    response = client.get('/')
    assert b'New Quiz' in response.data
    assert response.status_code == 200


def test_login_renders(client):
    """ Login page renders correctly """
    response = client.get('/auth/login')
    assert b'Sign In' in response.data
    assert response.status_code == 200


def test_register_renders(client):
    """ Register page renders correctly """
    response = client.get('/auth/register')
    assert b'Sign Up' in response.data
    assert response.status_code == 200

