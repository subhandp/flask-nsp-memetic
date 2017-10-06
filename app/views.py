from app import app

from flask import render_template, flash #, redirect, url_for, session, logging, request
#from  flask_mysqldb import MySQL
from models import Pattern_rest_schedules, Bidan
from wtforms import Form, StringField,TextAreaField, PasswordField, validators

#mysql = MySQL(app)

@app.route("/")
def homepage():
    return render_template('home.html')


@app.route("/penjadwalan/", methods=['GET', 'POST'])
def penjadwalan():

    table = {"kr": Bidan.query.filter(Bidan.officer == "KR").first(), "kt1": Bidan.query.filter( (Bidan.officer == "KT") &  (Bidan.tim == "tim1") ).first() ,
             "kt2": Bidan.query.filter( (Bidan.officer == "KT") &  (Bidan.tim == "tim2") ).first(),
             "tim1": Bidan.query.filter((Bidan.tim == "tim1") & (Bidan.officer != "KT") ).order_by(Bidan.id.asc()).all(),
             "tim2": Bidan.query.filter( (Bidan.tim == "tim2") & (Bidan.officer != "KT") ).order_by(Bidan.id.asc()).all()}
    return render_template('penjadwalan.html', table=table)