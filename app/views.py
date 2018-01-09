from app import app, db, LoginManager
from flask import render_template, request, abort , flash, redirect, url_for, session, logging, request
from models import Schedules, Bidan, Periode
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from nsp import generate_pattern_schedule, Memetic
from form import MinBidanForm, ProsesAlgoForm, LoginForm
from flask_login import login_user, logout_user, login_required
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



def get_hours_total(temp_obj):
    total_jam_kerja = 0
    p, s, m = 6, 6, 12
    total_rest = 0
    if temp_obj['rest_shift'] is not None:
        total_rest = len(temp_obj['rest_shift'])
        total_jam = 0
        for hari, shift in enumerate(temp_obj['rest_shift']):
            if shift == "P":
                total_jam = total_jam + p
            elif shift == "S":
                total_jam = total_jam + s
            elif shift == "M":
                total_jam = total_jam + m
            elif shift == "-" and temp_obj['shift'] is not None:
                shift = temp_obj["shift"][hari]
                if shift == "P":
                    total_jam = total_jam + p
                elif shift == "S":
                    total_jam = total_jam + s
                elif shift == "M":
                    total_jam = total_jam + m
        total_jam_kerja += total_jam
    elif temp_obj['shift'] is not None:
        total_jam = 0
        for hari, shift in enumerate(temp_obj['shift']):
            if shift == "P":
                total_jam = total_jam + p
            elif shift == "S":
                total_jam = total_jam + s
            elif shift == "M":
                total_jam = total_jam + m

        total_jam_kerja += total_jam


    return total_jam_kerja


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

        temp_obj['total_jam_kerja'] = get_hours_total(temp_obj)

        temp_obj["schedule_id"] = result.schedule_id
        new_obj.append(temp_obj)

    return new_obj


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


def log_n_save_proses_result(data, slug, days, periode_id):
    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
    path_config = '%s/log_proses_result.txt' % APPLICATION_DIR
    with open(path_config, "wb") as fo:
        fo.write("PERIODE: %s\n" % slug)
        fo.write("TOTAL HARI: %d\n" % days)
        fo.write("WAKTU EKSEKUSI: %s\n" % data["execution_time"])
        fo.write("TERMINASI: %s\n" % data["msg"])
        fo.write("GENERASI: %d\n" % data["generasi"])
        fo.write("FITNESS: %f\n" % data["elit_fitness"])
        fo.write("TOTAL PELANGGARAN: %d\n" % data["total_pelanggaran"])
        fo.write("DETAIL: \n")
        for jenis, total in data["pelanggaran"].items():
            wrt = "---%s: %d\n" % (jenis, total)
            fo.write(wrt)

    sch_query = Schedules.query.filter(Schedules.periode_id == periode_id)
    for id, shift_individu in data["individu"].items():
        bidan_shift = sch_query.filter(Schedules.bidan_id == id).first()
        bidan_shift.shift = ",".join(shift_individu)
        db.session.commit()

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


    kt = [shift_list(table_query.filter((Schedules.officer == "KT") & (Schedules.tim == "tim1")).filter(Periode.periode == periode_date).all()),
          shift_list(table_query.filter((Schedules.officer == "KT") & (Schedules.tim == "tim2")).filter(Periode.periode == periode_date).all()),
          shift_list(table_query.filter((Schedules.officer == "KT") & (Schedules.tim == "tim3")).filter(Periode.periode == periode_date).all())]

    tim = [shift_list(table_query.filter((Schedules.tim == "tim1") & (Schedules.officer != "KT")).filter(Periode.periode == periode_date).order_by(Schedules.bidan_id.asc()).all()),
           shift_list(table_query.filter((Schedules.tim == "tim2") & (Schedules.officer != "KT")).filter(Periode.periode == periode_date).order_by(Schedules.bidan_id.asc()).all()),
           shift_list(table_query.filter((Schedules.tim == "tim3") & (Schedules.officer != "KT")).filter(Periode.periode == periode_date).order_by(Schedules.bidan_id.asc()).all())]

    persir = shift_list(table_query.filter(Schedules.officer == "persir").order_by(Schedules.id.asc()).filter(Periode.periode == periode_date).all())

    periode_schedule = {"kr": shift_list(table_query.filter(Schedules.officer == "KR").filter(Periode.periode == periode_date).all()),
                        "kt": kt, "tim": tim, "persir": persir}

    # print(json.dumps(periode_schedule, indent=4, sort_keys=False))
    return render_template('home.html', periode=list_periode, table=periode_schedule, periode_value=periode_periode, days=days)


@app.route("/penjadwalan/", methods=['GET', 'POST'])
@login_required
def penjadwalan():
    return render_template('penjadwalan.html')


