from wtforms.fields import StringField, FieldList
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
    author = StringField(
        validators=[
            DataRequired(message="Please input author"),
            length(min=2, max=36, message="Author limits 2 - 36 characters")
        ]
    )
    tags = FieldList(
        StringField(
            validators=[
                DataRequired(message="Please input tags"),
                length(min=2, max=36, message="Tag limits 2 - 36 characters")
            ],
        ),
        validators=[
            DataRequired(
                message="Please input tags")
        ]
    )
    content = StringField(
        validators=[
            DataRequired(message="Please input contents"),
            length(min=3, max=65535, message="Title limits 3 - 65535 characters")
        ]
    )
