from flask import Flask
from flask import render_template, url_for
app = Flask(__name__)

#Comands to execute the app for windows
#venv/Scripts/activate
# $env:FLASK_ENV = "development"
#set FLASK_APP= app.py
#flask run

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/simple-map')
def simple_map():
    return render_template('simple_map.html')