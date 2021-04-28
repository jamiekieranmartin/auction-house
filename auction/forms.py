from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from .item.models import Categories


class FilterForm(FlaskForm):
    '''Filter form'''
    category = SelectField("Categories",
                           choices=[(0, 'All')] + Categories.choices(),
                           coerce=int)
    search = StringField("Search")

    submit = SubmitField("Filter")
