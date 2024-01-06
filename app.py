import json
from flask import Flask, request, jsonify, render_template
from fixed_point import main

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    try:
        data = request.get_json()
        func, max_iter, tolerance = decode_json(data)
        result = main(str(func), int(max_iter), float(tolerance))
        print(result)
        encrypted_data = encode_json(result)
        print(f"{encrypted_data}")
        return jsonify({"result": encrypted_data}), 200
    except TypeError as t:
        print(t)
        return json.dumps({"error": "TypeError"}), 401
    except Exception as e:
        print(e)
        return jsonify({"error": e}), 400


def decode_json(data: json):
    func = data.get("func", None)
    # x0=data.get("x0",None)
    max_iter = data.get("max_iter", None)
    tolerance = data.get("tolerance", None)
    return func, max_iter, tolerance


def encode_json(results):
    return json.dumps(
        {
            "roots": list([f"{result[-1]:.2f}" for result in results]),
            "iterations": [len(result) for result in results],
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
