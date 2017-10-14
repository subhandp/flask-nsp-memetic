from app import app, db
from flask import render_template, request, abort , flash # , redirect, url_for, session, logging, request
from models import Schedules, Bidan, Periode
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from nsp import generate_pattern_schedule, Memetic
from form import MinBidanForm, ProsesAlgoForm
import datetime, json, calendar, os
import ConfigParser

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

def shift_list(obj):

    new_obj = []
    for result in obj:
        temp_obj = {}
        temp_obj["id"] = result.id
        temp_obj["name"] = result.name
        temp_obj["officer"] = result.officer
        temp_obj["tim"] = result.tim
        temp_obj["nip"] = result.nip

        shift = ''.join(result.shift.split())
        if shift != "" and shift != "CLEAR":
            temp_obj["shift"] = result.shift.split(",")
        else:
            temp_obj["shift"] = None

        rest_shift = ''.join(result.rest_shift.split())
        if rest_shift != "" and rest_shift != "CLEAR":
            temp_obj["rest_shift"] = result.rest_shift.split(",")
        else:
            temp_obj["rest_shift"] = None

        temp_obj["schedule_id"] = result.schedule_id
        new_obj.append(temp_obj)

    #print(json.dumps(new_obj, indent=4, sort_keys=False))
    return  new_obj


def schedulling_setting(action='get', data = None):
    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
    path_config = '%s/nsp.ini' % APPLICATION_DIR
    config = ConfigParser.ConfigParser()
    config.read(path_config)
    if action == "get":
        config_data = {}
        for (key, val) in config.items(data):
            config_data[key] = val
        return config_data
    elif action == "set":
        for options, value in data["data"].items():
            config.set(data["section"], options, value)

        with open(path_config, 'wb') as configfile:
            config.write(configfile)


@app.route("/", methods=['GET', 'POST'])
def homepage():

    table_query = Schedules.query \
        .join(Periode) \
        .add_columns(Schedules.id.label("schedule_id"), Schedules.officer, Schedules.nip, Schedules.name, Schedules.shift, Schedules.rest_shift, Schedules.tim, Periode.id, Periode.periode)

    table_periode = table_query.order_by(Periode.periode.desc()).group_by(Periode.periode).all()
    list_periode = []
    for periode in table_periode:
        pr = {}
        pr["id"] = periode.periode.strftime("%Y-%m-%d")
        pr["periode"] = periode.periode.strftime("%B %Y")
        list_periode.append(pr)

    if request.method == 'POST':
        periode_periode = request.form["select-periode"]
    else:
        periode_periode = list_periode[0]["id"]

    periode_split = periode_periode.split("-")
    periode_date = datetime.date(int(periode_split[0]), int(periode_split[1]), 1)
    days = calendar.monthrange(periode_date.year, periode_date.month)[1]

    periode_schedule = {"kr": shift_list(table_query.filter(Schedules.officer == "KR").filter(Periode.periode == periode_date).all()),
             "kt1": shift_list(table_query.filter((Schedules.officer == "KT") & (Schedules.tim == "tim1")).filter(Periode.periode == periode_date).all()),
             "kt2": shift_list(table_query.filter((Schedules.officer == "KT") & (Schedules.tim == "tim2")).filter(Periode.periode == periode_date).all()),
             "tim1": shift_list(table_query.filter((Schedules.tim == "tim1") & (Schedules.officer != "KT")).filter(Periode.periode == periode_date).order_by(Schedules.bidan_id.asc()).all()),
             "tim2": shift_list(table_query.filter((Schedules.tim == "tim2") & (Schedules.officer != "KT")).filter(Periode.periode == periode_date).order_by(Schedules.bidan_id.asc()).all())}

    # print(json.dumps(periode_schedule, indent=4, sort_keys=False))
    return render_template('home.html', periode=list_periode, table=periode_schedule, periode_value=periode_periode, days=days)


@app.route("/penjadwalan/", methods=['GET', 'POST'])
def penjadwalan():
    return render_template('penjadwalan.html')


