from flask import Blueprint, render_template

from marketplace.db import get_db_connection

bp = Blueprint("item", __name__, url_prefix="/item")

@bp.route('/<int:id>')
def item(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, items.name, price_pennies, seller_id, description, mean_rating FROM items JOIN usersRatings ON seller_id = usersRatings.name WHERE id = %s", (id,))

    item = cur.fetchone()
    cur.close()
    conn.close()
    
    if item is None:
        return "Item not found", 404
    
    try:
        # Assuming the item tuple is structured as (id, name, price, description)
        item_info = {
            "id": item[0],
            "name": item[1],
            "price_pennies": item[2],
            "seller_id": item[3],
            "description": item[4],
            "seller_rating": item[5]
        }
    except Exception:
        return "An error occurred while loading the item", 500

    
    return render_template('item.html', item_info=item_info)