from flask import Blueprint, render_template, request, jsonify

from marketplace.db import get_db_connection

bp = Blueprint("catalogue", __name__, url_prefix="")

@bp.route("/")
def page_catalogue():
    min_price = request.args.get("min_price", default=0, type=int)
    max_price = request.args.get("max_price", default=10**9, type=int)
    min_rating = request.args.get("min_rating", default=0.0, type=float)
    sort_by = request.args.get("sort_by", default="price_asc", type=str)
    page = request.args.get("page", default=1, type=int)
    per_page = 10

    # Sorting SQL
    sort_sql = {
        "price_asc": "price_pennies ASC",
        "price_desc": "price_pennies DESC",
        "rating": "seller_reviews DESC"
    }.get(sort_by, "price_pennies ASC")

    # If min_rating is None or zero, allow showing sellers with no ratings
    rating_sql = "AND mean_rating >= %s" if min_rating else ""

    offset = (page - 1) * per_page

    conn = get_db_connection()
    cur = conn.cursor()

    try:

        cur.execute(f"""
            SELECT COUNT(*) FROM items JOIN usersRatings ON seller_id = usersRatings.name
            WHERE price_pennies BETWEEN %s AND %s
            {rating_sql} AND sold = false;
        """, (min_price, max_price, min_rating))
        total_items = cur.fetchone()[0]
        total_pages = (total_items + per_page - 1) // per_page

        cur.execute(f"""
            SELECT id, items.name, price_pennies, seller_id, mean_rating FROM items JOIN usersRatings ON seller_id = usersRatings.name 
            WHERE price_pennies BETWEEN %s AND %s 
            AND mean_rating >= %s AND sold = false
            ORDER BY {sort_sql}
            LIMIT %s OFFSET %s;
        """, (min_price, max_price, min_rating, per_page, offset))

        products = cur.fetchall()
        cur.close()
        conn.close()

        return render_template(
                    'catalogue.html',
                    products=products, 
                    current_page=page,
                    total_pages=total_pages,
                    total_items=total_items)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
