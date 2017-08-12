import datetime
import logging

from flask import Flask, render_template, request

import controllers

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return "hello world"


@app.route("/add-form", methods=["GET"])
def add_form():
    return render_template("add_form.html")


@app.route("/add-post", methods=["POST"])
def add_post():
    try:
        data = request.form
        controller = controllers.ItemController()
        controller.add(data["url"], data["token"], data["phone"])
        return "great success!"

    except Exception:
        return "failed :'("


def scheduled():
    mystring = (f"schedule triggered on {datetime.datetime.utcnow()}")
    logger.info(mystring)

    controller = controllers.ItemController()
    items = controller.get_active_items()
    logger.info(f"processing {len(items)} items")
    controller.process_items(items)

    return mystring


if __name__ == "__main__":
    app.run()
