from email import message
from email.policy import default
from wtforms.fields import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange, length, Optional
from wtforms import Form
import wtforms_json

wtforms_json.init()


class Post(Form):
    title = StringField(
        validators=[
            DataRequired(message="Please input title"),
            length(min=3, max=120, message="Title limits 3 - 120 characters")
        ]
    )
    author = StringField(
        validators=[
            DataRequired(message="Please input author"),
            length(min=2, max=36, message="Author limits 2 - 36 characters")
        ]
    )
    tags = StringField(
        validators=[
            DataRequired(
                message="Please input tags, multiple tags separated by commas"),
            length(min=2, max=360, message="Tags limits 2 - 360 characters")
        ]
    )
    content = StringField(
        validators=[
            DataRequired(message="Please input contents"),
            length(min=3, max=65535, message="Title limits 3 - 65535 characters")
        ]
    )
