import threading

from flask import Flask, jsonify

app = Flask(__name__)

lock = threading.Lock()

COUNTER_FILE = "server/counter.txt"


def read_counter():
    with open(COUNTER_FILE, "r") as f:
        return int(f.read())


def write_counter(value):
    with open(COUNTER_FILE, "w") as f:
        f.write(str(value))


# initialize on startup
write_counter(0)


@app.route("/inc", methods=["GET", "POST"])
def increment():
    with lock:
        # not using read and write functions to avoid opening twice
        with open(COUNTER_FILE, "r+") as f:
            value = int(f.read()) + 1
            f.seek(0)
            f.write(str(value))
    return jsonify({"counter current value": value})


@app.route("/count", methods=["GET"])
def get_count():
    return jsonify({"count": read_counter()})


@app.route("/reset", methods=["GET", "POST"])
def reset():
    global counter
    with lock:
        write_counter(0)
    return jsonify({"count": read_counter()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=False, threaded=True)
