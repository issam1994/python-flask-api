from flask import Flask, request, jsonify
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


def get_db_connection():
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, "database.db")
    db_conn = sqlite3.connect(db_path)
    db_conn.row_factory = sqlite3.Row
    return db_conn


def initialize_db():
    conn = get_db_connection()
    # create users table
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    password TEXT
    )
    """)
    # create notes table
    conn.execute("""
    CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    -- this line establishes the relation:
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)
    # commit the queries
    conn.commit()
    # close connection
    conn.close()


@app.route("/")
def home():
    return "Welcome to this python based API"


@app.route("/user", methods=["POST"])
def create_user():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    # check data is valid
    if not name or not email or not password:
        return jsonify({"error": "missing field"}), 400
    # hash password
    hashed_password = generate_password_hash(password)
    conn = get_db_connection()
    conn.execute(
        """
    INSERT INTO users (name, email, password) VALUES (?,?,?)
    """,
        (name, email, hashed_password),
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "User created successfully"})


@app.route("/users")
def get_users():
    conn = get_db_connection()
    # 1. Fetch all users from the database
    rows = conn.execute("SELECT id, name, email FROM users").fetchall()
    conn.close()
    # 2. Convert SQLite Row objects into a list of regular Python dictionaries
    users_list = []
    for row in rows:
        users_list.append({"id": row["id"], "name": row["name"], "email": row["email"]})
    return jsonify(users_list)


if __name__ == "__main__":
    initialize_db()
    app.run(debug=True)
