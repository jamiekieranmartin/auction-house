from sqlalchemy.orm import backref
from sqlalchemy.sql.schema import ForeignKey
from .. import db
from ..utils import JSON, humanise
from datetime import datetime


class WatchlistItem(db.Model, JSON):
    '''WatchlistItem database model'''

    __tablename__ = "watchlist_items"

    # Identifier fields
    id = db.Column(db.Integer, unique=True, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # User fields
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User',
                           backref=db.backref('watchlist_items', lazy=True))

    # Item fields
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    item = db.relationship('Item',
                           backref=db.backref('watchlist_items', lazy=True))

    # Initialiser function
    def __init__(self, user_id, item_id):
        '''The initialiser function for an item'''
        self.user_id = user_id
        self.item_id = item_id

    # Humanise functions
    def date_humanise(self):
        '''Returns humanised time difference'''
        return humanise(self.date)
