from flask import Flask,render_template

#create Flask instance
app = Flask(__name__)

#create route decorator
@app.route('/')

def index():
    return "<h1>Hello World!</h1>"

