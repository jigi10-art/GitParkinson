import pickle
from flask import Flask, redirect, render_template, request, url_for, jsonify
import pandas as pd
import numpy as np
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length
from joblib import load
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
import os
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from flask import make_response
from flask import Flask, render_template, request, make_response
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from flask import session

from flask import render_template, make_response, request
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time


# Define the features used in your machine learning model
feature_names = ["MDVP:Fo(Hz)", "MDVP:Fhi(Hz)", "MDVP:Flo(Hz)", "MDVP:Jitter(%)", "MDVP:Jitter(Abs)", 
                 "MDVP:RAP", "MDVP:PPQ", "Jitter:DDP", "MDVP:Shimmer", "MDVP:Shimmer(dB)", "Shimmer:APQ3", 
                 "Shimmer:APQ5", "MDVP:APQ", "Shimmer:DDA", "NHR", "HNR", "RPDE", "DFA", "spread1", 
                 "spread2", "D2", "PPE"]

# Load the scaler and model
# scaler = load(r'C:\Users\anagh\OneDrive\Desktop\PDFE\scaler_joblib')
scaler = load(r"C:\Users\anagh\OneDrive\Desktop\DUPE\web\PDFE\scaler_joblib")
# model = load(r"C:\Users\anagh\OneDrive\Desktop\PDFE\parkinson_model.sav")
model = load(r"C:\Users\anagh\OneDrive\Desktop\DUPE\web\PDFE\model.sav")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
bootstrap = Bootstrap(app)

# Define Flask forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')

# Routes
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/help')
def help():
    return render_template("help.html")

@app.route('/terms')
def terms():
    return render_template("tc.html")

@app.route("/disindex")
def disindex():
    return render_template("disindex.html")

# Standard credentials
standard_username = "admin"
standard_password = "admin@123"

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username == standard_username and password == standard_password:
            return redirect(url_for('dashboard'))
    return render_template("login.html", form=form)


@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/about2')
def about2():
    return render_template("about2.html")

@app.route('/enquiry')
def enquiry():
    return render_template("enquiry.html")

@app.route('/thanku')
def thanku():
    return render_template("thanku.html")

@app.route('/pd')
def parkinson():
    return render_template("pd.html")

@app.route('/help2')
def help2():
    return render_template("help2.html")

@app.route('/logout')
def logout():
    # Clear the session to logout the user
    session.clear()
    # Render the logout page
    return render_template('logout.html')

@app.route('/preview_input', methods=['POST'])
def preview_input():
    input_data = {}
    for feature_name in feature_names:
        feature = float(request.form[feature_name])
        input_data[feature_name] = feature

    return render_template("preview.html", input_data=input_data)

@app.route('/predict_parkinson', methods=['POST'])
def predict_parkinson():
    input_data = {}
    for feature_name in feature_names:
        feature = float(request.form[feature_name])
        input_data[feature_name] = feature

    # Scale the input data using the loaded scaler
    scaled_input = scaler.transform([list(input_data.values())])

    # Make predictions using the loaded model
    prediction = model.predict(scaled_input)[0]
    print("Type of the model:", type(model))

    # Pass the prediction result to pdresult.html
    return render_template("pdresult.html", prediction=prediction)




if __name__ == "__main__":
    app.run(debug=True)
