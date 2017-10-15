from flask_admin import Admin
from app import app, db
from flask_admin.contrib.sqla import ModelView
from models import Schedules, Bidan, Periode, User
from wtforms.fields import SelectField, PasswordField
from flask_admin.menu import MenuLink
from flask_admin import AdminIndexView, expose
from flask import g, url_for, request, redirect

class AdminAuthentication(object):
    def is_accessible(self):
        return g.user.is_authenticated

class BaseModelView(AdminAuthentication, ModelView):
    pass

class IndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not (g.user.is_authenticated):
            return redirect(url_for('login', next=request.path))
        return self.render('admin/index.html')

class UserModelView(BaseModelView):
    column_filters = ['username']
    column_list = ['username', 'created_timestamp']
    column_searchable_list = ['username']

    form_columns = ['username', 'password']
    form_extra_fields = {
        'password': PasswordField('New password')
    }

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password_hash = User.make_password(form.password.data)
        return super(UserModelView, self).on_model_change(
            form, model, is_created
        )

class SchedulesModelView(BaseModelView):
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

class PeriodeModelView(BaseModelView):
    column_searchable_list = ['periode']
    form_columns = ['periode']


class BidanModelView(BaseModelView):

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




admin = Admin(app, 'Penjadwalan Administrator', index_view=IndexView())
admin.add_view(BidanModelView(Bidan, db.session))
admin.add_view(PeriodeModelView(Periode, db.session))
admin.add_view(SchedulesModelView(Schedules, db.session))
admin.add_view(UserModelView(User, db.session))
admin.add_link(MenuLink(name='Dashboard', category='', url="/"))
admin.add_link(MenuLink(name='Logout', category='', url="/logout/"))