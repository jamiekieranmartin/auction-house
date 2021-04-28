from flask import Blueprint, render_template
from .item.models import Item
from .forms import FilterForm
from sqlalchemy import or_

bp = Blueprint('main', __name__)


# get items of user
# GET - returns all items
@bp.route('/', methods=['GET', 'POST'])
def index():
    form = FilterForm()

    query = Item.query

    if form.validate_on_submit():
        search = '%{search}%'.format(search=form.search.data)
        category = form.category.data

        query = query.filter(
            or_(Item.name.like(search), Item.description.like(search)))

        if (category > 0):
            query = query.filter_by(category=category)

    items = query.order_by(Item.date.desc()).all()

    return render_template('index.html', title='Items', items=items, form=form)
