from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS  # Import CORS
import bcrypt
import json
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session handling

CORS(app, origins="http://127.0.0.1:8080")

with open('passwd/credentials.json', 'r') as users_file:
    users = json.load(users_file)


# Decorator to protect routes
def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login_ui'))  # Redirect to login page
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def home_ui():
    return render_template('index.html')


@app.route('/privacy-policy', methods=['GET'])
def privacy_policy_ui():
    return render_template('privacy_policy.html')


@app.route('/contact', methods=['GET'])
def contact_page_ui():
    return render_template('contact.html')


@app.route('/pricing', methods=['GET'])
def pricing_ui():
    return render_template('pricing.html')


@app.route('/dashboard')
@login_required  # Protect the dashboard route
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
            session['user_id'] = username  # Store user ID in session
            return jsonify({
                "message": "Login successful",
                "redirect": "/dashboard"
            }), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401
    else:
        return jsonify({"message": "User not found"}), 404


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home_ui'))


app.run(debug=True, port=8080)
