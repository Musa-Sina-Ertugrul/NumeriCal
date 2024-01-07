import json
from flask import Flask, request, jsonify, render_template
from fixed_point import main

app = Flask(__name__)


@app.route("/")
def home():
    """
    Render the home page.

    Returns:
    str: Rendered HTML for the home page.
    """
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    """
    Perform fixed-point iteration calculations based on user input.

    JSON Payload:
    {
        "func": str,       # Mathematical function as a string
        "max_iter": int,   # Maximum number of iterations
        "tolerance": float # Tolerance for error
    }

    Returns:
    JSON: Computed roots and iteration information.
    """
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
    """
    Decode JSON data into function parameters.

    Args:
    data (json): JSON data containing function parameters.

    Returns:
    tuple: Tuple of function, max_iter, and tolerance.
    """
    func = data.get("func", None)
    # x0=data.get("x0",None)
    max_iter = data.get("max_iter", None)
    tolerance = data.get("tolerance", None)
    return func, max_iter, tolerance


def encode_json(results):
    """
    Encode computed roots and iteration information into JSON format.

    Args:
    results: Computed roots and iteration information.

    Returns:
    str: JSON-encoded string.
    """
    return json.dumps(
        {
            "roots": list([f"{result[-1]:.2f}" for result in results]),
            "iterations": [len(result) for result in results],
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
