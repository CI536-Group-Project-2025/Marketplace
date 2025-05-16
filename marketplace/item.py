from flask import Blueprint, render_template
from marketplace.users import login_required

bp = Blueprint("item", __name__, url_prefix="/item")

@bp.route("/<int:id>")
def page_item(id):
    return render_template('item.html', id=id)

@bp.route("/<int:id>/buy")
@login_required
def buy(id):
    return f"Buy {int(id)}!"
