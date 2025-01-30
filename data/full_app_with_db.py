from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS  # Import CORS
import bcrypt
import json
from functools import wraps
from flask_sqlalchemy import SQLAlchemy

# Configure SQLite (or switch to PostgreSQL/MySQL if needed)

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session handling

app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pms.db'  # Change to PostgreSQL/MySQL if needed
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Property(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  value = db.Column(db.Float, nullable=False)


class Income(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  property_id = db.Column(db.Integer,
                          db.ForeignKey('property.id'),
                          nullable=False)
  amount = db.Column(db.Float, nullable=False)
  date = db.Column(db.DateTime, default=db.func.current_timestamp())


class Expense(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  property_id = db.Column(db.Integer,
                          db.ForeignKey('property.id'),
                          nullable=False)
  amount = db.Column(db.Float, nullable=False)
  category = db.Column(db.String(100))
  date = db.Column(db.DateTime, default=db.func.current_timestamp())


with app.app_context():
  db.create_all()  # Creates the tables if they don’t exist

CORS(app, origins="http://127.0.0.1:8080")

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
  new_property = Property(name=data['name'], value=data['value'])
  db.session.add(new_property)
  db.session.commit()
  return jsonify({"message": "Property added successfully!"})


@app.route('/api/add_income', methods=['POST'])
@login_required
def add_income():
  data = request.json
  new_income = Income(property_id=data['property_id'], amount=data['amount'])
  db.session.add(new_income)
  db.session.commit()
  return jsonify({"message": "Income added successfully!"})


@app.route('/api/add_expense', methods=['POST'])
@login_required
def add_expense():
  data = request.json
  new_expense = Expense(property_id=data['property_id'],
                        amount=data['amount'],
                        category=data['category'])
  db.session.add(new_expense)
  db.session.commit()
  return jsonify({"message": "Expense added successfully!"})


@app.route('/api/properties', methods=['GET'])
@login_required
def get_properties():
  properties = Property.query.all()
  return jsonify([{
      "id": p.id,
      "name": p.name,
      "value": p.value
  } for p in properties])


@app.route('/api/remove_property/<int:property_id>', methods=['DELETE'])
@login_required
def remove_property(property_id):
  property_to_delete = Property.query.get(property_id)

  if not property_to_delete:
    return jsonify({"message": "Property not found"}), 404

  db.session.delete(property_to_delete)
  db.session.commit()

  return jsonify({"message": "Property removed successfully!"})


@app.route('/')
def home_ui():
  return render_template('index.html')


@app.route('/properties/add', methods=['GET'])
@login_required
def add_property_form():
  return render_template('add_property.html')


@app.route('/properties/delete', methods=['GET'])
@login_required
def del_property_form():
  return render_template('delete_property.html')


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
