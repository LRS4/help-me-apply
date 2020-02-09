import os
from flask import Flask, flash, jsonify, json, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from utils import scraper

# PEP8 Python Validator Tool: http://pep8online.com/

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=['GET', 'POST'])
def index():
    """Show introduction screen"""
    return render_template("index.html")

@app.route("/start", methods=['GET', 'POST'])
def start():
    """Show start of application screen"""
    if request.method == 'POST':
        url = request.form.get('url')
        text = scraper.getJobDescription(url)
        verbs, adjectives, adverbs, nouns =  scraper.getWords(text)
        return render_template('start.html', verbs=verbs, adjectives=adjectives, adverbs=adverbs, nouns=nouns)
    else:
        return render_template('start.html')    


if __name__ == '__main__':
    app.run()