#!/usr/bin/python3
"""
Imports: Blueprint, index, states
"""
from flask import Blueprint


# Create flask Blueprint to be used for all class objects
app_views = Blueprint(
    'app_views',
    __name__,
    template_folder='templates',
    static_folder='static'
)
# Default url prefix is '/api/v1'

from .index import *
from .states import *
from .cities import *
