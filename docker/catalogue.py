
from flask import Blueprint, request, jsonify
import psycopg2
import os

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# Session config
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = os.getenv("SECRET_KEY", "defaultsecret")
Session(app)

# Database connection
def get_db():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "marketplace"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASS", "password"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432")
    )
@app.route("/catalogue")
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

    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("""
            SELECT COUNT(*) FROM items 
            WHERE price_pennies BETWEEN %s AND %s 
            AND seller_reviews >= %s
        """, (min_price, max_price, min_rating))
        total_items = cur.fetchone()["count"]
        total_pages = (total_items + per_page - 1) // per_page

        cur.execute(f"""
            SELECT * FROM items 
            WHERE price_pennies BETWEEN %s AND %s 
            AND seller_reviews >= %s
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

if __name__ == "__main__":
    app.run(debug=True, port=8000)
