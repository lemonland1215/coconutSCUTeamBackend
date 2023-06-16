from flask import Flask, request, url_for
from datetime import datetime

app = Flask(__name__, static_folder="E:\\Programming\\testpython\\eg_flask\\phishing system\\app\\main",
            static_url_path="")


@app.route("/", methods=["GET"])
def hello_world():
    return url_for("logo")




app.run(debug=True, port=5001)
