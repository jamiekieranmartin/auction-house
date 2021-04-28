from flask import Blueprint, render_template, flash, redirect, url_for, abort
from .models import WatchlistItem
from .. import db
from flask_login import login_required, current_user

# init user blueprint
watchlist_bp = Blueprint("watchlist", __name__, url_prefix="/watchlist")


# get all watchlist items of user
# GET - returns an watchlist items
@watchlist_bp.route("", methods=['GET'])
@login_required
def index():
    watchlist = WatchlistItem.query.filter_by(user_id=current_user.id).all()
    return render_template("watchlist.html",
                           title="Watchlist",
                           watchlist=watchlist)


# remove a watched item from users watchlist
# POST - removes item
@watchlist_bp.route('/<item_id>/remove', methods=['GET'])
@login_required
def remove(item_id):
    user_id = current_user.id

    query = WatchlistItem.query.filter_by(item_id=item_id, user_id=user_id)
    watchlist_item = query.first()

    if watchlist_item is not None:
        query.delete()
        db.session.commit()

        flash('Watchlist Item removed!', 'success')
        return redirect(url_for('watchlist.index'))

    abort(400)


@watchlist_bp.route('/<item_id>/add', methods=['GET'])
@login_required
def add(item_id):
    user_id = current_user.id

    exists = WatchlistItem.query.filter_by(user_id=user_id,
                                           item_id=item_id).first()

    if exists:
        flash('Item already watched!', 'danger')
        return redirect(url_for('item.index', id=item_id))

    watched = WatchlistItem(user_id, item_id)

    db.session.add(watched)
    db.session.commit()

    # flash and return to watchlist screen
    flash('Item added to Watchlist!', 'success')
    return redirect(url_for('watchlist.index'))
