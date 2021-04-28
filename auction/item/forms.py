from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, TextAreaField
from wtforms.validators import InputRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired
from .models import Categories


class ItemForm(FlaskForm):
    '''Item form'''
    name = StringField("Name", validators=[InputRequired()])
    description = TextAreaField("Description", validators=[InputRequired()])
    starting_price = IntegerField(
        "Starting Price", validators=[InputRequired(),
                                      NumberRange(min=1)])
    category = SelectField("Categories",
                           choices=Categories.choices(),
                           coerce=int)
    image = FileField(
        "Image",
        validators=[FileRequired(),
                    FileAllowed(['jpg', 'jpeg', 'png'])])

    submit = SubmitField("Submit")
