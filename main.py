#Importing required libraries/packages
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, URL 
import os

#Only for local environment
#from dotenv import load_dotenv
#load_dotenv("secrets.env")

#Creating a child class of Declarative Base
class Base(DeclarativeBase):
    pass

#Creating an add cafe form
class AddCafeForm(FlaskForm):
    name = StringField(label="Cafe Name", validators=[DataRequired()])
    map_url = StringField(label="Map URL", validators=[DataRequired(),URL()])
    img_url = StringField(label="Image URL", validators=[DataRequired(),URL()])
    location = StringField(label="Location",validators=[DataRequired()])
    has_sockets = IntegerField(label="Does it have sockets? '1' for 'Yes' and '0' for 'No'")
    has_toilet = IntegerField(label="Does it have toilet? '1' for 'Yes' and '0' for 'No'")
    has_wifi = IntegerField(label="Does it have wifi? '1' for 'Yes' and '0' for 'No'")
    can_take_calls = IntegerField(label="Can it take calls? '1' for 'Yes' and '0' for 'No'")
    seats = StringField(label="No. of seats", validators=[DataRequired()])
    coffee_price = StringField(label="Coffee price: e.g.(£3.00)", validators=[DataRequired()])

    submit = SubmitField(label="Add Cafe",validators=[DataRequired()])

#Creating a Flask app
app = Flask(__name__)

#Creating a bootstrap for styling website
bootstrap = Bootstrap5(app=app)

#Creating a secret key
app.config['SECRET_KEY'] = os.getenv("FLASK_KEY") #Create your own random key.e.g 'kjhgdvl'

#Creating a database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///cafes.db")
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Cafe(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    name:Mapped[str] = mapped_column(String, nullable=False)
    map_url:Mapped[str] = mapped_column(String,nullable=False)
    img_url:Mapped[str] = mapped_column(String,nullable=False)
    location:Mapped[str] = mapped_column(String,nullable=False)
    has_sockets:Mapped[int] = mapped_column(Integer,nullable=False)
    has_toilet:Mapped[int] = mapped_column(Integer,nullable=False)
    has_wifi:Mapped[int] = mapped_column(Integer,nullable=False)
    can_take_calls:Mapped[int] = mapped_column(Integer,nullable=False)
    seats:Mapped[str] = mapped_column(String,nullable=False)
    coffee_price:Mapped[str] = mapped_column(String,nullable=False)

with app.app_context():
    db.create_all()

#Creating routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/all_cafes")
def all_cafes():
    result = db.session.execute(db.select(Cafe))
    posts = result.scalars().all()
    return render_template("cafes.html", cafes=posts)

#Adding a new cafe to the database
@app.route("/add_cafe",methods=["POST","GET"])
def add_cafe():
    add_cafe_form = AddCafeForm()
    if add_cafe_form.validate_on_submit():
        new_cafe = Cafe(
            name = add_cafe_form.name.data,
            map_url =  add_cafe_form.map_url.data,
            img_url =  add_cafe_form.img_url.data,
            location =  add_cafe_form.location.data,
            has_sockets =  add_cafe_form.has_sockets.data,
            has_toilet =  add_cafe_form.has_toilet.data,
            has_wifi =  add_cafe_form.has_wifi.data,
            can_take_calls =  add_cafe_form.can_take_calls.data,
            seats =  add_cafe_form.seats.data,
            coffee_price = add_cafe_form.coffee_price.data
            )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("all_cafes"))

    return render_template("add.html", form=add_cafe_form)

#Editing an existing cafe
@app.route("/edit/<cafe_name>",methods=["POST","GET"])
def delete(cafe_name):
    result = db.session.execute(db.select(Cafe).where(Cafe.name == cafe_name))
    cafe = result.scalar()
    if cafe:
        db.session.delete(cafe)
        db.session.commit()

    return redirect(url_for('all_cafes'))

#Running the flask app
if __name__ == "__main__":
    app.run(debug=True)