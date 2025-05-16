from flask import Blueprint, render_template
from marketplace.db import get_db_cursor  # Update the module path to the correct one

bp = Blueprint("item", __name__, url_prefix="/item")

@bp.route('/<int:id>')
def item(id):
    cursor = get_db_cursor()
    cursor.execute("SELECT id,name,price,description FROM items WHERE id = %s", (id,))
    item = cursor.fetchone()
    
    if item is None:
        return "Item not found", 404
    
    try:
        # Assuming the item tuple is structured as (id, name, price, description)
        item_info = {
            "id": item[0],
            "name": item[1],
            "price": item[2],
            "description": item[3]
        }
    except Exception as e:
        print("Error loading item {id}: {e}")
        return "An error occurred while loading the item", 500

    
    return render_template('item.html', item=item_info)