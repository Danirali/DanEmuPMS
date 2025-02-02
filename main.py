from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS  # Import CORS
import bcrypt
import json
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy.sql.schema import ForeignKey

# Configure SQLite (or switch to PostgreSQL/MySQL if needed)

PORT = 8080

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session handling

app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pms.db'  # Change to PostgreSQL/MySQL if needed
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Database Structure
class Property(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  value = db.Column(db.Float, nullable=False)
  unit = db.Column(db.String(100), nullable=False)


class Income(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  amount = db.Column(db.Float, nullable=False)
  date = db.Column(db.DateTime, default=db.func.current_timestamp())
  property_id = db.Column(db.Integer,
                          db.ForeignKey('property.id'),
                          nullable=False)
  extra = db.Column(db.String(100), nullable=True)


class Expense(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  amount = db.Column(db.Float, nullable=False)
  category = db.Column(db.String(50), nullable=False)
  property_id = db.Column(db.Integer,
                          db.ForeignKey('property.id'),
                          nullable=False)
  extra = db.Column(db.String(100), nullable=True)


with app.app_context():
  db.create_all()  # Creates the tables if they don’t exist

CORS(app, origins="http://0.0.0.0:"+ str(PORT))

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


def check_auth(f):

  @wraps(f)
  def decorated_function(*args, **kwargs):
    if 'user_id' in session:
      return jsonify({"status": "success"})
    return f(*args, **kwargs)

  return decorated_function


@app.route('/properties/add', methods=['GET'])
@login_required
def add_property_form():
  return render_template('add_property.html')

# API Route for expenses
@app.route('/api/expenses', methods=['GET'])
@login_required
def get_expenses():
  expenses = Expense.query.all()
  return jsonify([{
      "id": expense.id,
      "name": expense.name,
      "amount": expense.amount,
      "category": expense.category,
      "property_id": expense.property_id,
      "extra": expense.extra
  } for expense in expenses])

# API Route for adding expenses
@app.route('/api/expenses/add', methods=['POST'])
@login_required
def add_expense():
  data = request.json

  # Check for missing data
  if 'name' not in data or 'amount' not in data or 'category' not in data:
    return jsonify({"message": "Missing data"},{"data":[data]}), 400

  property_id = data.get('property_id')  # Should be a single ID, not a list
  extra = data.get('extra', None)  # Optional field

  # Create the new expense
  new_expense = Expense(
      name=data['name'],
      amount=float(data['amount']),  # Ensure it's a float
      category=data['category'],
      property_id=int(property_id),  # Ensure it's an integer
      extra=extra if isinstance(extra, str) else None  # Convert only if it's a string
  )
  db.session.add(new_expense)
  db.session.commit()

  return jsonify({"message": "Expense added successfully!"})

@app.route('/api/expenses/delete/<int:expense_id>', methods=['DELETE'])
@login_required
def remove_expense(expense_id):
  expense_to_delete = Expense.query.get(expense_id)

  if not expense_to_delete:
    return jsonify({"message": "Expense not found"}), 404

  db.session.delete(expense_to_delete)
  db.session.commit()

  return jsonify({"message": "Expense removed successfully!"})


# API Route for properties
@app.route('/api/properties', methods=['GET'])
@login_required
def get_properties():
  properties = Property.query.all()
  return jsonify([{
      "id": p.id,
      "name": p.name,
      "value": p.value,
      "unit": p.unit
  } for p in properties])

# API Route for adding properties
@app.route('/api/properties/add', methods=['POST'])
@login_required
def add_property():
  data = request.json

  if 'name' not in data or 'value' not in data or 'unit' not in data:
    return jsonify({"message": "Missing data"},{"data":[data]}), 400

  new_property = Property(name=data['name'],
                          value=data['value'],
                          unit=data['unit'])
  db.session.add(new_property)
  db.session.commit()
  return jsonify({"message": "Property added successfully!"})

@app.route('/api/property/delete/<int:property_id>', methods=['DELETE'])
@login_required
def remove_property(property_id):
  property_to_delete = Property.query.get(property_id)

  if not property_to_delete:
    return jsonify({"message": "Property not found"}), 404

  db.session.delete(property_to_delete)
  db.session.commit()

  return jsonify({"message": "Property removed successfully!"})


# API Route for income
@app.route('/api/income', methods=['GET'])
@login_required
def get_income():
  incomes = Income.query.all()
  return jsonify([{
      "id": income.id,
      "name": income.name,
      "amount": income.amount,
      "date": income.date,
      "property_id": income.property_id,
      "extra": income.extra
  } for income in incomes])

# API Route for adding income
@app.route('/api/income/add', methods=['POST'])
@login_required
def add_income():
  data = request.json

  if 'name' not in data or 'amount' not in data or 'property_id' not in data:
    return jsonify({"message": "Missing data"},{"data":[data]}), 400

  try:
    date_obj = datetime.strptime(data['date'], "%Y-%m-%d")
  except ValueError:
    return jsonify({"message": "Invalid date format. Use YYYY-MM-DD"}), 400

  new_income = Income(name=data['name'],
                      amount=data['amount'],
                      date=date_obj,
                      property_id=data['property_id'],
                      extra=data['extra'])
  db.session.add(new_income)
  db.session.commit()

  return jsonify({"message": "Income added successfully!"})

@app.route('/api/income/delete/<int:income_id>', methods=['DELETE'])
@login_required
def remove_income(income_id):
  income_to_delete = Income.query.get(income_id)

  if not income_to_delete:
    return jsonify({"message": "Income not found"}), 404

  db.session.delete(income_to_delete)
  db.session.commit()

  return jsonify({"message": "Income removed successfully!"})

@app.route("/api/income/net")
def net_income():
    incomes = db.session.query(db.func.sum(Income.amount)).scalar()	
    expenses = db.session.query(db.func.sum(Expense.amount)).scalar()	
    net_income = incomes - expenses

    return jsonify({"income": incomes, "expenses": expenses, "net": net_income})


@app.route('/')
def home_ui():
  return render_template('index.html')

@app.route('/expenses', methods=['GET'])
@login_required
def list_expenses_ui():
  return render_template('list_expenses.html')

@app.route('/properties', methods=['GET'])
@login_required
def list_properties_ui():
  return render_template('list_properties.html')

@app.route('/income', methods=['GET'])
@login_required
def list_income_ui():
  return render_template('list_income.html')

@app.route('/income/add', methods=['GET'])
@login_required
def add_income_ui():
  return render_template('add_income.html')

@app.route('/properties/delete', methods=['GET'])
@login_required
def del_property_form():
  return render_template('delete_property.html')


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
def dashboard():
    properties = Property.query.all()  # Fetch properties from the database
    return render_template('dashboard.html', properties=properties)

@app.route('/expenses/add', methods=['GET'])
@login_required
def add_expense_ui():
  return render_template('add_expense.html')

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
      "status":
      "Running",
      "port":
      PORT,
      "endpoints": [
          "/api/login", "/api/logout", "/api/properties", "/api/expenses",
          "/api/income", "/api/<domain>/add/{id}", "/api/<domain>/delete/{id}"
      ],
      "domains": [
        "properties", "income", "expenses"
      ]
  }), 200

@app.route('/api/query/login', methods=["GET"])
@check_auth
def query_login():
  return render_template('index.html')

@app.route('/dashboard_test')
def test_dash():
  return render_template('dashboard_test.html')

app.run(debug=True, port=PORT, host="0.0.0.0")
