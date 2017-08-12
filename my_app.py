
from flask import Flask, render_template, request

import controllers

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return "hello world"


@app.route("/add-form", methods=["GET"])
def add():
    return render_template("add.html")


@app.route("/add-post", methods=["POST"])
def add_post():
    try:
        data = request.form
        controller = controllers.ItemController()
        controller.add(data["url"], data["token"], data["phone"])
        return "great success!"

    except Exception:
        return "failed :'("


if __name__ == "__main__":
    app.run()
