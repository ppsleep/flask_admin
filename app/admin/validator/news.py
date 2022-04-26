from wtforms.fields import StringField
from wtforms.validators import DataRequired, length
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
    content = StringField(
        validators=[
            DataRequired(message="Please input contents"),
            length(min=3, max=65535, message="Title limits 3 - 65535 characters")
        ]
    )
