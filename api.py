from flask import Flask, request, jsonify
import sqlite3
from datetime import date

app = Flask(__name__)
DB = "db.sqlite3"

# ---------- DB CONNECT ----------
def db():
    return sqlite3.connect(DB)

# ---------- REGISTER + REFERRAL ----------
@app.route("/register", methods=["POST"])
def register():
    d = request.json
    conn = db()
    c = conn.cursor()

    c.execute(
        "INSERT OR IGNORE INTO users(id,name,balance) VALUES (?,?,0)",
        (d["id"], d["name"])
    )

    if "ref" in d and d["ref"]:
        c.execute(
            "INSERT OR IGNORE INTO referrals(referrer,referred) VALUES (?,?)",
            (d["ref"], d["id"])
        )
        c.execute(
            "UPDATE users SET balance=balance+5 WHERE id=?",
            (d["ref"],)
        )

    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

# ---------- TASK LIST ----------
@app.route("/tasks")
def tasks():
    conn = db()
    c = conn.cursor()
    c.execute("SELECT id,title,reward,type FROM tasks")
    data = c.fetchall()
    conn.close()
    return jsonify(data)

# ---------- SUBMIT TASK (DAILY LIMIT) ----------
@app.route("/submit-task", methods=["POST"])
def submit_task():
    d = request.json
    today = str(date.today())

    conn = db()
    c = conn.cursor()

    c.execute("""
        SELECT 1 FROM daily_tasks
        WHERE user_id=? AND task_id=? AND date=?
    """, (d["user_id"], d["task_id"], today))

    if c.fetchone():
        conn.close()
        return jsonify({"error": "Daily limit reached"}), 400

    c.execute(
        "INSERT INTO task_submissions(user_id,task_id,status) VALUES (?,?,?)",
        (d["user_id"], d["task_id"], "pending")
    )
    c.execute(
        "INSERT INTO daily_tasks(user_id,task_id,date) VALUES (?,?,?)",
        (d["user_id"], d["task_id"], today)
    )

    conn.commit()
    conn.close()
    return jsonify({"status": "submitted"})

# ---------- WITHDRAW ----------
@app.route("/withdraw", methods=["POST"])
def withdraw():
    d = request.json
    if d["amount"] < 500:
        return jsonify({"error": "Minimum withdraw 500"}), 400

    conn = db()
    c = conn.cursor()
    c.execute(
        "INSERT INTO withdraws(user_id,amount,method,number,status) VALUES (?,?,?,?,?)",
        (d["user_id"], d["amount"], d["method"], d["number"], "pending")
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "pending"})

# ================= ADMIN APIs =================

# ---------- PENDING TASKS ----------
@app.route("/admin/pending-tasks")
def pending_tasks():
    conn = db()
    c = conn.cursor()
    c.execute("""
        SELECT ts.id, u.name, t.title, t.reward
        FROM task_submissions ts
        JOIN users u ON ts.user_id=u.id
        JOIN tasks t ON ts.task_id=t.id
        WHERE ts.status='pending'
    """)
    data = c.fetchall()
    conn.close()
    return jsonify(data)

# ---------- APPROVE TASK ----------
@app.route("/admin/approve-task/<int:id>")
def approve_task(id):
    conn = db()
    c = conn.cursor()

    c.execute(
        "SELECT user_id, task_id FROM task_submissions WHERE id=?",
        (id,)
    )
    row = c.fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "Not found"}), 404

    user_id, task_id = row
    c.execute("SELECT reward FROM tasks WHERE id=?", (task_id,))
    reward = c.fetchone()[0]

    c.execute(
        "UPDATE users SET balance=balance+? WHERE id=?",
        (reward, user_id)
    )
    c.execute(
        "UPDATE task_submissions SET status='approved' WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()
    return jsonify({"status": "approved"})

# ---------- PENDING WITHDRAW ----------
@app.route("/admin/pending-withdraw")
def pending_withdraw():
    conn = db()
    c = conn.cursor()
    c.execute("""
        SELECT w.id, u.name, w.amount, w.method, w.number
        FROM withdraws w
        JOIN users u ON w.user_id=u.id
        WHERE w.status='pending'
    """)
    data = c.fetchall()
    conn.close()
    return jsonify(data)

# ---------- APPROVE WITHDRAW ----------
@app.route("/admin/approve-withdraw/<int:id>")
def approve_withdraw(id):
    conn = db()
    c = conn.cursor()

    c.execute(
        "SELECT user_id, amount FROM withdraws WHERE id=?",
        (id,)
    )
    row = c.fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "Not found"}), 404

    user_id, amount = row

    c.execute(
        "UPDATE users SET balance=balance-? WHERE id=?",
        (amount, user_id)
    )
    c.execute(
        "UPDATE withdraws SET status='paid' WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()
    return jsonify({"status": "paid"})

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
