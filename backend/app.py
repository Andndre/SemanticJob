import os
import sqlite3
from flask import Flask, render_template, request, jsonify, g, session, redirect, url_for
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
load_dotenv()

from SPARQLWrapper import SPARQLWrapper, JSON
from save import search_and_store_jobs

# Konfigurasi aplikasi Flask
app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['DATABASE'] = os.path.join(os.getcwd(), 'users.db')
app.config['SECRET_KEY'] = os.urandom(24)

# Konfigurasi GraphDB
GRAPHDB_ENDPOINT = os.getenv("GRAPHDB_ENDPOINT") + '/repositories/lokerku'

def get_jobs():
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)
    query = """
    PREFIX ex: <http://example.org/ontology/>
    SELECT DISTINCT ?title ?salary ?companyName ?location ?source ?job_url WHERE {
        ?job a ex:Job ;
             ex:title ?title ;
             ex:salary ?salary ;
             ex:company ?company ;
             ex:source ?source ;
             ex:job_url ?job_url .
        ?company ex:name ?companyName ;
                 ex:location ?location .
    }
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    jobs = []
    for result in results["results"]["bindings"]:
        job = {
            "title": result["title"]["value"],
            "salary": result["salary"]["value"],
            "company": result["companyName"]["value"],
            "location": result["location"]["value"],
            "job_url": result["job_url"]["value"]
        }
        jobs.append(job)
        
    return jobs

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        db.commit()

def login_required(f):
    def wrap(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Unauthorized access"}), 401
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    hashed_password = generate_password_hash(password)
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 400

    return jsonify({"message": "User registered successfully"}), 201

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id, password FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()

    if user is None or not check_password_hash(user[1], password):
        return jsonify({"error": "Invalid username or password"}), 400

    session['user_id'] = user[0]
    return jsonify({"message": "Login successful"}), 200

@app.route("/api/logout", methods=["POST"])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logout successful"}), 200

@app.route("/api/user", methods=["GET"])
@login_required
def get_user_info():
    user_id = session['user_id']
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT username FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()

    if user is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"username": user[0]}), 200

@app.route("/api/jobs", methods=["GET"])
@login_required
def api_home():
    page = int(request.args.get("page", 1))
    total_per_page = int(request.args.get("total_per_page", 10))
    jobs = get_jobs()
    start = (page - 1) * total_per_page
    end = start + total_per_page
    paginated_jobs = jobs[start:end]
    return jsonify(paginated_jobs)

@app.route("/api/search", methods=["GET"])
@login_required
def api_search():
    keyword = request.args.get("keyword", "").strip()
    if keyword:
        jobs = search_and_store_jobs(keyword)
        return jsonify(jobs)
    else:
        return jsonify([])

@app.route("/", methods=["GET"])
def home():
    keyword = request.args.get("query", "").strip()
    if keyword:
        jobs = search_and_store_jobs(keyword)
    else:
        jobs = get_jobs()
    return render_template("index.html", jobs=jobs, keyword=keyword)

# Menjalankan aplikasi Flask
if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialized")
    print("Starting Flask app...")
    app.run(host='0.0.0.0', port=5000, debug=True)
    