from flask import Blueprint

bp = Blueprint("item", __name__, url_prefix="/item")

@bp.route('/<int:id>')
def item(id):
    return render_template('item.html', id)
