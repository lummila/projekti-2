from flask import Flask, Response, request
from flask_cors import CORS
import game
import json

app = Flask(__name__)
CORS(app)


@app.route("/")  # type: ignore
def register():
    # Rekisteröityminen
    args = request.args
    return


@app.route("/action")  # type: ignore
def action():
    # Lentäminen ja työskentely
    return


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, use_reloader=True)
