# forms.py
from flask_wtf import FlaskForm
from wtforms import IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class ClaimForm(FlaskForm):
    policy_id = IntegerField('Policy ID', validators=[DataRequired(), NumberRange(min=1)])
    description = TextAreaField('Description of the Claim', validators=[DataRequired()])
    submit = SubmitField('Submit Claim')