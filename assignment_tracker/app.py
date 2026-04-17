import os
import sqlite3
from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

# create flask app and secret key
app = Flask(__name__)
app.secret_key = "dev-secret-key-change-later"

# goes and creates a path to our folder path with database file (extra precautain)
DATABASE = os.path.join(os.path.dirname(__file__), "database.db")


# helper function that opens connection and access via name
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # so we can access columns by name
    return conn

# main homepage
@app.route("/")
def index():


    if "user_id" not in session:
        return redirect("/login")

    # fetches the user in session
    db = get_db()
    user = db.execute(
        "SELECT username FROM users WHERE id = ?", (session["user_id"],)).fetchone()

    # safety check
    if user is None:
        db.close()
        session.clear()
        return redirect("/login")

    # fetches all assignment data ordering by due date 
    assignments = db.execute(
        "SELECT * FROM assignments WHERE user_id = ? ORDER BY due_date ASC",
        (session["user_id"],)).fetchall()
    db.close()

    # loads main page inputting users data
    return render_template("index.html", username=user["username"], assignments=assignments)


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # if any field is empty make user register again
        if not username or not password or not confirmation:
            flash("All fields are required.")
            return redirect("/register")


        if password != confirmation:
            flash("Passwords do not match.")
            return redirect("/register")

        # hash the password via werkzeug lib
        password_hash = generate_password_hash(password)

        db = get_db()

        # try to add user into database if doesnt exists
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

        # Check if user exists or passwords dont match 
        if user is None or not check_password_hash(user["password_hash"], password):
            flash("Invalid username or password.")
            return redirect("/login")

        # add user via their id to the session
        session["user_id"] = user["id"]
        flash("Logged in!")
        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():

    # clear session data
    session.clear()
    flash("You have been logged out.")
    return redirect("/login")


@app.route("/add", methods=["GET", "POST"])
def add():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        title = request.form.get("title")
        course = request.form.get("course")
        due_date = request.form.get("due_date")
        priority = request.form.get("priority")

        db = get_db()

        # add users assignment in database with respect to the session of user.
        db.execute(
            "INSERT INTO assignments (user_id, title, course, due_date, priority, completed) VALUES (?, ?, ?, ?, ?, 0)",
            (session["user_id"], title, course, due_date, priority)
        )
        db.commit()
        db.close()

        flash("Assignment added!")
        return redirect("/")

    return redirect("/")

# captures assignments int id as POST method
@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    if "user_id" not in session:
        return redirect("/login")
    db = get_db()

    # updates the users assignment via their id to become completed
    db.execute("UPDATE assignments SET completed = 1 WHERE id = ? AND user_id = ?",
               (id, session["user_id"]))
    db.commit()
    db.close()
    flash("Assignment marked as done!")
    return redirect("/")

# captures assingments int id as POST method
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    if "user_id" not in session:
        return redirect("/login")
    db = get_db()

    # delete the users assignment via their id
    db.execute("DELETE FROM assignments WHERE id = ? AND user_id = ?",
               (id, session["user_id"]))
    db.commit()
    db.close()
    flash("Assignment deleted.")
    return redirect("/")


@app.route("/timer")
def timer():
    if "user_id" not in session:
        return redirect("/login")
    db = get_db()

    # fetch users assignments to be displayed
    assignments = db.execute(
        "SELECT * FROM assignments WHERE user_id = ? AND completed = 0 ORDER BY due_date ASC",
        (session["user_id"],)
    ).fetchall()
    db.close()
    return render_template("timer.html", assignments=assignments)


# captures the same assignment id via POST method to log it
@app.route("/log_time/<int:id>", methods=["POST"])
def log_time(id):
    if "user_id" not in session:
        return redirect("/login")
    minutes = request.form.get("time_studied", 0)
    db = get_db()

    # updates users assignments time studied column 
    db.execute(
        "UPDATE assignments SET time_studied = time_studied + ? WHERE id = ? AND user_id = ?",
        (minutes, id, session["user_id"])
    )
    db.commit()
    db.close()
    flash("Time logged!")
    return redirect("/timer")


if __name__ == "__main__":
    app.run(debug=True)
