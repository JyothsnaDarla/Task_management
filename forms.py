from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=150)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=2000)])
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')])
    priority = SelectField('Priority', choices=[('1', 'Low'), ('2', 'Medium'), ('3', 'High')], coerce=int)
    due_date = DateField('Due date', validators=[Optional()], format='%Y-%m-%d')
    submit = SubmitField('Save')

class TaskQuickForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=150)])
    description = StringField('Description', validators=[Optional(), Length(max=300)])
    submit = SubmitField('Add')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
