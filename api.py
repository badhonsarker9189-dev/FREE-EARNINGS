from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def db():
    return sqlite3.connect("db.sqlite3")

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    conn = db()
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users(id,name) VALUES (?,?)",
              (data["id"], data["name"]))
    conn.commit()
    conn.close()
    return jsonify({"status":"ok"})

@app.route("/tasks")
def tasks():
    conn = db()
    c = conn.cursor()
    c.execute("SELECT id,title,reward,type FROM tasks")
    data = c.fetchall()
    conn.close()
    return jsonify(data)

@app.route("/submit-task", methods=["POST"])
def submit_task():
    data = request.json
    conn = db()
    c = conn.cursor()
    c.execute("INSERT INTO task_submissions(user_id,task_id) VALUES (?,?)",
              (data["user_id"], data["task_id"]))
    conn.commit()
    conn.close()
    return jsonify({"status":"submitted"})

@app.route("/withdraw", methods=["POST"])
def withdraw():
    d = request.json
    if d["amount"] < 500:
        return jsonify({"error":"Minimum 500"}),400
    conn = db()
    c = conn.cursor()
    c.execute("INSERT INTO withdraws(user_id,amount,method,number) VALUES (?,?,?,?)",
              (d["user_id"], d["amount"], d["method"], d["number"]))
    conn.commit()
    conn.close()
    return jsonify({"status":"pending"})

if __name__ == "__main__":
    app.run(port=5000)
