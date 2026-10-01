from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def get_db():
    return sqlite3.connect("posts.db")


# Create table
def create_table():
    db = get_db()

    db.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)

    db.commit()
    db.close()


# Show posts
@app.route("/run")
def home():

    db = get_db()

    posts = db.execute(
        "SELECT * FROM posts"
    ).fetchall()

    db.close()

    return render_template("review.html", posts=posts)


@app.route("/")
def index():
    return render_template("index.html")


# Add post
@app.route("/add", methods=["POST"])
def add_post():

    title = request.form["title"]
    content = request.form["content"]

    db = get_db()

    db.execute(
        "INSERT INTO posts (title, content) VALUES (?, ?)",
        (title, content)
    )

    db.commit()
    db.close()

    return redirect("/")


if __name__ == "__main__":
    create_table()
    app.run(debug=True)