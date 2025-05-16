from flask import Blueprint, render_template, session

from marketplace.db import get_db_connection
from marketplace.users import login_required

bp = Blueprint("basket", __name__, url_prefix="/basket")

@bp.get("/")
@login_required
def page_basket():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
            "SELECT name, price_pennies, seller_id, item_id FROM baskets, items WHERE user_name = %s AND item_id = id;",
            (session["user"],)
            )

    items = cur.fetchall()
    cur.close()
    conn.close()

    # No need to error on an empty basket, just show the user that their basket is empty
    if items is None:
        items = []

    return render_template('basket.html', items=items)

# @bp.route("/", methods=["POST"])
# def create_basket():
#     user_id = request.json.get("user_id")
#     if not user_id:
#         return jsonify({"error": "user_id is required"}), 400
#
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("INSERT INTO basket (user_id) VALUES (%s) RETURNING id;", (user_id,))
#     basket_id = cur.fetchone()[0]
#     conn.commit()
#     cur.close()
#     conn.close()
#     return jsonify({"id": basket_id}), 201
