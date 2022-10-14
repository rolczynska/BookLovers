from flask import Flask, render_template, request
import json

app2 = Flask(__name__)


@app2.route("/")
def receive_data():
    return "I am second application."


if __name__ == '__main__':
    app2.run(port=5001)

