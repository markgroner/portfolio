# import necessary libraries
import numpy as np
import pandas as pd
import os
import datetime

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
from flask_sqlalchemy import SQLAlchemy
'''
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///pub_atx.sqlite"
app.config['GOOGLE_API_KEY'] = os.environ.get('GOOGLE_API_KEY', '') or ''
app.config['QUANDL_API_KEY'] = os.environ.get('QUANDL_API_KEY', '') or ''
'''

db = SQLAlchemy(app)
from .models import Company,company_columns,CompanyPrcsDaily,CompanyPrcsMnthly


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/nba')
def nba_home():
    return render_template('nba_index.html')


@app.route('/nba/lineup_comparison')
def lineup_comparison():
    return render_template('lineup_comparison.html')
