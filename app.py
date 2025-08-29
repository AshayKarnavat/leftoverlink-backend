# app.py

from flask import Flask  
from flask import jsonify
from flask import request
import sqlite3
from pathlib import Path
from flask_cors import CORS

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

        data = request.get_json()  # 1. read JSON from frontend
        food = data.get("food")
        quantity = data.get("quantity")
        location = data.get("location")
        user_id = data.get("user_id")

        conn = get_db_connection()          # 2. open database
        cur = conn.cursor()                 # 3. get cursor

        cur.execute(
            "INSERT INTO donations (food, quantity, location,user_id) VALUES (?, ?, ?,?)",
            (food, quantity, location,user_id)
        )                                   # 4. insert new donation
        conn.commit()                        # 5. save changes
        conn.close()                         # 6. close database

        return jsonify({"donation": data, "message": "Donation added!", "redirect_url":"/"})
    

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

        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT id FROM users WHERE username = ?",(username,))
        if cur.fetchone():
            conn.close()
            return jsonify({"error":"username already exists"})
        
        cur.execute("SELECT id FROM users WHERE email = ?",(email,))
        if cur.fetchone():
            conn.close()
            return jsonify({"error":"email already exists"})

        cur.execute("INSERT INTO users (username, email) VALUES (?, ?)", (username, email))
        conn.commit()
        conn.close()
        return jsonify({"message": "user added", "data": {"username": username, "email": email}})
        

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

if __name__ == "__main__":   
    app.run(debug=True)
    
