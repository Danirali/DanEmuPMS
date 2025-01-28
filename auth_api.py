from flask import Flask, request, jsonify
import bcrypt
import json

app = Flask(__name__)

with open('passwd/credentials.json', 'r') as users_file:
    users = json.load(users_file) 

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username in users:
        stored_hashed_password = users[username]['password_hash']

        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401
    else:
        return jsonify({"message": "User not found"}), 404


app.run(debug=True,port=5000)
