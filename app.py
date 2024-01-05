from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/calculate", methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        func,x0,max_iter,tolerance = decode_json(data)
        root,iterations_number= fixedPoint(func,x0,max_iter,tolerance) #TODO:Handle the fixed point please
        encrypted_data= encode_json(root,iterations_number)
        return jsonify({"result": encrypted_data}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid payload"}), 400

def decode_json(data:json):
    func=data.get("func",None)
    x0=data.get("x0",None)
    max_iter=data.get("max_iter",None)
    tolerance=data.get("tolerance",None)
    print(f"func:{func} \n x0:{x0} \n max_iter:{max_iter} \n tolerance:{tolerance} \n ")
    return func,x0,max_iter,tolerance

def encode_json(root,iterations):

    return jsonify({"root":root,
                    "iterations":iterations})


if __name__ == '__main__':
    app.run(debug=True)
