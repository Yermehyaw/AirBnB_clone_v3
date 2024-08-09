#!/usr/bin/python3
"""
Test functions in flask app.py

IMPORTS: client
"""
from tests.test_api import client


def test_404(client):
    """Test error handler 404"""
    res = client.get('/api/v2')
    assert status_code == 400
    assert b'error: Not found' in res.data
