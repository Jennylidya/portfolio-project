from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS contacts (name TEXT, email TEXT, message TEXT)"
    )
    conn.close()

init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    conn = sqlite3.connect("database.db")
    conn.execute(
        "INSERT INTO contacts VALUES (?, ?, ?)",
        (name, email, message),
    )
    conn.commit()
    conn.close()

    return "Data Saved"


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)