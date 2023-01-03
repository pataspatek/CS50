from flask import Flask, render_template, redirect, request, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL

from helpers import login_required, usd

# Configurate application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Set a secret key
SECRET_KEY = "\x0f\xab\xbe5K\xbb7\xfe\x08\xa6\x10\xc7p-\x92\x98\xff\xb8\xe6\x9d|\x8e\xc7\xe7"
app.config["SECRET_KEY"] = SECRET_KEY

# Configurate CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.context_processor
def inject():
    """Inject data to all html templates"""

    # Get current user id
    user_id = session.get("user_id")

    # Find the status of the current user
    current_person = db.execute("SELECT * FROM users WHERE id = ?", user_id)

    return dict(current_person=current_person, usd=usd)


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show home page to the user"""

    # User reached route via GET
    if request.method == "GET":

        # Get all of the registered restaurants
        restaurants = db.execute("SELECT * FROM restaurant")

        return render_template("index.html", restaurants=restaurants)

    # User reached route via POST
    else:
        restaurant = request.form.get("restaurant")
        print(restaurant)

        owner = db.execute("SELECT owner FROM restaurant WHERE name = ?", restaurant)

        products = db.execute("SELECT name, price FROM products WHERE owner = ?", owner[0]['owner'])

        return render_template("menu.html", restaurant=restaurant, products=products)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via GET
    if request.method == "GET":

        return render_template("register.html")

    # User reached route via POST (as by submitting a form)
    else:
        username = request.form.get("username")
        name = request.form.get("name")
        surname = request.form.get("surname")
        email = request.form.get("email")
        address = request.form.get("address")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was provided
        if not username:
            flash("Must provide username")
            return render_template("register.html", username=username, name=name, surname=surname, email=email, address=address, password=password)

        # Ensure email was provided
        if not email:
            flash("Must provide email")
            return render_template("register.html", username=username, name=name, surname=surname, email=email, address=address, password=password)

        # Ensure password was provided
        if not password:
            flash("Must provide password")
            return render_template("register.html", username=username, name=name, surname=surname, email=email, address=address, password=password)

        # Ensure confirmation was provided
        if not confirmation:
            flash("Must confirm your password")
            return render_template("register.html", username=username, name=name, surname=surname, email=email, address=address, password=password)

        # Ensure confirmation match the password
        if password != confirmation:
            flash("Confirmation does not match the password")
            return render_template("register.html", username=username, name=name, surname=surname, email=email, address=address, password=password)

        # Check whether username is already taken
        username_check = db.execute("SELECT username FROM users WHERE username = ?", username)
        if len(username_check) >= 1:
            flash("Username is already taken")
            return render_template("register.html", username=username, name=name, surname=surname, email=email, address=address, password=password)

        # Check whether e-mail is already taken
        email_check = db.execute("SELECT email FROM users WHERE email = ?", email)
        if len(email_check) >= 1:
            flash("Email is already taken")
            return render_template("register.html", username=username, name=name, surname=surname, email=email, address=address, password=password)

        # Hash provided password
        hash = generate_password_hash(password)

        # Add new user to database
        new_user = db.execute("""INSERT INTO users (username, name, surname, email, address, hash)
        VALUES(?, ?, ?, ?, ?, ?)""",
        username, name, surname, email, address, hash)

        # Create new session for the registered user
        session["user_id"] = new_user

        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log in user"""

    # Forget any user_id
    session.clear()

    # User reached route via GET
    if request.method == "GET":
        return render_template("login.html")

    # User reached route via POST (as by submitting a form)
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was provided
        if not username:
            flash("Must provide username")
            return render_template("login.html", username=username, password=password)

        # Ensure password was provided
        if not password:
            flash("Must provide password")
            return render_template("login.html", username=username, password=password)

        # Query database to check if the user exist
        query = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exist and password is correct
        if len(query) != 1 or not check_password_hash(query[0]["hash"], password):
            flash("Invalid username and/or password")
            return render_template("login.html", username=username, password=password)

        # Remember which user has logged in
        session["user_id"] = query[0]["id"]

        return redirect("/")


