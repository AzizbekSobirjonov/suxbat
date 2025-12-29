from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    return sqlite3.connect("database.db")

# DB init
with get_db() as db:
    db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS messages(
            id INTEGER PRIMARY KEY,
            username TEXT,
            text TEXT
        )
    """)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (u, p)
        ).fetchone()

        if user:
            session["user"] = u
            return redirect("/chat")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        try:
            db = get_db()
            db.execute(
                "INSERT INTO users(username, password) VALUES (?,?)",
                (u, p)
            )
            db.commit()
            return redirect("/")
        except:
            pass

    return render_template("register.html")

@app.route("/chat")
def chat():
    if "user" not in session:
        return redirect("/")
    return render_template("chat.html")

@app.route("/send", methods=["POST"])
def send():
    if "user" not in session:
        return ""

    msg = request.form["message"]

    db = get_db()
    db.execute(
        "INSERT INTO messages(username, text) VALUES (?,?)",
        (session["user"], msg)
    )
    db.commit()

    return ""

@app.route("/messages")
def messages():
    db = get_db()
    msgs = db.execute(
        "SELECT username, text FROM messages"
    ).fetchall()

    return jsonify(msgs)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
