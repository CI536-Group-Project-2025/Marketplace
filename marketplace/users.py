from argon2 import PasswordHasher
from argon2.profiles import RFC_9106_LOW_MEMORY
from flask import Blueprint, jsonify, request
from psycopg2 import DatabaseError
from werkzeug.wrappers import Response

from marketplace.db import get_db_cursor, commit, rollback

# As defined in our API spec.
MIN_PASSWORD_LEN = 8

# Using hashing parameters tuned for low memory environments (e.g. a docker container)
ph = PasswordHasher.from_parameters(RFC_9106_LOW_MEMORY)
bp = Blueprint("users", __name__, url_prefix="")

@bp.put('/signup')
def signup():
    content = request.get_json()
    if not content:
        response = jsonify({"message": "Invalid MIME type"})
        response.status = 400
        return response

    password = content.get("pw")
    email = content.get("email")
    user_name = content.get("user_name")
    addr = content.get("addr")

    # Delete the contents of the request so that `password` isn't hanging
    # around in memory after we are done with it.
    del content

    # We need all of this information to create a new user
    if not (password and email and user_name and addr):
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

    try:
        cur = get_db_cursor()

        # This query inserts a new user in to the users table, receives the automatically
        # generated `id` (`RETURNING id`), and uses that id to populate the userslogin
        # entry. It's all executed as one query so that if any part of it fails, the entire
        # query is scrapped.
        cur.execute("""
                    WITH user_id AS (INSERT INTO users (name)
                                     VALUES (%s)
                                     RETURNING id)
                    INSERT INTO userslogin (id, email, hash, deliveryaddr) 
                        SELECT *, %s, %s, %s FROM user_id
                    RETURNING id;
                    """, (user_name, email, hash, addr))

        id = cur.fetchone()[0]

        commit()
        cur.close()

        response = jsonify({"id": id})
        return response
    except DatabaseError as e:
        cur.close()
        response = jsonify({"message": "A user already exists with that username or email"})
        response.status = 409
        return response

