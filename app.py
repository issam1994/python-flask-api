from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return "Welcome to this python based API"


@app.route("/user", methods=["POST"])
def create_user():
    return "User created successfully"


@app.route("/users")
def get_users():
    return jsonify({"id": 1, "name": "issam"})


if __name__ == "__main__":
    app.run(debug=True)
