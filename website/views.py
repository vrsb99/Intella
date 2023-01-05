from flask import Blueprint, render_template
from . import db

views = Blueprint('views', __name__)
products = ['oreo original', "lay's classic", 'camel roasted peanuts', 'lindor cornet milk', 'ruffles original', 'anchor strong beer']

@views.route('/')
def homepage():
    return render_template('index.html')