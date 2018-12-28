
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 21:00:06 2018

@author: Kennedy Sousa
"""

import os.path
import pickle
import requests
import json

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

clf = 'model.pk'
sentiment = {'Negative': -1, 'Neutral': 0, 'Positive': 1}
    
#Load the saved model
print("Loading the model...")
loaded_model = None

with open('./models/'+clf,'rb') as f:
    loaded_model = pickle.load(f)

print("The model has been loaded... \nReady to make predictions...")

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
        

        #predictions = loaded_model.predict(request_json)

        print(request_json['text'])

        probability = loaded_model.predict_proba([request_json['text']])
        
        print (json.dumps({"comment": request_json['text'],
                        "sentiment": dict(zip(list(sentiment.keys()), list(probability[0])))
                    }, 
                    sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False))

        responses = jsonify({"comment": request_json['text'],
                        "sentiment": dict(zip(list(sentiment.keys()), list(probability[0])))
                    })

        responses.status_code = 200
    except Exception as e:
        raise e
    
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
