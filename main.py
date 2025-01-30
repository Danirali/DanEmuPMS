from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS  # Import CORS
import bcrypt
import json

app = Flask(__name__)

CORS(app, origins="http://127.0.0.1:8080")

with open('passwd/credentials.json', 'r') as users_file:
    users = json.load(users_file)


@app.route('/')
def home_ui():
    return render_template('index.html')


@app.route('/privacy-policy', methods=['GET'])
def privacy_policy_ui():
    return render_template('privacy_policy.html')


@app.route('/login', methods=['GET'])
def login_ui():
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username in users:
        stored_hashed_password = users[username]['password_hash']

        if bcrypt.checkpw(password.encode('utf-8'),
                          stored_hashed_password.encode('utf-8')):
            return jsonify({
                "message": "Login successful",
                "redirect": "/dashboard"
            }), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401
    else:
        return jsonify({"message": "User not found"}), 404


app.run(debug=True, port=8080)
