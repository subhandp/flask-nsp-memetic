from flask_admin import Admin
from app import app, db
from flask_admin.contrib.sqla import ModelView
from models import Schedules, Bidan, Periode
from wtforms.fields import SelectField


class SchedulesModelView(ModelView):
    column_searchable_list = ['name']
    column_filters = ['name', 'periode']
    column_list = ['name', 'nip', 'officer', 'tim', 'shift', 'rest_shift', 'periode']
    form_columns = ['name', 'nip', 'officer', 'tim', 'shift', 'rest_shift', 'periode']
    _tim_choices = [(choice, label) for choice, label in [
        ('none', 'None'),
        ('tim1', 'Tim 1'),
        ('tim2', 'Tim 2'),
    ]]

    _officer_choices = [(choice, label) for choice, label in [
        ('KR', 'Kepala Ruangan (KR)'),
        ('KT', 'Kepala Tim (KT)'),
        ('SN', 'Senior (SN)'),
        ('JR', 'Junior (JR)'),
    ]]

    column_choices = {
        'tim': _tim_choices,
        'officer': _officer_choices
    }

    form_choices = {
        'tim': _tim_choices,
        'officer': _officer_choices
    }

class PeriodeModelView(ModelView):
    column_searchable_list = ['periode']
    form_columns = ['periode']


class BidanModelView(ModelView):

    column_searchable_list = ['nip', 'name']
    column_list = ['name', 'nip', 'officer', 'tim']
    form_columns = ['name', 'nip', 'officer', 'tim']
    column_filters = ['tim', 'name', 'officer']

    _tim_choices = [(choice, label) for choice, label in [
        ('none', 'None'),
        ('tim1', 'Tim 1'),
        ('tim2', 'Tim 2'),
    ]]

    _officer_choices = [(choice, label) for choice, label in [
        ('KR', 'Kepala Ruangan (KR)'),
        ('KT', 'Kepala Tim (KT)'),
        ('SN', 'Senior (SN)'),
        ('JR', 'Junior (JR)'),
    ]]

    column_choices = {
        'tim': _tim_choices,
        'officer': _officer_choices
    }

    form_choices = {
        'tim': _tim_choices,
        'officer': _officer_choices
    }




admin = Admin(app, 'Blog Admin')
admin.add_view(BidanModelView(Bidan, db.session))
admin.add_view(PeriodeModelView(Periode, db.session))
admin.add_view(SchedulesModelView(Schedules, db.session))
