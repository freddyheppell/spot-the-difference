from flask import Flask

app = Flask(__name__)


@app.route("/hello/<string:name>")

def hello(name):

    return "Hello" + name + "!"