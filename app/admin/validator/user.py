from wtforms.fields import StringField
from wtforms.validators import DataRequired, length, EqualTo
from wtforms import Form
import wtforms_json

wtforms_json.init()


class Password(Form):
    password = StringField(
        validators=[
            DataRequired(message="Please input your password"),
            length(min=6, message="Password must be at least 6 characters")
        ]
    )
    npassword = StringField(
        validators=[
            DataRequired(message="Please input your new password"),
            length(min=6, message="Password must be at least 6 characters")
        ]
    )
    cpassword = StringField(
        validators=[
            DataRequired(message="Please input your confirming password"),
            length(min=6, message="Password must be at least 6 characters"),
            EqualTo(
                'npassword', message="The new password and confirming password do not match"
            )
        ]
    )
