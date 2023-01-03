import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, flash
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""
    # User reached route via GET
    if request.method == "GET":

        # Get id of current user
        user_id = session["user_id"]

        # Get username and cash of current user
        current_user = db.execute("SELECT username, cash FROM users WHERE id = ?", user_id)
        username = current_user[0]["username"]
        cash = current_user[0]["cash"]

        # Get all of the current user's transactions
        transactions = db.execute("""SELECT symbol, name, SUM(shares) AS shares FROM transactions WHERE username = ?
        GROUP BY symbol HAVING SUM(shares) > 0""", username)

        return render_template("index.html", transactions=transactions, cash=cash, usd=usd, lookup=lookup)

    # User reached route via POST (as by submitting a form via POST)
    else:

        # User presses the "BUY" button next to specific holding
        if request.form["action"] == "Buy":

            # Get id of current user
            user_id = session["user_id"]

            # Get username and cash of current user
            current_user = db.execute("SELECT username, cash FROM users WHERE id = ?", user_id)
            cash = current_user[0]["cash"]

            # Hidden form with default value of the chosen stock symbol
            symbol = request.form.get("symbol")

            # Returns dictionary with stock info (name, price, symbol)
            stock = lookup(symbol)

            name = stock["name"]
            price = stock["price"]

            return render_template("buy.html", symbol=symbol, name=name, price=price, cash=cash)

        # User presses the "SELL" button next to specific holding
        if request.form["action"] == "Sell":

            # Get id of current user
            user_id = session["user_id"]

            # Get username and cash of current user
            current_user = db.execute("SELECT username, cash FROM users WHERE id = ?", user_id)
            cash = current_user[0]["cash"]

            # Hidden form with default value of the chosen stock symbol
            symbol = request.form.get("symbol")

            # Returns dictionary with stock info (name, price, symbol)
            stock = lookup(symbol)

            name = stock["name"]
            shares = db.execute("SELECT SUM(shares) AS shares FROM transactions WHERE symbol = ?", symbol)[0]["shares"]

            return render_template("sell.html", symbol=symbol, name=name, shares=shares, cash=cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via GET
    if request.method == "GET":

        user_id = session["user_id"]
        current_user = db.execute("SELECT username, cash FROM users WHERE id = ?", user_id)
        cash = current_user[0]["cash"]

        return render_template("buy.html", cash=cash)

    # User reached route via POST (as by submitting a form via POST)
    else:
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Ensure symbol was provided
        if not symbol:
            return apology("Please provide stock symbol")

        # Returns dictionary with stock info (name, price, symbol)
        stock = lookup(symbol)

        # Ensure valid stock symbol was provided
        if stock == None:
            return apology("Invalid stock symbol")

        # Convert number of shares from string to positive int
        try:
            shares = int(shares)
            # Checks for negative number of shares
            if shares < 1:
                return apology("Please provide positive number of shares")
        # Handles non-numeric inputs
        except:
            return apology("Please provide number of shares")

        # Get value of the transaction
        value = shares * stock["price"]

        # Finds current user
        user_id = session["user_id"]

        # Find the current user in database
        current_user = db.execute("SELECT * FROM users WHERE id = ?", user_id)

        # Checks user balance
        cash = current_user[0]["cash"]

        # Checks if user has enough money to make a purchase
        if cash < value:
            return apology("Not enough money")

        # Updates the user cash after purchase
        updated_cash = cash - value
        db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash, user_id)

        # Get the date of the transaction
        date = datetime.now()

        # Action is always buy in here
        action = "buy"

        # Insert data to transactions database
        db.execute("""INSERT INTO transactions (username, action, symbol, name, shares, price, value, date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", current_user[0]["username"], action, symbol.upper(), stock["name"], shares, stock["price"], value, date)

        # Redirect back to user's portfolio after succesful buy with a flash message
        flash(f"You have succesfully bought {shares} shares of {stock['name']} for {usd(value)}!")
        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Finds current user
    user_id = session["user_id"]

    # Finds userame
    current_user = db.execute("""SELECT username, cash FROM users
    WHERE id = ?""", user_id)

    username = current_user[0]["username"]
    cash = current_user[0]["cash"]

    # Finds all transactions of the current user
    transactions = db.execute("""SELECT name, symbol, action, shares, price, value, date FROM transactions
    WHERE username = ?""", username)

    return render_template("history.html", transactions=transactions, cash=cash)


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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

    # User reached route via GET
    if request.method == "GET":
        return render_template("quote.html")

    # User reached route via POST (as by submitting a form via POST)
    else:
        symbol = request.form.get("symbol")

        # Ensure symbol was provided
        if not symbol:
            return apology("Please provide stock symbol")

        # Returns dictionary with stock info (name, price, symbol)
        stock = lookup(symbol.upper())

        # Ensure valid stock symbol was provided
        if stock == None:
            return apology("Invalid stock symbol")

        return render_template("quoted.html", name=stock["name"], price=stock["price"], symbol=stock["symbol"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via GET
    if request.method == "GET":
        return render_template("register.html")

    # User reached route via POST (as by submitting a form via POST)
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("Must provide username")

        # Ensure password was submitted
        if not password:
            return apology("Must provide password")

        # Ensure confirmation of password was submitted
        if not confirmation:
            return apology("Must confirm password")

        # Check the password match the confirmation
        if password != confirmation:
            return apology("Confirmation does not match the password")

        # Store provided password
        hash = generate_password_hash(password)

        try:
            # Add new user to database
            new_user = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)
        except:
            # Return an apology if the user with the same name already exists
            return apology("Username already exists")

        # Remember which user has logged in
        session["user_id"] = new_user

        # Redirect user to home page
        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via GET
    if request.method == "GET":
        user_id = session["user_id"]

        # Get username of current user
        current_user = db.execute("""SELECT username, cash FROM users
        WHERE id = ?""", user_id)

        username = current_user[0]["username"]

        cash = current_user[0]["cash"]

        user_portfolio = db.execute("""SELECT symbol FROM transactions
        WHERE username = ? GROUP BY symbol HAVING SUM(shares) > 0""", username)

        return render_template("sell.html", portfolio=user_portfolio, cash=cash)

    # User reached route via POST (as by submitting a form via POST)
    else:
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Ensure symbol was provided
        if not symbol:
            return apology("Please provide stock symbol")

        # Returns dictionary with stock info (name, price, symbol)
        stock = lookup(symbol.upper())

        # Ensure valid stock symbol was provided
        if stock == None:
            return apology("Invalid stock symbol")

        # Convert number of shares from string to positive int
        try:
            shares = int(shares)
            # Checks for negative number of shares
            if shares < 1:
                return apology("Please provide positive number of shares")
        # Handles non-numeric inputs
        except:
            return apology("Please provide number of shares")

        # Finds current user
        user_id = session["user_id"]

        # Finds userame
        current_user = db.execute("SELECT username, cash FROM users WHERE id = ?", user_id)
        username = current_user[0]["username"]

        # Checks if the user has enough shares to sell
        user_shares = db.execute("""SELECT SUM(shares) AS shares FROM transactions
        WHERE username = ? AND symbol = ?""", username, symbol)

        if user_shares[0]["shares"] < shares:
            return apology("Not enoug shares to sell")

        # Get value of the transaction
        value = shares * stock["price"]

        # Find the current user in database
        current_user = db.execute("SELECT * FROM users WHERE id = ?", user_id)

        # Checks user balance
        cash = current_user[0]["cash"]

        # Updates the user cash after purchase
        updated_cash = cash + value
        db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash, user_id)

        # Get the date of the transaction
        date = datetime.now()

        # Action is always sell in here
        action = "sell"

        # Insert data to transactions database
        db.execute("""INSERT INTO transactions (username, action, symbol, name, shares, price, value, date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", current_user[0]["username"], action, symbol.upper(), stock["name"], shares*(-1), stock["price"], value, date)

        # Redirect back to user's portfolio after succesful buy with a flash message
        flash(f"You have succesfully sold {shares} shares of {stock['name']} for {usd(value)}!")
        return redirect("/")


@app.route("/manage", methods=["GET", "POST"])
def manage():
    """Manage account"""

    # User reached route via GET
    if request.method == "GET":

        # Get current user id
        user_id = session["user_id"]

        # Get cash of current user
        current_user = db.execute("SELECT username, cash FROM users WHERE id = ?", user_id)
        cash = current_user[0]["cash"]

        return render_template("manage.html", cash=cash)

    # User reached route via POST (as by submitting a form via POST)
    else:

        # User wants to deposit money into account
        if request.form["action"] == "Deposit":

            deposit = request.form.get("money_deposit")

            # Ensure deposit form is not empty
            if not deposit:
                return apology("Please provide ammount of money you want to deposit")

            # Ensure positive float was provided
            try:
                deposit = float(deposit)
                if deposit < 0:
                    return apology("Can't deposit negative number")
            except:
                return apology("Please provide ammount of money you want to deposit")

            # Get current user id
            user_id = session["user_id"]

            # Get cash of current user
            current_user = db.execute("SELECT username, cash FROM users WHERE id = ?", user_id)
            cash = current_user[0]["cash"]

            # New balance
            updated_cash = cash + deposit

            # Update user cash balance
            db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash, user_id)

            flash(f"You have succesfully deposit {usd(deposit)}!")
            return redirect("/")

        # User wants to withdraw money from account
        if request.form["action"] == "Withdraw":

            withdraw = request.form.get("money_withdraw")

            # Ensure withdraw form is not empty
            if not withdraw:
                return apology("Please provide ammount of money you want to withdraw")

            # Ensure positive float was provided
            try:
                withdraw = float(withdraw)
                if withdraw < 0:
                    return apology("Can't withdraw negative number")
            except:
                return apology("Please provide ammount of money you want to withdraw")

            # Get current user id
            user_id = session["user_id"]

            # Get cash of current user
            current_user = db.execute("SELECT username, cash FROM users WHERE id = ?", user_id)
            cash = current_user[0]["cash"]

            # Ensure the user does not withdraw more money than he has
            if withdraw > cash:
                return apology("Not enough money")

            # New balance
            updated_cash = cash - withdraw

            # Update user cash balance
            db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash, user_id)

            flash(f"You have succesfully withdraw {usd(withdraw)}!")
            return redirect("/")

        # User wants to change their password
        if request.form["action"] == "Change":

            # Get current user id
            user_id = session["user_id"]

            # Get current user hash
            hash = db.execute("SELECT hash FROM users WHERE id = ?", user_id)

            current_password = request.form.get("current_password")

            if not current_password or not check_password_hash(hash[0]["hash"], current_password):
                return apology("Wrong password")

            new_password = request.form.get("new_password")

            if current_password == new_password:
                return apology("New password can not be the same")

            if not new_password:
                return apology("Must provide new password")

            confirm_password = request.form.get("confirm_password")

            if not confirm_password:
                return apology("Must confirm password")

             # Check the password match the confirmation
            if new_password != confirm_password:
                return apology("Confirmation does not match the password")

            # Store provided password as a hash
            new_hash = generate_password_hash(new_password)

            # Update user password
            db.execute("UPDATE users SET hash = ? WHERE id = ?", new_hash, user_id)

            # Succesful password change
            flash(f"You have succesfully changed your password!")
            return redirect("/")