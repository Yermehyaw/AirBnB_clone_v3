#!/usr/bin/python3
"""
Test flask app staorage index functions
"""
from test_api import client
from models import storage as chosen_storage

def test_status(client):
    """Test status of flask app"""
    res = client.get('/status')
    assert res.status_code == 200
    assert b'status: OK' in res.data

def test_total_objs(client):
    """Test the total count of objs returned"""
    # NOTE: This is really a pseudotest, becasue no change is made to 
    # the chosen_storage object
    res = client.get('/api/v1/stat')
    assert res.status_code == 200
