
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 21:00:06 2018

@author: Kennedy Sousa
"""

import os.path
import pickle
import requests

from flask import Flask, render_template, jsonify, request, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_moment import Moment
from datetime import datetime
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'
bootstrap = Bootstrap(app)
moment = Moment(app)

class TextForm(FlaskForm):
    text = TextAreaField('Type the text to classify:', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = TextForm()
    if form.validate_on_submit():
        text = form.text.data
        res = requests.post(url_for('index', _external=True) + 'api/v1/', json={'text':text})
        flash(res.text)
        return redirect(url_for('index'))
    return render_template('index.html', form=form, current_time=datetime.utcnow())

@app.route('/api/v1/', methods=['POST'])
def apicall():
    """API Call

    """

    try:
        request_json = request.get_json()
        # test = pd.read_json(request_json, orient='records')
    except Exception as e:
        raise e

    print(request_json)
    
    responses = jsonify(name="Kennedy")
    responses.status_code = 200
    
    return (responses)

@app.errorhandler(400)
def bad_request(error=None):
	message = {
			'status': 400,
			'message': 'Bad Request: ' + request.url + '--> Please check your data payload...',
	}
	resp = jsonify(message)
	resp.status_code = 400

	return resp

@app.errorhandler(500)
def server_error(error=None):
	message = {
			'status': 500,
			'message': 'Server error! Application failed due to an error on server side.',
	}
	resp = jsonify(message)
	resp.status_code = 500

	return resp
