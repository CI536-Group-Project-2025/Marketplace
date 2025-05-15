
from flask import Blueprint, request, jsonify
import psycopg2
import os

bp = Blueprint("basket", __name__, url_prefix="/basket")

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        database=os.getenv("POSTGRES_DB", "postgres"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres"),
        port=os.getenv("POSTGRES_PORT", 5432)
    )

@bp.route("/", methods=["GET"])
def get_baskets():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM basket;")
    baskets = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(baskets)

@bp.route("/", methods=["POST"])
def create_basket():
    user_id = request.json.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO basket (user_id) VALUES (%s) RETURNING id;", (user_id,))
    basket_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": basket_id}), 201

@bp.route("/<int:id>", methods=["GET"])
def get_basket(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM basket WHERE id = %s;", (id,))
    basket = cur.fetchone()
    cur.close()
    conn.close()
    if basket:
        return jsonify(basket)
    else:
        return jsonify({"error": "Basket not found"}), 404
