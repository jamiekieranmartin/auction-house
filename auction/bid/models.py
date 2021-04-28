from .. import db
from ..utils import JSON, humanise
from datetime import datetime


class Bid(db.Model, JSON):
    '''Bid Model'''
    __tablename__ = "bids"

    # Identifier fields
    id = db.Column(db.Integer, unique=True, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # User fields
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref(
        'bids', lazy=True))

    # Item fields
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)

    bid = db.Column(db.Integer, nullable=False)

    # Initialiser function
    def __init__(self, form, user_id, item_id):
        '''The initialiser function for a bid when passing a form'''
        self.user_id = user_id
        self.item_id = item_id

        # get values from form
        self.bid = form.bid.data

    def bid_humanise(self):
        '''Returns a prettified starting price'''
        return 'AUD$' + str(self.bid)

    def date_humanise(self):
        '''Returns humanised time difference'''
        return humanise(self.date)
