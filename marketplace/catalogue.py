from flask import Blueprint, request, jsonify

from marketplace.db import get_db_connection

bp = Blueprint("catalogue", __name__, url_prefix="")

@bp.route("/")
def catalogue():
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

    offset = (page - 1) * per_page

    conn = get_db_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            SELECT COUNT(*) FROM items JOIN usersRatings ON seller_id = usersRatings.name
            WHERE price_pennies BETWEEN %s AND %s
            AND mean_rating >= %s;
        """, (min_price, max_price, min_rating))
        total_items = cur.fetchone()[0]
        total_pages = (total_items + per_page - 1) // per_page

        cur.execute(f"""
            SELECT * FROM items JOIN usersRatings ON seller_id = usersRatings.name 
            WHERE price_pennies BETWEEN %s AND %s 
            AND mean_rating >= %s
            ORDER BY {sort_sql}
            LIMIT %s OFFSET %s
        """, (min_price, max_price, min_rating, per_page, offset))

        products = cur.fetchall()
        return jsonify({
            "products": products,
            "pagination": {
                "current_page": page,
                "total_pages": total_pages,
                "total_items": total_items
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            cur.close()
            conn.close()
