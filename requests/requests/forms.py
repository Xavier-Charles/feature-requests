from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField,IntegerField,\
            SubmitField, BooleanField, FileField, TextAreaField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, ValidationError, Length
from requests.models import User, Requests, Clients

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ClientForm(FlaskForm):
    name = StringField('Client name', validators=[DataRequired()])
    location = StringField('Title', validators=[DataRequired(), Length(min=5, max=255)])
    submit = SubmitField('Add client')

class UpdateClientForm(FlaskForm):
    name = StringField('Client name', validators=[DataRequired()])
    location = StringField('Title', validators=[DataRequired(), Length(min=5, max=255)])
    submit = SubmitField('Update')

def client_query():
    return Clients.query

def get_pk(obj):
    return str(obj)

class RequestForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=255)])
    description = TextAreaField('Description', validators=[DataRequired()])
    product_area = SelectField('Product area', choices=(('Policies','Policies'), ('Billing','Billing'), ('Claims','Claims'), ('Reports','Reports')),\
            validators=[DataRequired()])

    target_date = DateField('Target Date',validators=[DataRequired()], format="%Y-%m-%d")
    files = FileField('Files', validators=[FileAllowed(['jpg','png','txt','doc','docx','pdf'])])
    client_priority = SelectField('Priority', choices=(('A_level','A_level'),\
            ('B_level','B_level'),('C_level','C_level'),('D_level','D_level')), validators=[DataRequired()])

    submit = SubmitField('Add request')

    def validate_requests(self, username):
        request_ = User.query.filter_by(title=title.data).first()
        same_request = User.query.filter_by(client=client).first()
        if request_ == same_request:
            raise ValidationError(" The request has already been added ")

class UpdateRequestForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=255)])
    description = TextAreaField('Description', validators=[DataRequired()])
    product_area = SelectField('Product area', choices=(('Policies','Policies'), ('Billing','Billing'), ('Claims','Claims'), ('Reports','Reports')),\
            validators=[DataRequired()])

    target_date = DateField('Target Date',validators=[DataRequired()], format="%Y-%m-%d")
    files = FileField('Files', validators=[FileAllowed(['jpg','png','txt','doc','docx','pdf'])])
    client_priority = SelectField('Priority', choices=(('A_level','A_level'),\
            ('B_level','B_level'),('C_level','C_level'),('D_level','D_level')), validators=[DataRequired()])

    submit = SubmitField('Update')

