from flask import Flask, request, jsonify, render_template


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/calculate", methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        decrypted_data = decrypt_data(data["input"])
        return jsonify({"result": data}), 200
    except Exception:
        return jsonify({"error": "Invalid payload"}), 400




if __name__ == '__main__':
    app.run(debug=True)
