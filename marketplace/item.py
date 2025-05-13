from flask import Blueprint

bp = Blueprint("item", __name__, url_prefix="/item")

@bp.route('/<int:id>')
def item(id):
    return f"Item {id}\n"
