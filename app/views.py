from app import app, db
from flask import render_template, flash  # , redirect, url_for, session, logging, request
# from  flask_mysqldb import MySQL
from models import Schedules, Bidan, Periode
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from memetika import nsp
import datetime

def create_schedule_db(periode_date):
    periode_baru = Periode(periode=periode_date)
    db.session.add(periode_baru)
    db.session.commit()
    for bdn in Bidan.query.all():
        sch = Schedules(periode_id=periode_baru.id,
                        bidan_id=bdn.id,
                        name=bdn.name,
                        nip=bdn.nip,
                        officer=bdn.officer,
                        tim=bdn.tim)
        db.session.add(sch)
    db.session.commit()


@app.route("/")
def homepage():
    return render_template('home.html')


@app.route("/penjadwalan/", methods=['GET', 'POST'])
def penjadwalan():
    return render_template('penjadwalan.html')


@app.route("/penjadwalan/<slug>/", methods=['GET', 'POST'])
def penjadwalan_proses(slug):
    meme = nsp()
    slug_date = slug.split("-")
    periode_date = datetime.date(int(slug_date[1]), int(slug_date[0]), 1);
    periode_db = Periode.query.filter(Periode.periode == periode_date).first()
    if not periode_db:
        create_schedule_db(periode_date)
        meme.generate_pattern_schedule(periode_date)
    else:
        sch = Schedules.query.filter(Schedules.periode_id == periode_db.id).first()
        if not sch.rest_shift or sch.rest_shift == "":
            meme.generate_pattern_schedule(periode_date)


    table = {"kr": Bidan.query.filter(Bidan.officer == "KR").first(),
             "kt1": Bidan.query.filter((Bidan.officer == "KT") & (Bidan.tim == "tim1")).first(),
             "kt2": Bidan.query.filter((Bidan.officer == "KT") & (Bidan.tim == "tim2")).first(),
             "tim1": Bidan.query.filter((Bidan.tim == "tim1") & (Bidan.officer != "KT")).order_by(Bidan.id.asc()).all(),
             "tim2": Bidan.query.filter((Bidan.tim == "tim2") & (Bidan.officer != "KT")).order_by(Bidan.id.asc()).all()}
    return render_template('penjadwalan.html', table=table, periode=slug)
