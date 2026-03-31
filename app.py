from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

# ✅ Fix database path for Render
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.db")


def init_db():
    conn = sqlite3.connect(db_path)
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

    conn = sqlite3.connect(db_path)
    conn.execute(
        "INSERT INTO contacts VALUES (?, ?, ?)",
        (name, email, message),
    )
    conn.commit()
    conn.close()

    return "Data Saved"

@app.route("/data")
def view_data():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts")
    data = cursor.fetchall()
    conn.close()

    return render_template("data.html", data=data)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)