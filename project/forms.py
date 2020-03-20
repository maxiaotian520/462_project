from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectMultipleField, SelectField
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Required
from project.models import User

class MultiCheckboxField(SelectMultipleField):
	widget = ListWidget(prefix_label=False)
	option_widget = CheckboxInput()

class Select2MultipleField(MultiCheckboxField):

    def pre_validate(self, form):
        # Prevent "not a valid choice" error
        pass

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = ",".join(valuelist)
        else:
            self.data = ""

class RegisteraionForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    genre = Select2MultipleField('What kind of movie do you like?', choices=[('1', 'Crime'),  ('2', 'Comedy'), ('3', 'Drama'),
                                                 ('4', 'Thriller'), ('5', 'Family'), ('6', 'Adventure'),
                                                 ('7', 'Mystery'), ('8', 'Documentary'), ('9', 'Fantasy')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That name is taken, Please choose a different one')

    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken, Please choose a different one')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    genre = Select2MultipleField('What kind of movie do you like?', choices=[('1', 'Crime'), ('2', 'Comedy'), ('3', 'Drama'),
                                                   ('4', 'Thriller'), ('5', 'Family'), ('6', 'Adventure'),
                                                   ('7', 'Mystery'), ('8', 'Documentary'), ('9', 'Fantasy')])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That name is taken, Please choose a different one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken, Please choose a different one')
