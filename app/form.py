import wtforms
from wtforms.validators import DataRequired, Email, URL, Optional, Length, NumberRange


class MinBidanForm(wtforms.Form):
    shift_pagi_sn = wtforms.IntegerField('<strong>SHIFT PAGI</strong> - Senior (SN):', validators=[DataRequired()])

    shift_pagi_jr = wtforms.IntegerField('<strong>SHIFT PAGI</strong> - Junior (JR):', validators=[DataRequired()])

    shift_siang_sn = wtforms.IntegerField('<strong>SHIFT SIANG</strong> - Senior (SN):', validators=[DataRequired()])

    shift_siang_jr = wtforms.IntegerField('<strong>SHIFT SIANG</strong> - Junior (JR):', validators=[DataRequired()])

    shift_malam_sn = wtforms.IntegerField('<strong>SHIFT MALAM</strong> - Senior (SN):', validators=[DataRequired()])

    shift_malam_jr = wtforms.IntegerField('<strong>SHIFT MALAM</strong> - Junior (JR):', validators=[DataRequired()])

    section_min_bidan = wtforms.HiddenField('',validators=[DataRequired()], default='min_bidan')


class ProsesAlgoForm(wtforms.Form):
    generasi = wtforms.IntegerField('Generasi:', validators=[DataRequired()])

    populasi = wtforms.IntegerField('Populasi:', validators=[DataRequired()])

    prob_rekombinasi = wtforms.FloatField('Probabilitas Rekombinasi:', validators=[DataRequired(), NumberRange(min=0, max=1) ])

    prob_mutasi = wtforms.FloatField('Probabilitas Mutasi:', validators=[DataRequired(), NumberRange(min=0, max=1)])

    prob_local_search = wtforms.FloatField('Probabilitas Local Search:', validators=[DataRequired(), NumberRange(min=0, max=1)])

    section_proses_algo = wtforms.HiddenField('', validators=[DataRequired()], default='proses_algo')

