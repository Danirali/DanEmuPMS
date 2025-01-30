from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS  # Import CORS
import bcrypt
import json
from functools import wraps
import pyodbc

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session handling

CORS(app, origins="http://127.0.0.1:8080")

# Path to your Microsoft Access database (.accdb file)
DB_PATH = r"C:\path\to\your\database.accdb"

# Create a connection function
def get_db_connection():
    conn = pyodbc.connect(
        r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"  
        rf"DBQ={DB_PATH};"  # Use raw string format (r"")
    )
    return conn


# Start Requests

with open('passwd/credentials.json', 'r') as users_file:
    users = json.load(users_file)


def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('home_ui'))
        return f(*args, **kwargs)

    return decorated_function

@app.route('/api/add_property', methods=['POST'])
@login_required
def add_property():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO Properties (name, value) VALUES (?, ?)", 
                   (data['name'], data['value']))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"message": "Property added successfully!"})


@app.route('/api/add_income', methods=['POST'])
@login_required
def add_income():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO Income (property_id, amount) VALUES (?, ?)", 
                   (data['property_id'], data['amount']))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"message": "Income added successfully!"})


@app.route('/api/add_expense', methods=['POST'])
@login_required
def add_income():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO Expense (property_id, amount) VALUES (?, ?)", 
                   (data['property_id'], data['amount']))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"message": "Expense added successfully!"})

@app.route('/api/properties', methods=['GET'])
@login_required
def get_properties():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, value FROM Properties")
    properties = [{"id": row[0], "name": row[1], "value": row[2]} for row in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    
    return jsonify(properties)


@app.route('/')
def home_ui():
    return render_template('forms.html')

@app.route('/form')
def form_ui():
    return render_template('forms.html')

@app.route('/privacy-policy', methods=['GET'])
def privacy_policy_ui():
    return render_template('privacy_policy.html')


@app.route('/terms-of-service', methods=['GET'])
def terms_policy_ui():
    return render_template('terms.html')


@app.route('/contact', methods=['GET'])
def contact_page_ui():
    return render_template('contact.html')


@app.route('/pricing', methods=['GET'])
def pricing_ui():
    return render_template('pricing.html')


@app.route('/about', methods=['GET'])
def about_ui():
    return render_template('about.html')


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
            session['user_id'] = username
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


@app.route('/api')
def api_status():
    return jsonify({
        "API Status": "API is running",
        "Endpoints": ["/api/login", "/api/dashboard", "/api/logout"]
    }), 200


app.run(debug=True, port=8080)