@app.route("/penjadwalan/<slug>/", methods=['GET', 'POST'])
def penjadwalan_proses(slug):
    try:
        days = 0
        slug_date = slug.split("-")
        periode_date = datetime.date(int(slug_date[1]), int(slug_date[0]), 1)
        table_query = Bidan.query \
            .join(Schedules) \
            .join(Periode) \
            .add_columns(Bidan.id, Bidan.name, Bidan.officer, Bidan.tim, Bidan.nip, Schedules.shift,
                         Schedules.rest_shift, Schedules.id.label("schedule_id")) \
            .filter(Periode.periode == periode_date)
        if periode_date:
            days = calendar.monthrange(periode_date.year, periode_date.month)[1]
            periode_db = Periode.query.filter(Periode.periode == periode_date).first()
            if not periode_db:
                create_schedule_db(periode_date)
                generate_pattern_schedule(periode_date)
            else:
                sch = Schedules.query.filter(Schedules.periode_id == periode_db.id).first()
                if not sch.rest_shift or sch.rest_shift == "":
                    generate_pattern_schedule(periode_date)

            if request.method == 'POST':
                if request.json:
                    if request.json['ajax'] == 'generate-jadwal':
                        with open("scheduling_process.txt", "wb") as fo:
                            fo.write("true")

                        min_bidan = schedulling_setting('get', 'min_bidan')
                        setting_algoritma = schedulling_setting('get', 'memetika')
                        init_data = min_bidan.copy()
                        init_data.update(setting_algoritma)
                        init_data["days"] = days
                        init_data["periode_id"] = periode_db.id

                        meme = Memetic(init_data)
                        meme.initial_populasi()
                        for generasi in range(meme.generasi):
                            meme.fitness()
                            meme.selection()
                            meme.recombination()
                            meme.mutation()
                            meme.local_search()
                            meme.population_replacement()
                            if meme.termination(generasi):
                                with open("scheduling_process.txt", "wb") as fo:
                                    fo.write("false")
                                break

                        meme.detail_solusi()
                        return json.dumps({'status': 'OK'});
                    elif request.json['ajax'] == 'stop-generate-jadwal':
                        with open("scheduling_process.txt", "wb") as fo:
                            fo.write("false")
                    elif request.json['ajax'] == 'get-rest-shift':
                        try:
                            rest_req = shift_list(table_query.filter(Schedules.id == request.json['schedule_id']).all())
                            return json.dumps({'status': 'OK', 'days': days, 'res_data': rest_req})
                        except Exception as e:
                            return json.dumps({'status': 'ERROR', 'res_data': e})
                elif request.form:
                    print request.form.getlist("rest-shift")

    except Exception as e:
        print e
        abort(404)

    table = {"kr": shift_list(table_query.filter(Bidan.officer == "KR").all()),
             "kt1": shift_list(table_query.filter((Bidan.officer == "KT") & (Bidan.tim == "tim1")).all()),
             "kt2": shift_list(table_query.filter((Bidan.officer == "KT") & (Bidan.tim == "tim2")).all()),
             "tim1": shift_list(table_query.filter((Bidan.tim == "tim1") & (Bidan.officer != "KT")).order_by(Bidan.id.asc()).all()),
             "tim2": shift_list(table_query.filter((Bidan.tim == "tim2") & (Bidan.officer != "KT")).order_by(Bidan.id.asc()).all())}

    return render_template('penjadwalan.html', table=table, periode=periode_db, days=days)


@app.route("/setting/", methods=['GET', 'POST'])
def setting():
    min_bidan_data = schedulling_setting('get', 'min_bidan')
    proses_algo_data = schedulling_setting('get', 'memetika')
    min_bidan_form = MinBidanForm(data=min_bidan_data)
    proses_algo_form = ProsesAlgoForm(data=proses_algo_data)
    if request.method == 'POST':
        if 'section_min_bidan' in request.form:
            min_bidan_form = MinBidanForm(request.form)
            if min_bidan_form.validate():
                schedulling_setting("set", {"section": 'min_bidan', "data": request.form})
                flash('Batasan penjadwalan berhasil diubah.', 'success')
        elif 'section_proses_algo' in request.form:
            proses_algo_form = ProsesAlgoForm(request.form)
            if proses_algo_form.validate():
                schedulling_setting("set", {"section": 'memetika', "data": request.form})
                flash('Proses algoritma berhasil diubah.', 'success')

    return render_template('setting.html', min_bidan_form=min_bidan_form, proses_algo_form=proses_algo_form)