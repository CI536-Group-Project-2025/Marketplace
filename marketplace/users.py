import functools

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from argon2.profiles import RFC_9106_LOW_MEMORY
from flask import Blueprint, jsonify, render_template, redirect, request, session, url_for
import os
import psycopg2
from flask import Blueprint, jsonify, request, session
from psycopg2 import DatabaseError

from marketplace.db import get_db_connection

# As defined in our API spec.
MIN_PASSWORD_LEN = 8

# Using hashing parameters tuned for low memory environments (e.g. a docker container)
ph = PasswordHasher.from_parameters(RFC_9106_LOW_MEMORY)
bp = Blueprint("users", __name__, url_prefix="")

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get("user") is None:
            return redirect(url_for('users.page_login'))

        return view(**kwargs)

    return wrapped_view

@bp.get('/signup')
def page_sign_up():
    return render_template("signup.html")

@bp.post('/signup')
def user_sign_up():
    content = request.form
    if not content:
        response = jsonify({"message": "Invalid MIME type"})
        response.status = 400
        return response

    password = content.get("pw")
    email = content.get("email")
    user_name = content.get("user_name")
    post_code = content.get("post_code")
    addr_line_1 = content.get("address_line1")
    addr_line_2 = content.get("address_line2")
    addr_level_1 = content.get("address_level1")
    addr_level_2 = content.get("address_level2")

    # Delete the contents of the request so that `password` isn't hanging
    # around in memory after we are done with it.
    del content

    # We need all of this information to create a new user
    if not (password and email and user_name and post_code and addr_line_1):
        response = jsonify({"message": "Valid json data not provided"})
        response.status = 400
        return response

    if len(password) < MIN_PASSWORD_LEN:
        response = jsonify({"message": f"Your password too is short. Passwords must be at least {MIN_PASSWORD_LEN} characters."})
        response.status = 400
        return response

    hash = ph.hash(password)
    # Delete password so that it's not available in memory any longer than necessary.
    # NOTE: Since Python is Garbage-Collected, this doesn't actually guarantee that
    # the memory is zeroed & freed now, but it gives a better chance that it is sooner.
    del password

    conn = psycopg2.connect(host='postgres',
                            database='postgres',
                            user=os.environ["DB_USER"],
                            password=os.environ["DB_PASS"])
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO users (name, email, hash) VALUES (%s, %s, %s);", (user_name, email, hash))

        cur.execute("INSERT INTO usersShippingAddress VALUES (%s, %s, %s, %s, %s, %s);", (user_name, post_code, addr_line_1, addr_line_2, addr_level_2, addr_level_1))

        conn.commit()
        cur.close()

        session["user"] = user_name
        return redirect('/')
    except DatabaseError:
        conn.rollback()
        cur.close()
        response = jsonify({"message": "A user already exists with that username or email"})
        response.status = 409
        return response


@bp.get("/login")
def page_login():
    return render_template("login.html")

@bp.post("/login")
def user_login():
    content = request.form
    if not content:
        response = jsonify({"message": "Invalid MIME type"})
        response.status = 400
        return response

    password = content.get("pw")
    user_name = content.get("user_name")

    del content

    if not (password and user_name):
        response = jsonify({"message": "Valid form data not provided"})
        response.status = 400
        return response

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT hash FROM users WHERE name = %s;", (user_name,))
        
        hash = cur.fetchone()

        cur.close()
        conn.close()

        if hash is None or not len(hash):
            response = jsonify({"message": "No user by that name exists"})
            response.status = 404
            return response
        
        ph.verify(hash[0], password)
        del password

        # Add a user session
        session["user"] = user_name
        
        return redirect('/')
    except VerifyMismatchError:
        response = jsonify({"message": "Incorrect user name or password"})
        response.status = 403
        return response

        


