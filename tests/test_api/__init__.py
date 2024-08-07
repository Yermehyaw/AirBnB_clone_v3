#!/usr/bin/python3
"""
test flask app package initializer
"""
from api.v1 import app
from api.v1.views import app_views
import pytest


@pytest.fixture
def client():
    """Configure flask app for testing"""
    
    app.config['TESTING'] = True  # Disable error catching reports
    
    client = app.test_client
    yield client
