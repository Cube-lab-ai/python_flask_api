from flask import Flask, jsonify, request
from mysql.connector import Error
import mysql.connector


app = Flask(__name__)


# 🧩 Long Answer (How It REALLY Works)

# 1️⃣ This line is the key
# @app.route("/", methods=["GET"])

# This is called a decorator.
# It tells Flask:
# “When someone sends a GET request to /, call the function below it.”

# 🔹 request.args
# In Flask, request represents the incoming HTTP request.
# request.args is a dictionary-like object that contains all the query parameters sent in the URL for GET requests.
# request.args = {
#     "name1": "Alice",
#     "age": "25"
# }

# 3️⃣ request.args is built
# Flask takes the query string:
# name1=Alice&age=25

# and turns it into a dictionary-like object:
# request.args = {
#     "name1": "Alice",
#     "age": "25"
# }

# Technically, request.args is a werkzeug.datastructures.ImmutableMultiDict, which behaves like a Python dictionary.
# You can access parameters using:
# name1 = request.args.get("name1")   # returns "Alice"
# age   = request.args.get("age")     # returns "25"

# If a parameter is not present, get() returns None (or a default if you specify it):
# country = request.args.get("country", "Unknown")  # returns "Unknown"

# 1️⃣ Parameter (in Flask / URL)
# Think of parameters as the names in the URL query string — the data that the client (browser or Postman) sends to your API.

# Example URL:
# http://127.0.0.1:5000/api/hello?name1=Alice&country=USA


# Here:
# Parameter	Value
# name1	Alice
# country	USA

# name1 and country are parameters.
# They are sent by the client as part of the URL.

# 2️⃣ Argument (in Python function)
# An argument is the value you pass into a function when calling it.

# Example:
# country = request.args.get("country", "Unknown")
# "country" → the parameter you are trying to look up in request.args
# "Unknown" → the argument to the .get() function. It tells .get(): “If the parameter doesn’t exist, return this value.”

# | Concept   | In code     | In URL / request                       |
# | --------- | ----------- | -------------------------------------- |
# | Parameter | `"country"` | client may send `?country=USA`         |
# | Argument  | `"Unknown"` | fallback value if parameter is missing |


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message" : "Hello world"})

@app.route("/api/finacle", methods=["GET"])
def helloworldfromfinalce():
    return jsonify({"message" : "hello from finacle"})

@app.route("/api/hello", methods=["GET"])
def hello():
    name1 = request.args.get("name1")
    return jsonify({"return name" : f"hello {name1}"})

@app.route("/api/getdatafromfinacle", methods=["GET"])
def getfinalcedata():
    namefinalce = request.args.get("finalename" , "infosys private limited")
    return jsonify({"message" : f"gotten data from finacle {namefinalce}"})

@app.route("/api/getandreturnname", methods=["GET"])
def getandreturnname():
    name = request.args.get("name")
    return jsonify({"message" : f"hello {name}"})   

@app.route("/api/getdata", methods=['GET'])
def callgetdata():
    data = request.args.get("hello")
    return jsonify({"hello" : data})

@app.route("/api/getpostdata", methods=["POST"])
def getdate():
    data = request.get_json()
    return jsonify({"data" : data})

@app.route("/api/getpaymentdata", methods=['GET'])
def callgetpaymentdata():
    return jsonify({"return" : "world"})

# 1️⃣ URL Parameters (Path Variables)
# Instead of query strings:
@app.route("/api/user/<username>", methods=["GET"])
def get_user(username):
    return jsonify({"user": username})


@app.route("/api/getuser/<username>", methods=["GET"])
def getusername(username):
    return jsonify({"user" : username})

# 2️⃣ Input Validation & Error Handling
# Right now, if name is missing, you return:

@app.route("/api/requestname", methods=["GET"])
def requestname():
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "name is required"}), 400
    return jsonify({"message": f"hello {name}"})

    
#  http://localhost:5000/api/getname/
# Flask sees no <nameed> value, so it does not call your function.
# Flask immediately returns 404 Not Found.
# Your if not nameed: check never runs, because the function is never entered.

@app.route("/api/getname/<nameed>", methods=["GET"])
def name(nameed):
    if not nameed:
        return jsonify({"status" : "0", "message" : "no data found"}), 400
    return jsonify({"status" : 1})

# mysql 

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          # XAMPP default
            password="",          # Usually empty for XAMPP root
            database="testdb"     # Your database name
        )
        return connection
    except Error as e:
        print("Database connection error:", e)
        return None

@app.route("/api/user", methods=["POST"])
def create_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "name and email required"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB connection failed"}), 500

    cursor = conn.cursor()
    query = "INSERT INTO users (name, email) VALUES (%s, %s)"
    cursor.execute(query, (name, email))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"status": "success", "message": "User created"})

if __name__ == "__main__":
    app.run(debug=True)

#