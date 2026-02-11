import threading

from flask import Flask, jsonify

app = Flask(__name__)

lock = threading.Lock()
counter = 0


@app.route("/inc", methods=["GET", "POST"])
def increment():
    global counter
    with lock:
        counter += 1
    return jsonify({"counter current value": counter})


@app.route("/count", methods=["GET"])
def get_count():
    return jsonify({"count": counter})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False, threaded=True)
