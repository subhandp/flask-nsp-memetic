from app import app, db
from flask import render_template, request, abort  # , redirect, url_for, session, logging, request
from models import Schedules, Bidan, Periode
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from nsp import generate_pattern_schedule, Memetic
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

    try:
        slug_date = slug.split("-")
        periode_date = datetime.date(int(slug_date[1]), int(slug_date[0]), 1)
        if periode_date:
            periode_db = Periode.query.filter(Periode.periode == periode_date).first()
            if not periode_db:
                create_schedule_db(periode_date)
                generate_pattern_schedule(periode_date)
            else:
                sch = Schedules.query.filter(Schedules.periode_id == periode_db.id).first()
                if not sch.rest_shift or sch.rest_shift == "":
                    generate_pattern_schedule(periode_date)

            if request.method == 'POST':
                if request.json['ajax'] == 'generate-jadwal':
                    if request.method == 'POST':
                        if request.json['ajax'] == 'generate-jadwal':
                            print "GENERATE JADWAL"
                            meme = Memetic()
                            meme.initial_populasi()
                            for generasi in range(meme.generasi):
                                meme.fitness()
                                meme.selection()
                                meme.recombination()
                                meme.mutation()
                                meme.local_search()
                                meme.population_replacement()
                                if meme.termination(generasi):
                                    break

                            meme.detail_solusi()

    except Exception as e:
        abort(404)


    # if request.method == 'POST':
    #     if request.json['ajax'] == 'generate-jadwal':
    #         print "GENERATE JADWAL"
    #         meme = Memetic()
    #         meme.initial_populasi()
    #         for generasi in range(meme.generasi):
    #             meme.fitness()
    #             meme.selection()
    #             meme.recombination()
    #             meme.mutation()
    #             meme.local_search()
    #             meme.population_replacement()
    #             if meme.termination(generasi):
    #                 break
    #
    #         meme.detail_solusi()

    table_query = Bidan.query\
            .join(Schedules)\
            .join(Periode)\
            .add_columns(Bidan.id, Bidan.name, Bidan.officer, Bidan.tim, Bidan.nip, Schedules.rest_shift, Schedules.id)\
            .filter(Periode.periode == periode_date)\

    table = {"kr": table_query.filter(Bidan.officer == "KR").first(),
             "kt1": table_query.filter((Bidan.officer == "KT") & (Bidan.tim == "tim1")).first(),
             "kt2": table_query.filter((Bidan.officer == "KT") & (Bidan.tim == "tim2")).first(),
             "tim1": table_query.filter((Bidan.tim == "tim1") & (Bidan.officer != "KT")).order_by(Bidan.id.asc()).all(),
             "tim2": table_query.filter((Bidan.tim == "tim2") & (Bidan.officer != "KT")).order_by(Bidan.id.asc()).all()}
    return render_template('penjadwalan.html', table=table, periode=periode_db)