@app.route("/logout")
def logout():
    """Log out user"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/manage", methods=["GET", "POST"])
@login_required
def manage():
    """Manage account"""

    # User reached route via GET
    if request.method == "GET":

        return render_template("manage.html")

    # User reached route via POST (as by submitting a form)
    else:

        # User wants to deposit money into account
        if request.form["action"] == "deposit":

            # Get user input
            deposit = request.form.get("deposit")

            # Ensure ammount was provided
            if not deposit:
                flash("Please provide ammount of money you want to deposit")
                return redirect("/manage")

            # Ensure positive float was provided
            try:
                deposit = float(deposit)
                if deposit < 0:
                    flash("Must provide positive number")
                    return redirect("/manage")
            except:
                flash("Must provide positive number")
                return redirect("/manage")

            # Get current user id
            user_id = session["user_id"]

            current_user = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
            cash = current_user[0]["cash"]

            # Update user balance
            updated_cash = cash + deposit

            db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash, user_id)

            flash(f"You have succesfully deposit {usd(deposit)}!")

            return redirect("/")

        # User wants to change his password
        if request.form["action"] == "password_change":

            # Save form inputs
            current = request.form.get("current_password")
            new = request.form.get("new_password")
            confirmation = request.form.get("confirm_password")

            # Get current user id
            user_id = session["user_id"]

            # Get current user hash
            hash = db.execute("SELECT hash FROM users WHERE id = ?", user_id)
            hash = hash[0]["hash"]

            # Ensure correct current password was provided
            if not current or not check_password_hash(hash, current):
                flash("Wrong password")
                return redirect("/manage")

            # Ensure new password was provided
            if not new:
                flash("Must provide new password")
                return redirect("/manage")

            # Ensure new password differ from current
            if new == current:
                flash("New password can not be the same as current")
                return redirect("/manage")

            # Ensure confirmation was provided
            if not confirmation:
                flash("Must confirm password")
                return redirect("/manage")

            # Check if the confirmation match new password
            if new != confirmation:
                flash("Confirmation does not match the new password")
                return redirect("/manage")

            # Create a new hash from new password
            new_hash = generate_password_hash(new)

            # Update user password
            db.execute("UPDATE users SET hash = ? WHERE id = ?", new_hash, user_id)

            # Password change was succesful
            flash("You have succesfully changed your password!")
            return redirect("/")


@app.route("/partnership", methods=["GET", "POST"])
@login_required
def partnership():
    """Became a partner and register your restaurant via form"""

    # User reached route via GET
    if request.method == "GET":

        # Current user
        user_id = session["user_id"]
        user = db.execute("SELECT username FROM users WHERE id = ?", user_id)
        user = user[0]["username"]

         # Quesry for users requests
        try:
            users_requests = db.execute("SELECT * FROM requests WHERE owner = ?", user)

        except:
            pass

        return render_template("partnership.html", users_requests=users_requests)

    # User reached route via POST (as by submitting a form)
    else:

        # Form
        name = request.form.get("restaurant")
        description = request.form.get("description")

        # Current user
        user_id = session["user_id"]
        owner = db.execute("SELECT username FROM users WHERE id =?", user_id)
        owner = owner[0]["username"]

        # Ensure name of the restaurant was provided
        if not name:
            flash("Must provide name of the restaurant")
            return redirect("/partnership")

        # Ensure that for this named restaurant is not already applied
        requests = db.execute("SELECT * FROM requests WHERE name = ?", name)

        if len(requests) >= 1:
            flash("For this restaurant was already apllied")
            return redirect("/partnership")

        # Ensure the restaurant is not already partnered
        restaurants = db.execute("SELECT * FROM restaurant WHERE name = ?", name)

        if len(restaurants) >= 1:
            flash("This restaurant is alredy partner")
            return redirect("/partnership")

        # Ensure only one restaurant for each user
        exist_owner = db.execute("SELECT * FROM restaurant WHERE owner = ?", owner)

        if len(exist_owner) >= 1:
            flash("You are already owner")
            return redirect("/partnership")

        # Ensure only one request was sent by this user
        request_owner = db.execute("SELECT * FROM requests WHERE owner = ?", owner)

        if len(request_owner) >= 1:
            flash("You already sent request")
            return redirect("/partnership")

        # Add new user to database
        db.execute("INSERT INTO requests (name, description, owner) VALUES(?, ?, ?)", name, description, owner)

        flash(f"Congratulations, {name} successfully requested to become a partner")
        return redirect("/")


@app.route("/requests", methods=["GET", "POST"])
@login_required
def requests():
     # User reached route via GET
    if request.method == "GET":

        # Query for all requests
        pending = db.execute("SELECT * FROM requests")

        return render_template("requests.html", pending=pending)

    # User reached route via POST (as by submitting a form)
    else:

        # Admin accept the request
        if request.form["action"] == "Accept":

            # Get restaurant name from hiddne form
            restaurant_name = request.form.get("restaurant")
            restaurant_description = request.form.get("description")
            restaurant_owner = request.form.get("owner")

            # Remove request from requests table
            db.execute("DELETE FROM requests WHERE name = ?", restaurant_name)

            # Change user status to owner
            db.execute("UPDATE users SET status = ? WHERE username = ?", "owner", restaurant_owner)

            # Insert into restaurant
            db.execute("INSERT INTO restaurant (name, description, owner) VALUES(?, ?, ?)", restaurant_name,   restaurant_description,  restaurant_owner)

            flash(f"{restaurant_name} was accepted!")
            return redirect("/requests")


        if request.form["action"] == "Decline":

            # Get restaurant name from hiddne form
            restaurant_name = request.form.get("restaurant")

            # Remove request from requests table
            db.execute("DELETE FROM requests WHERE name = ?", restaurant_name)

            flash(f"{restaurant_name} was declined!")
            return redirect("/requests")


@app.route("/restaurant", methods=["GET", "POST"])
@login_required
def restaurant():
    # User reached route via GET
    if request.method == "GET":

        # Get current user
        user_id = session["user_id"]
        user_name = db.execute("SELECT username FROM users WHERE id = ?", user_id)
        user_name = user_name[0]["username"]

        # Get current restaurant
        restaurant_name = db.execute("SELECT name FROM restaurant WHERE owner = ?", user_name)
        restaurant_name = restaurant_name[0]["name"]

        # Get all the products of the current user's restaurant
        products = db.execute("SELECT name, price FROM products WHERE owner = ?", user_name)

        return render_template("restaurant.html", restaurant_name=restaurant_name, products=products)

    # User reached route via POST (as by submitting a form)
    else:

        # Add new product
        if request.form["action"] == "Add":

            # Get product name from the form
            product = request.form.get("product")

            # Ensure product name was provided
            if not product:
                flash("Must provide product name!")
                return redirect("/restaurant")

            # Check if the product already exist
            all_products = db.execute("SELECT * FROM products WHERE name = ?", product)

            if len(all_products) >= 1:
                flash("Product is already registered")
                return redirect("/restaurant")

            # Get product price from the price
            price = request.form.get("price")

            # Ensure price was provided
            if not price:
                flash("Must provide price of the product")
                return redirect("/restaurant")

            # Ensure positive float was provided
            try:
                price = float(price)
                if price <= 0:
                    flash("Must provide positive number")
                    return redirect("/restaurant")

            except:
                flash("Must provide positive number")
                return redirect("/restaurant")

            # Current user id
            user_id = session["user_id"]
            user_name = db.execute("SELECT username FROM users WHERE id = ?", user_id)
            user_name = user_name[0]["username"]

            # Insert into products table
            db.execute("INSERT INTO products (name, price, owner) VALUES(?, ?, ?)", product, price, user_name)

            flash(f"New product was added!")
            return redirect("/restaurant")

        # Remove product
        if request.form["action"] == "Delete":

            # Get restaurant name from hiddne form
            product_name = request.form.get("product")

            # Remove request from requests table
            db.execute("DELETE FROM products WHERE name = ?", product_name)

            return redirect("/restaurant")


@app.route("/menu", methods=["POST"])
@login_required
def menu():
    # Get a list with all of the selected products
    selected_products = request.form.getlist("products")

    products_price = 0

    for product in selected_products:
        price = db.execute("SELECT price FROM products WHERE name = ?", product)
        price = price[0]["price"]
        products_price += price

    print(products_price)

    # Get current user's balance
    user_id = session["user_id"]
    current_balance = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    # Check if the user has enough cash for the purchase
    if products_price > current_balance:
        flash("Not enough money for the purchase!")
        return redirect("/")

     # Update user balance
    updated_cash = current_balance - products_price

    db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash, user_id)

    return render_template("confirmation.html", selected_products=selected_products)