from os import environ
from flask import Flask, redirect

app = Flask(__name__)

@app.route("/")
def home():
    return redirect("https://twitter.com/caitslobstah")

app.run(host='0.0.0.0', port=environ.get('PORT'))