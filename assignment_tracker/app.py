import os
import sqlite3
from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-later"

DATABASE = os.path.join(os.path.dirname(__file__), "database.db")


def get_db():
    """Open a new database connection and return it."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # so we can access columns by name
    return conn


@app.route("/")
def index():
    # Lock down: redirect to login if not logged in
    if "user_id" not in session:
        return redirect("/login")

    db = get_db()
    user = db.execute("SELECT username FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    assignments = db.execute(
        "SELECT * FROM assignments WHERE user_id = ? ORDER BY due_date ASC",
        (session["user_id"],)
    ).fetchall()
    db.close()
    return render_template("index.html", username=user["username"], assignments=assignments)


@app.route("/add", methods=["POST"])
def add():
    if "user_id" not in session:
        return redirect("/login")

    title = request.form.get("title")
    course = request.form.get("course", "")
    due_date = request.form.get("due_date")
    priority = request.form.get("priority", "Medium")

    if not title or not due_date:
        flash("Title and due date are required.")
        return redirect("/")

    db = get_db()
    db.execute(
        "INSERT INTO assignments (user_id, title, course, due_date, priority) VALUES (?, ?, ?, ?, ?)",
        (session["user_id"], title, course, due_date, priority)
    )
    db.commit()
    db.close()

    flash("Assignment added!")
    return redirect("/")


@app.route("/update/<int:assignment_id>", methods=["POST"])
def update(assignment_id):
    if "user_id" not in session:
        return redirect("/login")

    db = get_db()
    db.execute(
        "UPDATE assignments SET completed = 1 WHERE id = ? AND user_id = ?",
        (assignment_id, session["user_id"])
    )
    db.commit()
    db.close()

    flash("Assignment marked as done!")
    return redirect("/")


@app.route("/delete/<int:assignment_id>", methods=["POST"])
def delete(assignment_id):
    if "user_id" not in session:
        return redirect("/login")

    db = get_db()
    db.execute(
        "DELETE FROM assignments WHERE id = ? AND user_id = ?",
        (assignment_id, session["user_id"])
    )
    db.commit()
    db.close()

    flash("Assignment deleted!")
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Basic validation
        if not username or not password or not confirmation:
            flash("All fields are required.")
            return redirect("/register")

        if password != confirmation:
            flash("Passwords do not match.")
            return redirect("/register")

        # Hash the password and insert the user
        password_hash = generate_password_hash(password)

        db = get_db()
        try:
            db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                       (username, password_hash))
            db.commit()
        except sqlite3.IntegrityError:
            flash("Username already exists.")
            db.close()
            return redirect("/register")
        db.close()

        flash("Registration successful! Please log in.")
        return redirect("/login")

    # GET request — show the form
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Username and password are required.")
            return redirect("/login")

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        db.close()

        if user is None or not check_password_hash(user["password_hash"], password):
            flash("Invalid username or password.")
            return redirect("/login")

        # Store user ID in the session
        session["user_id"] = user["id"]
        flash("Logged in!")
        return redirect("/")

    # GET request — show the form
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