@app.route("/penjadwalan/<slug>/", methods=['GET', 'POST'])
@login_required
def penjadwalan_proses(slug):
    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
    path_config = '%s/log_proses_result.txt' % APPLICATION_DIR
    logs = [line.rstrip('\n') for line in open(path_config)]

    with open("scheduling_process.txt", "wb") as fo:
        fo.write("false")
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

        ahads = []
        for d in range(days):
            if datetime.date(periode_date.year, periode_date.month, d+1).weekday() == 6:
                ahads.append(d)

        periode_db = Periode.query.filter(Periode.periode == periode_date).first()
        if not periode_db:
            create_schedule_db(periode_date)

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
                    init_data["ahads"] = ahads

                    meme = Memetic(init_data)
                    meme.initial_populasi()
                    for generasi in range(meme.generasi):
                        meme.fitness()
                        meme.selection()
                        meme.recombination()
                        meme.mutation()
                        meme.local_search()
                        meme.population_replacement()
                        terminasi = meme.termination(generasi)
                        if terminasi["stop"]:
                            log_n_save_proses_result(terminasi["data"], slug, days, periode_db.id)
                            break
                    meme.detail_solusi()
                    return json.dumps({'status': 'OK'})

                elif request.json['ajax'] == 'stop-generate-jadwal':
                    with open("scheduling_process.txt", "wb") as fo:
                        fo.write("false")

                elif request.json['ajax'] == 'get-rest-shift':
                    rest_req = shift_list(table_query.filter(Schedules.id == request.json['schedule_id']).all())
                    return json.dumps({'status': 'OK', 'days': days, 'res_data': rest_req})

                elif request.json['ajax'] == 'generate-rest-jadwal':
                    result = generate_pattern_schedule(periode_date, days)
                    if result:
                        flash('Rest jadwal berhasil digenerate.', 'success')
                    else:
                        flash('Rest jadwal gagal digenerate, acuan jadwal tidak ditemukan.', 'danger')
                    return json.dumps({'status': 'OK'})

                elif request.json['ajax'] == 'clears-schedule':
                    current_schedule = Schedules.query.filter(Schedules.periode_id == periode_db.id).all()
                    if request.json['schedule']:
                        for sch in current_schedule:
                            sch.shift = ""
                    if request.json['rest_schedule']:
                        for sch in current_schedule:
                            sch.rest_shift = "CLEAR"

                    db.session.commit()
                    flash('Jadwal berhasil dibersihkan.', 'success')
                    return json.dumps({'status': 'OK'})

                elif request.json['ajax'] == 'get-detail-min-bidan':
                    hari = int(request.json['hari'])
                    pagi, siang, malam = [], [], []
                    current_schedule = table_query.filter(Bidan.officer != "persir").all()
                    counter = 0
                    for sch in current_schedule:
                        counter += 1
                        t = {"no":counter, "officer": sch.officer, "nama": sch.name, "nip": sch.nip}

                        if sch.rest_shift != "CLEAR":
                            temp_shift = sch.rest_shift.split(",")

                            if temp_shift[hari] == "-":
                                if sch.shift != "":
                                    temp_shift = sch.shift.split(",")
                        else:
                            if sch.shift != "":
                                temp_shift = sch.shift.split(",")

                        if temp_shift[hari] == "P":
                            pagi.append(t)
                        elif temp_shift[hari] == "S":
                            siang.append(t)
                        elif temp_shift[hari] == "M":
                            malam.append(t)


                    return json.dumps({'status': 'OK', 'pagi': pagi, 'siang': siang, 'malam': malam})

            elif request.form:
                if 'rest_schedule_id' in request.form:
                    rest_schedule_id = int(request.form["rest_schedule_id"])
                    bidan_name = str(request.form["bidan-name"]).upper()
                    rest_shift = request.form.getlist("rest-shift")
                    null_rest = True
                    for shift in rest_shift:
                        if shift != '-':
                            null_rest = False

                    if null_rest:
                        rest_str = "CLEAR"
                    else:
                        rest_str = ",".join(str(i) for i in rest_shift)

                    print rest_str

                    rest_db = Schedules.query.filter(Schedules.id == rest_schedule_id).first()
                    rest_db.rest_shift = rest_str
                    db.session.commit()
                    flash('%s, rest jadwal berhasil diubah.' % bidan_name, 'success')


    kt = [shift_list(table_query.filter((Bidan.officer == "KT") & (Bidan.tim == "tim1")).all()),
          shift_list(table_query.filter((Bidan.officer == "KT") & (Bidan.tim == "tim2")).all()),
          shift_list(table_query.filter((Bidan.officer == "KT") & (Bidan.tim == "tim3")).all())]

    tim = [shift_list(table_query.filter((Bidan.tim == "tim1") & (Bidan.officer != "KT")).order_by(Bidan.id.asc()).all()),
           shift_list(table_query.filter((Bidan.tim == "tim2") & (Bidan.officer != "KT")).order_by(Bidan.id.asc()).all()),
           shift_list(table_query.filter((Bidan.tim == "tim3") & (Bidan.officer != "KT")).order_by(Bidan.id.asc()).all())]

    persir = shift_list(table_query.filter(Bidan.officer == "persir").order_by(Bidan.id.asc()).all())

    table = {"kr": shift_list(table_query.filter(Bidan.officer == "KR").all()), "kt": kt, "tim": tim, "persir": persir}

    return render_template('penjadwalan.html', table=table, periode=periode_db, days=days, scheduling_process=logs)


@app.route("/setting/", methods=['GET', 'POST'])
@login_required
def setting():
    min_bidan_data = schedulling_setting('get', 'min_bidan')
    proses_algo_data = schedulling_setting('get', 'memetika')
    min_bidan_form = MinBidanForm(data=min_bidan_data)
    proses_algo_form = ProsesAlgoForm(data=proses_algo_data)
    if request.method == 'POST':
        if 'section_proses_algo' in request.form:
            proses_algo_form = ProsesAlgoForm(request.form)
            if proses_algo_form.validate():
                schedulling_setting("set", {"section": 'memetika', "data": request.form})
                flash('Proses algoritma berhasil diubah.', 'success')

    return render_template('setting.html', min_bidan_form=min_bidan_form, proses_algo_form=proses_algo_form)

@app.route("/logout/")
def logout():
    logout_user()
    flash("Anda berhasil logged out.", "success")
    return redirect(request.args.get('next') or url_for('homepage'))

@app.route("/login/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        form = LoginForm(request.form)
        if form.validate():
            # login_user helpers flask-login setting correct session
            login_user(form.user, remember=form.remember_me.data)
            flash("%s anda berhasil logged in." % form.user.username, "success")
            return redirect(request.args.get("next") or url_for("homepage"))
    else:
        form = LoginForm()

    return render_template("login.html", login_form=form)