from flask import Blueprint, render_template, redirect, url_for, flash, abort, session
from flask_login import login_required, current_user
from .forms import ItemForm
from .. import db
from .models import Item
from ..watchlist.models import WatchlistItem

# init item blueprint
item_bp = Blueprint("item", __name__, url_prefix="/item")


# get items of user
# GET - returns all items of a particular user
@item_bp.route('', methods=['GET', 'POST'])
@login_required
def items():
    items = Item.query.filter_by(user_id=current_user.id).all()

    return render_template('item/index.html', title='Items', items=items)


# get item by id
# GET - returns an item
@item_bp.route("/<id>", methods=['GET', 'POST'])
def index(id):
    item = Item.query.filter_by(id=id).first()
    watched = None

    if item is None:
        abort(404)

    if current_user:
        user_id = current_user.id
        watched = WatchlistItem.query.filter_by(user_id=user_id,
                                                item_id=item.id).first()

    return render_template("item/item.html",
                           title=item.name,
                           item=item,
                           watched=watched)


# create new item
# GET - returns create item form
# POST - posts create item form to database
@item_bp.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    user_id = current_user.id
    form = ItemForm()

    # action if form is validated when submitted
    if form.validate_on_submit():
        # create item from values
        item = Item(form, user_id)

        # save item to db
        db.session.add(item)
        db.session.commit()
        # db.session.save()

        # flash and return to home screen
        flash('Item created!', 'success')
        return redirect(url_for('item.index', id=item.id))

    # return template if the form hasn't validated
    return render_template('item/create.html', form=form, title="Create Item")


@item_bp.route('/<id>/close', methods=['GET'])
@login_required
def close(id):
    user_id = current_user.id
    item = Item.query.filter_by(id=id, user_id=user_id, open=True).first()

    if item is None:
        abort(400)

    item.open = False

    db.session.commit()

    # flash and return to home screen
    flash('Auction closed!', 'success')
    return redirect(url_for('item.index', id=id))
