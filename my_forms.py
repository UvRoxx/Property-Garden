from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, URL
from flask_ckeditor import CKEditorField
from flask_wtf import RecaptchaField
from wtforms.fields.html5 import EmailField

provinces = ["Quebec", "British Columbia", "Manitoba", "New Brunswick", "Newfoundland", "Labrador"
    , "Nova Scotia", "Ontario", "Prince Edward Island", "Alberta", "Saskatchewan"]
rooms = ["Any", 1, 2, 3, 4, 5]


class SearchForm(FlaskForm):
    search = StringField(label="", validators=[DataRequired()])
    submit = SubmitField(label="Search")

class SearchFormS(FlaskForm):
    search_string = StringField(label="", validators=[DataRequired()])
    number_of_rooms = SelectField(label="Number Of Rooms", choices=rooms)
    province = SelectField(label="Province", choices=provinces)
    submit = SubmitField(label="Search")


class SignUpForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    recaptcha = RecaptchaField()

    submit = SubmitField("Log In")


class PostListingForm(FlaskForm):
    title = StringField("Listing Title", validators=[DataRequired()])
    listing_url = StringField("Listing URL", validators=[DataRequired(), URL()])
    listing_address = StringField("Listing Address", validators=[DataRequired()])
    listing_price = IntegerField("Listing Price", validators=[DataRequired()])
    about = TextAreaField("About You", validators=[DataRequired()])
    submit = SubmitField("Post Listing")


class PostListingDirectForm(FlaskForm):
    title = StringField("Listing Title", validators=[DataRequired()])
    about = TextAreaField("About You", validators=[DataRequired()])
    submit = SubmitField("Post Listing")


class ContactForm(FlaskForm):
    message = TextAreaField("Message ", validators=[DataRequired()])
    submit = SubmitField("Send")
