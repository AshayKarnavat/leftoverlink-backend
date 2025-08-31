# app.py

from flask import Flask  
from flask import jsonify
from flask import request
import sqlite3
from pathlib import Path
from flask_cors import CORS
import bcrypt
import os

app = Flask(__name__)   
CORS(app)

DB_PATH = Path(__file__).parent/"database.db" 

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # makes rows behave like dictionaries
    return conn


@app.route("/")         
def home():
    return "Hello, Ashay! This is your backend talking."  

@app.route("/bye")
def exit():
    return "Goodbye, Ashay! Server signing off!"

@app.route("/donations", methods=["GET","POST"])
def donations():

    if request.method == "GET":

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, food, quantity, location FROM donations")
        rows = cur.fetchall()
        
        donationslist = []
        for row in rows:
            donationslist.append({
                "id": row["id"],
                "food": row["food"],
                "quantity": row["quantity"],
                "location": row["location"]
            })
        
        conn.close()
        return jsonify(donationslist)

    if request.method == "POST":
        data = request.get_json()
        food = data.get("food")
        quantity = data.get("quantity")
        location = data.get("location")
        user_id = data.get("user_id")

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("INSERT INTO donations(food,quantity,location,user_id) VALUES(?,?,?,?)",(food,quantity,location,user_id)) 
        conn.commit()
        new_id = cur.lastrowid
        conn.close()

        return jsonify({
            "message":"donation added!",
            "donation":{
                "food":food,
                "quantity":quantity,
                "location":location,
                "id":new_id
            }
        }),201

@app.route("/donations/<int:donation_id>",methods=["DELETE"])
def deletedonations(donation_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM donations WHERE id = ?", (donation_id,))
    conn.commit()

    if cur.rowcount == 0:
        conn.close()
        return jsonify({"error": f"No donation with id {donation_id} found"}), 404

    conn.close()
    return jsonify({"message": f"Donation with id {donation_id} deleted!"})


@app.route("/donations/<int:donation_id>",methods=["PUT"])
def putdonations(donation_id):
    data = request.get_json()
    food = data.get("food")
    quantity = data.get("quantity")
    location = data.get("location")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE donations SET food = ?, quantity = ?, location = ? WHERE id = ?",(food,quantity,location,donation_id))
    conn.commit()
    if cur.rowcount == 0:
        conn.close()
        return jsonify({"error":f"donation with id {donation_id} doesn't exist!"}),404
    else:
        conn.close()
        return jsonify({"message":f"donation with id {donation_id} updated successfully!"}),200



@app.route("/users",methods=["GET","POST"])
def users() :
    if request.method == "GET":
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, username, email FROM users")
        rows = cur.fetchall()

        userslist = []

        for row in rows:
            userslist.append({
                "id": row["id"],
                "username": row["username"],
                "email": row["email"]
            })
        conn.close()
        return jsonify(userslist)
        

    
    if request.method == "POST":
        
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
        if cur.fetchone():
            conn.close()
            return jsonify({"error":"Username or email already exists"}), 409

        cur.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hashed_password))
        conn.commit()
        conn.close()
        return jsonify({"message": "User registered successfully!", "data": {"username": username, "email": email}}), 201
        

@app.route("/users/<int:user_id>",methods=["DELETE"])
def deleteusers(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()

    if cur.rowcount == 0:
        conn.close()
        return jsonify({"error": f"No user with id {user_id} found"}), 404

    conn.close()
    return jsonify({"message": f"user with id {user_id} deleted!"})
    

@app.route("/users/<int:user_id>",methods=["PUT"])
def putusers(user_id):
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET username = ?, email = ? WHERE id = ?",(username,email,user_id))
    conn.commit()
    if cur.rowcount == 0:
        conn.close()
        return jsonify({"error":f"user with id {user_id} doesn't exist!"}),404
    else:
        conn.close()
        return jsonify({"message":f"user with id {user_id} updated successfully!"}),200

@app.route('/login', methods=["POST"])
def login():

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id,password from users WHERE username = ?",(username,))
    user = cur.fetchone()

    if not user:
        conn.close()
        return jsonify({"error": "Invalid username or password"}), 401
    
    if bcrypt.checkpw(password.encode('utf-8'), user['password']):
        conn.close()
        return jsonify({"message": "Login successful!","user_id": user['id'],"username":username}), 200
    else:
        conn.close()
        print("Login failed: Incorrect password")
        return jsonify({"error": "Invalid username or password"}), 401
    

if __name__ == "__main__":
    app.run(debug=True)
