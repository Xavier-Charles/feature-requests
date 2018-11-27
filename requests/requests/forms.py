from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,IntegerField,\
            SubmitField, BooleanField, FileField, TextAreaField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, ValidationError, Length
from requests.models import User, Requests, Clients
from wtforms_sqlalchemy.fields import QuerySelectField


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ClientForm(FlaskForm):
    name = StringField('Client name', validators=[DataRequired()])
    location = StringField('Title', validators=[DataRequired(), Length(min=5, max=255)])
    submit = SubmitField('Add client')

def client_query():
    return Clients.query

class RequestForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=255)])
    description = TextAreaField('Description', validators=[DataRequired()])
    product_area = SelectField('Product area', choices=('Policies', 'Billing', 'Claims', 'Reports'),\
            validators=[DataRequired()])
    target_date = DateField('Target Date',validators=[DataRequired()], format="%Y-%m-%d")
    files = FileField('Files')
    client_priority = SelectField('Priority', choices=(('a','A_level'),\
            ('b','B_level'),('c','C_level'),('d','D_level')), validators=[DataRequired()])
    client = QuerySelectField(label='Clients', query_factory=client_query, allow_blank=True)
    submit = SubmitField('Add request')

    def validate_requests(self, username):
        request_ = User.query.filter_by(title=title.data).first()
        same_request = User.query.filter_by(client=client).first()
        if request_ == same_request:
            raise ValidationError(" The request has already been added ")

