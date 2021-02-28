from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
# Search Functions Imported Here
from search_centris import SearchCentris
from search_zumper import SearchZumper
from search_kijiji import SearchKijiji
from search_dupropio import SearchDupropio
from fix_query import get_place_name
from send_mail import send_mail

# Flask Boot Strap And Form Functions Here
from flask_bootstrap import Bootstrap

# My Forms Libraries Here
from my_forms import SearchForm, LoginForm, SignUpForm, PostListingForm, PostListingDirectForm, ContactForm
from flask_ckeditor import CKEditor

# SQLAlchemy Libraries Here
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from sqlalchemy.orm import relationship

# Standard Libraries
from datetime import date
from random import shuffle
import json
import os

# GLOBAL VARS

# Flask App Setup
app = Flask(__name__)
search_centris = SearchCentris()
search_zumper = SearchZumper()
search_kijiji = SearchKijiji()
search_dupropio = SearchDupropio()
Bootstrap(app)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

# CKEditor Config

ckeditor = CKEditor(app)
app.config['CKEDITOR_PKG_TYPE'] = 'baisc'
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = os.environ.get('PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.environ.get('SECRET_KEY')
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Login Configuration


login_manager = LoginManager()
login_manager.init_app(app)


# Database Models

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    listing = relationship("Listing", back_populates="author")


class Listing(db.Model):
    __tablename__ = "listing"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String(100), nullable=False)
    about = db.Column(db.String(1000))
    date = db.Column(db.String(250), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    author = relationship('User', back_populates="listing")
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# ------------------------------------------------------------------


db.create_all()


# Login Loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/results/<query>/<page_number>', methods=['GET', 'POST'])
def results(query, page_number: int):
    name = get_place_name(query)
    result = []
    data = [
        search_kijiji.search_kijiji(place_name=name, page_number=page_number),
        search_centris.search_centris(place_name=name, rent_sale="rent"),
        search_zumper.search_zumper(place_name=name, page_number=page_number),
        search_dupropio.search_dupropio(place_name=name, page_number=page_number)
    ]
    page_number = int(page_number) + 1
    for info in data:
        if info is None:
            print("none called")
            pass
        else:
            result += info
    # result = shuffle(result)

    with open('data.json', 'w') as fp:
        json.dump(result, fp)
    try:
        size = len(result)
    except TypeError:
        size = 0
    return render_template("/result.html", results=result, len=size, searching_in=name,
                           logged_in=current_user.is_authenticated, page_number=page_number)


@app.route('/', methods=['GET', 'POST'])
def home():
    search_form = SearchForm()

    if search_form.validate_on_submit():
        return redirect(url_for('results', query=search_form.search.data, page_number=1))
    return render_template("/index.html", form=search_form, name=welcome_name(),
                           logged_in=current_user.is_authenticated)


# LOGIN SIGNUP
@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if request.method == "request":
        print("got hit")
    if login_form.validate():
        try:
            user = User.query.filter_by(email=login_form.email.data).first()
            if check_password_hash(user.password, login_form.password.data):
                print("login success")
                login_user(user)
                return redirect(url_for("home"))
            else:
                flash("Invalid Password")
        except AttributeError:
            flash("User Not Found")
    else:
        flash("Error")
    return render_template("login.html", form=login_form, name=welcome_name(),logged_in=current_user.is_authenticated)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignUpForm()
    if request.method == 'POST' and signup_form.validate_on_submit():
        print("got Post")
        new_user = User(
            name=signup_form.username.data,
            email=signup_form.email.data,
            password=generate_password_hash(signup_form.password.data, method="pbkdf2:sha256", salt_length=10)
        )
        db.session.add(new_user)
        db.session.commit()
        print("New user added")
        login_user(new_user)
        return redirect(url_for("home"))
    else:
        flash("Invalid Input Please Try Again")
    return render_template("signup.html", form=signup_form, name=welcome_name())


# ------------------------------------------------------------------

# Listing POST and SHOW
@app.route('/add-listing', methods=['GET', 'POST'])
@login_required
def add_listing():
    listing_form = PostListingForm()

    if listing_form.validate():
        new_listing = Listing(
            title=listing_form.title.data,
            url=listing_form.listing_url.data,
            about=listing_form.about.data,
            date=date.today(),
            address=listing_form.listing_address.data,
            price=listing_form.listing_price.data,
            img_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQZIaIUXwPa6Gq_"
                    "mLoGpGK35G7dVnH5-8Rx1A&usqp=CAU",
            author=current_user

        )
        db.session.add(new_listing)
        db.session.commit()
        print("Listing Added Successfully")
        return redirect(url_for('show_all'))

    return render_template("post-listing.html", form=listing_form, name=welcome_name(),logged_in=current_user.is_authenticated)


@app.route("/direct/<index>", methods=['GET', 'POST'])
@login_required
def direct_post(index):
    index = int(index)
    with open('data.json', 'r') as fp:
        post_info = json.load(fp)
    post_info = post_info[index]
    direct_form = PostListingDirectForm()
    if direct_form.validate_on_submit():
        new_listing = Listing(
            title=direct_form.title.data,
            url=post_info['url'],
            about=direct_form.about.data,
            date=date.today(),
            address=post_info['address'],
            price=post_info['price'],
            img_url=post_info['img_url'],
            author=current_user
        )
        db.session.add(new_listing)
        db.session.commit()
        print("Listing Added Successfully")
        return redirect(url_for('show_all'))

    return render_template("post-direct.html", form=direct_form, name=welcome_name(),logged_in=current_user.is_authenticated)


@app.route("/showlisting")
def show_all():
    return render_template("show-listing.html", listings=db.session.query(Listing).all(), name=welcome_name(),logged_in=current_user.is_authenticated)


@app.route("/deatil-listing/<id>", methods=['GET', 'POST'])
@login_required
def show_listing_detail(id):
    contact_form = ContactForm()
    display_listing = Listing.query.get(id)
    if contact_form.validate_on_submit():
        sender = User.query.get(current_user.id)
        message = contact_form.message.data.split(">")[1].split("<")[0]
        send_mail(current_user.email, message, sender.name, sender.email)
        return redirect(url_for("home"))
    return render_template("display-detail.html", listing=display_listing, form=contact_form,logged_in=current_user.is_authenticated)


# ------------------------------------------------------------------


@app.route('/showMyListings', methods=['GET', 'POST'])
@login_required
def ShowMyListings():
    listings = Listing.query.filter_by(author_id=current_user.id).all()
    user = User.query.get(current_user.id)
    length=len(listings)
    return render_template("showMyListings.html", listing=listings, user=user,length=length,logged_in=current_user.is_authenticated)


@app.route('/delete_listing<id>', methods=['GET', 'POST'])
@login_required
def delete_listing(id):
    listing = Listing.query.get(id)
    db.session.delete(listing)
    db.session.commit()
    return render_template('showMyListings.html',logged_in=current_user.is_authenticated)


def welcome_name() -> str:
    if current_user.is_authenticated:
        return User.query.get(current_user.id).name
    else:
        return ""




@app.errorhandler(401)
def unauthorized(*args):
    return render_template("unauthorized.html")

@app.errorhandler(404)
def notfound(*args):
    return render_template('NotFound.html')


if __name__ == '__main__':
    app.run(debug=True)

