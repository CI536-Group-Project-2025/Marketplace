from flask import Blueprint
from marketplace.db import get_db_cursor, commit, rollback
from psycopg2 import DatabaseError

bp = Blueprint("users", __name__, url_prefix="")

@bp.put('/signup')
def signup():
    try:
        cur = get_db_cursor()

        cur.execute("""
                    WITH user_id AS (INSERT INTO users (name) 
                                     VALUES ('John Doe')
                                     RETURNING id)
                    INSERT INTO userslogin 
                        (id, email, hash, deliveryaddr) 
                    SELECT 
                            *,
                            'email@example.com', 
                            'd465a26b97465ebc976ddd74fbca41d8329ee45961effa84b4cde57e5a42', 
                            '1 Example Street, Town, AA11 1AA'
                            FROM user_id
                    RETURNING id;
                    """)

        id = cur.fetchone()

        commit()
        cur.close()

        return ({"id": id}, 201)
    except DatabaseError as e:
        rollback()
        return ({"message": "A user already exists with that username or email"}, 409)

