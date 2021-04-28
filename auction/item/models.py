from .. import db
from enum import Enum
import os
import uuid
from werkzeug.utils import secure_filename
from ..utils import JSON, humanise
from datetime import datetime
from ..bid.models import Bid


class Categories(Enum):
    '''Categories Enum'''

    Oil = 1
    Watercolor = 2
    Pastel = 3
    Acrylic = 4
    Charcoal_Drawing = 5
    Coloured_Pencil = 6
    Pencil_Sketch = 7
    Ink = 8
    Glass = 9
    Ball_Point_Pen_Art = 10
    Collage = 11
    Sand = 12
    Spray = 13
    Digital = 14
    Graffiti = 15
    Scroll = 16
    Water_Miscible_Oil_Paints = 17

    @classmethod
    def choices(cls):
        '''Returns choices for SelectField'''
        return [(choice.value, choice.name.replace('_', ' '))
                for choice in cls]


class Item(db.Model, JSON):
    '''Item database model'''
    __tablename__ = "items"

    # Identifier fields
    id = db.Column(db.Integer, unique=True, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    open = db.Column(db.Boolean, nullable=False, default=True)

    # User fields
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('items', lazy=True))

    # Descriptive fields
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(240), nullable=False)
    image = db.Column(db.String(120), nullable=False)
    category = db.Column(db.Integer, nullable=False)
    starting_price = db.Column(db.Integer, nullable=False)

    # Bids
    bids = db.relationship('Bid')

    # Initialiser function
    def __init__(self, form, user_id):
        '''The initialiser function for an item when passing a form'''
        self.user_id = user_id

        # get values from form
        self.name = form.name.data
        self.description = form.description.data
        self.category = form.category.data
        self.starting_price = form.starting_price.data

        # get file extension using last item after split of filename on '.'
        extension = secure_filename(form.image.data.filename).split('.')[-1]

        # join random uuid and extension to make filename
        self.image = '.'.join([str(uuid.uuid1()), extension])

        # make image path using filename and save image
        image_path = os.path.join('auction/static/uploads', self.image)
        form.image.data.save(image_path)

    # Humanise functions
    def category_humanise(self):
        '''Returns a prettified category'''
        return Categories(self.category).name.replace('_', ' ')

    def starting_price_humanise(self):
        '''Returns a prettified starting price'''
        return 'AUD$' + str(self.starting_price)

    def date_humanise(self):
        '''Returns humanised time difference'''
        return humanise(self.date)

# Bid functions
    def bid_count(self):
        '''Returns how many bids have been made'''
        return Bid.query.filter_by(item_id=self.id).count()

    def top_bid(self):
        '''Returns the highest bid if there is one'''
        bid = Bid.query.filter_by(item_id=self.id).order_by(
            Bid.bid.desc()).first()

        if bid is None:
            return self.starting_price

        return bid.bid

    def top_bid_humanise(self):
        '''Returns the highest bid if there is one'''
        bid = Bid.query.filter_by(item_id=self.id).order_by(
            Bid.bid.desc()).first()

        if bid is None:
            return self.starting_price_humanise()

        return 'AUD$' + str(bid.bid)

    def top_bid_date_humanise(self):
        bid = Bid.query.filter_by(item_id=self.id).order_by(
            Bid.bid.desc()).first()

        if bid is None:
            return self.date_humanise()

        return humanise(bid.date)
