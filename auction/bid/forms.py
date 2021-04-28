from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import InputRequired, NumberRange


class BidForm(FlaskForm):
    '''Item form'''
    bid = IntegerField(
        "Bid", validators=[InputRequired(), NumberRange(min=1)])

    submit = SubmitField("Submit")
