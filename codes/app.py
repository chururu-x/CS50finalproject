import os
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, sgd

# configure application
app = Flask(__name__)

# custom SGD filter
app.jinja_env.filters["sgd"] = sgd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///pole.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cart", methods=["GET", "POST"])
@login_required
def cart():
    # Ensure cart exists
    if "cart" not in session:
        session["cart"] = []

    # POST
    if request.method == "POST":
        # adds selected class to cart
        option = request.form.get("option")
        if option:
            session["cart"].append(option)
        # removes class from cart
        else:
            class_id = request.form.get("remove")
            if class_id:
                session["cart"].remove(class_id)
        return redirect("/cart")

    # GET
    if len(session["cart"]) == 1:
        items = db.execute("SELECT timings.id, class, timing, price FROM timings JOIN classes ON timings.class_id = classes.id WHERE timings.id = (?)", session["cart"])
    else:
        items = db.execute("SELECT timings.id, class, timing, price FROM timings JOIN classes ON timings.class_id = classes.id WHERE timings.id IN (?)", session["cart"])

    # calculate total price
    total_price = 0
    for i in range(len(items)):
        total_price += int(items[i]["price"])
    # print = (session["cart"])
    return render_template("cart.html", items=items, total_price=total_price, print=print)


@app.route("/classes", methods=["GET"])
def classes():
    return render_template("classes.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email"):
            return apology("must provide email", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for email
        rows = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid email and/or password", 403)

        # Remember which user has logged in. "rows[0]" bcos query should return only one row of data that matches user-id
        session["user_id"] = rows[0]["id"]

        # Redirect user to their classes
        return redirect("/your-reservations")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/contemporary-3", methods=["GET"])
@login_required
def contemporary_3():
    # queries timings of class_id WHERE class is 'Tricks 1'
    rows = db.execute("SELECT * FROM timings WHERE class_id IN (SELECT id FROM classes WHERE class = ?)", ('Contemporary Level 3',))
    return render_template("/contemporary-3.html", rows=rows)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Ensures first name and last name field are not blank
        first_name = request.form.get("firstname")
        last_name = request.form.get("lastname")
        if not first_name or not last_name:
            return apology("First name and last name required", 400)

        # Ensures email field isn't blank
        email = request.form.get("email")
        if not email:
            return apology("Email required", 400)

        # Validates email format
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            return apology("Invalid email format", 400)

        # Ensures email isn't taken
        rows = db.execute("SELECT * FROM users WHERE email = ?", email)
        if len(rows) > 0 and rows[0]["email"] == email:
            return apology("Email taken. Please use another email.", 400)

        # ensures that pw matches
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if password != confirmation or not password or not confirmation:
            return apology("Passwords do not match", 400)

        # hash pw
        hashed_pw = generate_password_hash(password)

        # store all field values in db (users)
        db.execute("INSERT INTO users(first_name, last_name, email, hash) VALUES(?, ?, ?, ?)", first_name, last_name, email, hashed_pw)

        # log user in and redirect to home page
        new_id = db.execute("SELECT * FROM users WHERE email = ?", email)
        session["user_id"] = new_id[0]["id"]
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/reviews", methods=["GET", "POST"])
def reviews():
    # display all existing reviews
    reviews = db.execute("SELECT name, review, rating FROM reviews")

    # display the average review rating
    rating_sum = 0
    n = len(reviews)
    for i in range(n):
        rating_sum += int(reviews[i]["rating"])
    average = round(rating_sum / n, 1)

    # POST -- store data submitted into DB
    if request.method == "POST":
        name = request.form.get("name")
        review = request.form["review"]
        rating = request.form.get("rating")

        # Store the review in the database
        db.execute("INSERT INTO reviews (name, review, rating) VALUES (?, ?, ?)", name, review, rating)

        # Retrieve all reviews from the database
        return redirect("/reviews")

    else:
        return render_template("reviews.html", reviews=reviews, average=average)


@app.route("/success", methods=["POST"])
@login_required
def success():
    # returns apology if cart is empty
    if session["cart"] == []:
        return apology("Cart cannot be empty", 400)

    # obtain timings_ids from sessions["cart"]
    else:
        for i in range(len(session["cart"])):
            # find corresponding class_id
            timing_id = session["cart"][i]
            rows = db.execute("SELECT classes.id AS class_id FROM classes JOIN timings ON timings.class_id = classes.id WHERE timings.id = (?)", timing_id)
            class_id = int(rows[0]["class_id"])
            # insert timing_id and class_id into bookings table
            db.execute("INSERT INTO bookings(timing_id, user_id, class_id) VALUES(?, ?, ?)", timing_id, session["user_id"], class_id)

            # get current booking count of the class, add 1 to it and update table with new booking count
            list = db.execute("SELECT * FROM timings WHERE id =(?)", timing_id)
            booking_count = list[0]["booking_count"] + 1
            db.execute("UPDATE timings SET booking_count = (?) WHERE id = (?)", booking_count, timing_id)


        #empty cart
        session["cart"] = []

        return render_template("success.html")


@app.route("/tricks-1", methods=["GET"])
@login_required
def tricks_1():
    # queries timings of class_id WHERE class is 'Tricks 1'
    rows = db.execute("SELECT * FROM timings WHERE class_id IN (SELECT id FROM classes WHERE class = ?)", ('Tricks Level 1',))
    return render_template("/tricks-1.html", rows=rows)


@app.route("/tricks-2", methods=["GET"])
@login_required
def tricks_2():
    # queries timings of class_id WHERE class is 'Tricks 1'
    rows = db.execute("SELECT * FROM timings WHERE class_id IN (SELECT id FROM classes WHERE class = ?)", ('Tricks Level 2',))
    return render_template("/tricks-2.html", rows=rows)


@app.route("/your-reservations", methods=["GET"])
@login_required
def your_bookings():
    # show list of booked classes
    bookings = db.execute("SELECT class, timing, term, year FROM bookings JOIN classes ON bookings.class_id = classes.id JOIN timings ON timings.id = bookings.timing_id WHERE user_id = (?)", session["user_id"])
    return render_template("/your-reservations.html", bookings=bookings)


