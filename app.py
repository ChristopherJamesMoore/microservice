#importing frameworks
from flask import Flask, jsonify, request
from dotenv import load_dotenv
import pyodbc
import os
from functools import wraps

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database connection configuration
CONNECTION_STRING = (
    f"Driver={{ODBC Driver 17 for SQL Server}};"
    f"Server={os.getenv('DB_SERVER')};"
    f"Database={os.getenv('DB_NAME')};"
    f"UID={os.getenv('DB_USERNAME')};"
    f"PWD={os.getenv('DB_PASSWORD')};"
    "Encrypt=no;"
    "TrustServerCertificate=yes"
)

def get_db_connection():
    """Create and return a database connection"""
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        return conn
    except Exception as e:
        print(f"Database connection error: {str(e)}")
        return None

def handle_errors(f):
    """Decorator for handling common errors in routes"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(f"Error: {str(e)}")
            return jsonify({"error": "An error occurred."}), 500
    return wrapper

# Routes
@app.route('/trails', methods=['GET'])
@handle_errors
def get_trails():
    """Fetch all trails"""
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed."}), 500

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Trails")
    trails = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
    conn.close()
    return jsonify(trails)

@app.route('/trails', methods=['POST'])
@handle_errors
def add_trail():
    """Add a new trail"""
    data = request.json
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed."}), 500

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Trails (TrailName, TrailSummary, TrailDescription, Difficulty, Location, Length, ElevationGain) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        data['TrailName'], data['TrailSummary'], data['TrailDescription'], data['Difficulty'],
        data['Location'], data['Length'], data['ElevationGain']
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Trail added successfully."}), 201

@app.route('/routes', methods=['GET'])
@handle_errors
def get_routes():
    """Fetch all routes"""
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed."}), 500

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Routes")
    routes = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
    conn.close()
    return jsonify(routes)

@app.route('/trail-features', methods=['GET'])
@handle_errors
def get_trail_features():
    """Fetch all trail features"""
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed."}), 500

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TrailFeatures")
    features = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
    conn.close()
    return jsonify(features)

@app.route('/trail-feature-associations', methods=['GET'])
@handle_errors
def get_trail_feature_associations():
    """Fetch all trail-feature associations"""
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed."}), 500

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TrailFeatureAssociations")
    associations = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
    conn.close()
    return jsonify(associations)

if __name__ == '__main__':
    app.run(debug=True)