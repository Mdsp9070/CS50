import os

from datetime import date
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Query infos from database
    rows = db.execute("SELECT * FROM buy WHERE user_id = :user",
                      user=session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = :user",
                      user=session["user_id"])[0]['cash']

    # pass a list of lists to the template page, template is going to iterate it to extract the data into a table
    total = cash
    stocks = []
    for index, row in enumerate(rows):
        stock_info = lookup(row['symbol'])

        # create a list with all the info about the stock and append it to a list of every stock owned by the user
        stocks.append(list((stock_info['symbol'], stock_info['name'], row['number'],
                            stock_info['price'], round(stock_info['price'] * row['number'], 2))))
        total += stocks[index][4]

    return render_template("index.html", stocks=stocks, cash=round(cash, 2), total=round(total, 2))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buys shares of stocks"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Obtain the data necessary for the transaction
        share = int(request.form.get("share"))
        symbol = lookup(request.form.get("symbol"))['symbol']

        # Control if the stock symbol is valid
        if not lookup(symbol):
            return apology("Could not find the stock")

        # Calculate total value of the transaction
        price = lookup(symbol)['price']
        cash = db.execute("SELECT cash FROM users WHERE id = :user",
                          user=session["user_id"])[0]['cash']
        cash_after = cash - price * float(share)

        # Check if current cash is enough for transaction
        if cash_after < 0:
            return apology("You don't have enough money for this transaction")

        # Check if user already has one or more stocks from the same company
        stock = db.execute("SELECT number FROM buy WHERE user_id = :user AND symbol = :symbol",
                           user=session["user_id"], symbol=symbol)

        # Insert new row into the stock table
        if not stock:
            db.execute("INSERT INTO buy(user_id, symbol, number) VALUES (:user, :symbol, :amount)",
                       user=session["user_id"], symbol=symbol, amount=share)

        # update row into the stock table
        else:
            share += stock[0]['number']

            db.execute("UPDATE buy SET number = :number WHERE user_id = :user AND symbol = :symbol",
                       user=session["user_id"], symbol=symbol, amount=share)

        # update user's cash
        db.execute("UPDATE users SET cash = :cash WHERE id = :user",
                   cash=cash_after, user=session["user_id"])

        # Update history table
        db.execute("INSERT INTO transactions(user_id, symbol, amount, value) VALUES (:user, :symbol, :amount, :value)",
                   user=session["user_id"], symbol=symbol, amount=share, value=round(price*float(share)))

        # Redirect user to index page with a success message
        flash("Bought!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # query database with the transactions history
    rows = db.execute("SELECT * FROM transactions WHERE user_id = :user",
                      user=session["user_id"])

    # pass a list of lists to the template page, template is going to iterate it to extract the data into a table
    transactions = []
    for row in rows:
        stock_info = lookup(row['symbol'])

        # create a list with all the info about the transaction and append it to a list of every stock transaction
        transactions.append(list(
            (stock_info['symbol'], stock_info['name'], row['amount'], row['value'], date.today())))

    # redirect user to index page
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    if request.method == "POST":
        if request.form.get("password") != request.form.get("password2"):
            return apology("New passwords must be the same")
        pass_after = generate_password_hash(request.form.get("password"))
        db.execute("UPDATE users SET hash = :hash WHERE id = :user_id", hash=pass_after, user_id=session["user_id"])
        return redirect("/")
    else:
        return render_template("change.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        if not request.form.get("quote"):
            return apology("Must provide a quote to search!")

        row = lookup(request.form.get("quote"))

        if row != None:
            return render_template("price.html", row=row)
        else:
            return apology("Must provide a valid symbol!")
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        if request.form.get('password') != request.form.get('password2'):
            return apology("Passwords don't match!")
        row = db.execute("SELECT * FROM users WHERE username = :username",
                         username=request.form.get("username"))

        if len(row) == 1:
            return apology("Username already exist :/")

        db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=request.form.get(
            "username"), hash=(generate_password_hash(request.form.get("password"))))

        flash("Password changed!")
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # collect relevant informations
        amount = int(request.form.get("amount"))
        symbol = request.form.get("symbol")
        price = lookup(symbol)["price"]
        value = round(price*float(amount))

        # Update stocks table
        amount_before = db.execute("SELECT number FROM buy WHERE user_id = :user AND symbol = :symbol",
                                   symbol=symbol, user=session["user_id"])[0]['number']
        amount_after = amount_before - amount

        # delete stock from table if we sold every unit we had
        if amount_after == 0:
            db.execute("DELETE FROM buy WHERE user_id = :user AND symbol = :symbol",
                       symbol=symbol, user=session["user_id"])

        # stop the transaction if the user does not have enough stocks
        elif amount_after < 0:
            return apology("That's more than the stocks you own")

        # otherwise update with new value
        else:
            db.execute("UPDATE buy SET number = :amount WHERE user_id = :user AND symbol = :symbol",
                       symbol=symbol, user=session["user_id"], amount=amount_after)

        # calculate and update user's cash
        cash = db.execute("SELECT cash FROM users WHERE id = :user",
                          user=session["user_id"])[0]['cash']
        cash_after = cash + price * float(amount)

        db.execute("UPDATE users SET cash = :cash WHERE id = :user",
                   cash=cash_after, user=session["user_id"])

        # Update history table
        db.execute("INSERT INTO transactions(user_id, symbol, amount, value) VALUES (:user, :symbol, :amount, :value)",
                   user=session["user_id"], symbol=symbol, amount=-amount, value=value)

        # Redirect user to home page with success message
        flash("Sold!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # query database with the transactions history
        rows = db.execute("SELECT symbol, number FROM buy WHERE user_id = :user",
                          user=session["user_id"])

        # create a dictionary with the availability of the stocks
        stocks = {}
        for row in rows:
            stocks[row['symbol']] = row['number']

        return render_template("sell.html", stocks=stocks)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
