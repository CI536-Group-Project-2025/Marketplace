from flask import Blueprint, flash, redirect, render_template, session, url_for

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

@bp.post("/add/<int:id>")
@login_required
def basket_add(id):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO baskets VALUES (%s, %s);", (session["user"], id))
        conn.commit()
        cur.close()
        conn.close()
        # flash("Added to basket!")
    except:
        flash("Could not add item to basket")
    
    return redirect(url_for('item.page_item', id=id))

@bp.post("/remove/<int:id>")
@login_required
def basket_remove(id):
    conn = get_db_connection()
    cur = conn.cursor()

    # Not worried about errors, as the remove option will only be shown when somebody
    # has it in their basket. If somebody manually tries this endpoint, that's their
    # problem.
    cur.execute("DELETE FROM baskets WHERE user_name = %s AND item_id = %s", (session["user"], id))
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('basket.page_basket'))
