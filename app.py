from flask import Flask
from flask_cors import CORS

# import game
from sql import Sql
# import json

app = Flask(__name__)
CORS(app)


@app.route("/<name>/<pincode>")
def play(name, pincode):
    username = name
    pin_code = pincode

    sql = Sql()

    return sql.login(username, pin_code)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3306, use_reloader=True)
