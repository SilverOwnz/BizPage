from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Email, Length, DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ThisIsSupposedToBeSecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True)
    description = db.Column(db.String(500))
    hoursMon = db.Column(db.String(50))
    hoursTues = db.Column(db.String(50))
    hoursWed = db.Column(db.String(50))
    hoursThurs = db.Column(db.String(50))
    hoursFri = db.Column(db.String(50))
    hoursSat = db.Column(db.String(50))
    hoursSun = db.Column(db.String(50))
    address = db.Column(db.String(100))
    atmosphere = db.Column(db.String(25))
    paymentMode = db.Column(db.String(20))


class forms(FlaskForm):
    name = StringField('ShopName', validators=[InputRequired()])
    email = StringField('UserEmail', validators=[InputRequired(), Email(message="invalid email"), Length(max=50)])
    description = StringField('ShopDescription')
    hoursMon = StringField('shophoursMon',)
    hoursTues = StringField('shophoursTues')
    hoursWed = StringField('shophoursWed')
    hoursThurs = StringField('shophoursThurs')
    hoursFri = StringField('shophoursFri')
    hoursSat = StringField('shophoursSat')
    hoursSun = StringField('shophoursSun')
    address = StringField('shopAddress', validators=[InputRequired()])
    atmosphere = StringField('shopAtmosphere', validators=[InputRequired()])
    paymentMode = StringField('shoppaymentMode', validators=[InputRequired()])
    submit = SubmitField('Submit')

@app.route('/listings')
def listing():
    all_listing = Listing.query.all()
    return render_template('listings.html', list=all_listing)


@app.route('/listings/<shopname>')
def shop(shopname):
    shop = Listing.query.filter_by(name=shopname).first()
    return render_template('Shop.html', shop=shop)


@app.route('/form', methods=['GET', 'POST'])
def add_form():
    form = forms()
    if form.validate_on_submit():
        listing = Listing(name=form.name.data, description=form.description.data, hoursMon=form.hoursMon.data, hoursTues=form.hoursTues.data, hoursWed=form.hoursWed.data, hoursThurs=form.hoursThurs.data, hoursFri=form.hoursFri.data, hoursSat=form.hoursSat.data, hoursSun=form.hoursSun.data, address=form.address.data, atmosphere=form.atmosphere.data, paymentMode=form.paymentMode.data)
        db.session.add(listing)
        db.session.commit()
        return redirect(url_for('listing'))

    return render_template('form.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)

