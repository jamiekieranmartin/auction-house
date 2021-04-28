from auction.bid.forms import BidForm
from flask import Blueprint, redirect, url_for, abort, render_template, flash
from flask_login import login_required, current_user
from ..item.models import Item
from .. import db
from .models import Bid

bid_bp = Blueprint('bid', __name__, url_prefix='/bid')


# get bids on id
# GET - returns all bids of item
@bid_bp.route('/<id>', methods=['GET', 'POST'])
@login_required
def item(id):
    user_id = current_user.id
    item = Item.query.filter_by(id=id).first()
    bids = Bid.query.filter_by(item_id=id).all()

    if item is None:
        abort(404)

    if user_id is item.user_id:
        return render_template('bid/item.html', title='Bids on item', item=item, bids=bids)
    else:
        form = BidForm()

        if form.validate_on_submit():

            if form.bid.data <= item.top_bid():
                flash('Bid must be higher than that!', 'danger')
                return redirect(url_for('bid.item', id=id))

            bid = Bid(form, user_id, id)

            db.session.add(bid)
            db.session.commit()

            flash('Successfully bid', 'success')
            return redirect(url_for('item.index', id=id))

        return render_template('bid/index.html', title='Bid', form=form, item=item)
