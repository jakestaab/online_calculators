from flask import Flask, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, SelectField, IntegerField


app = Flask(__name__)
app.config['SECRET_KEY'] = '987kjhgh(*Lz4d09wfh'


class VD_Form(FlaskForm):
    material = RadioField('Material', choices=[(12.9, 'CU'), (21.2, 'AL')])
    phase = RadioField('Phase', choices=[(2, '1'), (1.732, '3')])
    size = SelectField('Conductor Size', choices=[(10,10), (8,8), (6,6)])
    length = IntegerField('Length')
    current = IntegerField('Current')
    voltage = IntegerField('Voltage')
    submit = SubmitField('Calculate VD')


class CF_Form(FlaskForm):
    size = SelectField('Conductor Size', choices=[('10','10'),('8','8'),('6','6')])
    number = IntegerField('No. of Conductors')
    insulation = SelectField('Ins. Type', choices=[('PV','PV'),('THHN','THHN')])
    ground = SelectField('Ground Size', choices=[('10','10'),('8','8'),('6','6')])
    conduit = SelectField('Conduit Type', choices=[('EMT','EMT'),('PVC','PVC')])
    submit = SubmitField('Calculate Size')


class WS_Form(FlaskForm):
    current = IntegerField('Current')
    number = IntegerField('No. of Conductors')
    insulation = SelectField('Ins. Type', choices=[('PV', 'PV'), ('THHN', 'THHN')])
    temperature = IntegerField('Amb. Temp. (F)')
    continuous = RadioField('Phase', choices=[(1.25, 'Yes'), (1, 'No')])
    submit = SubmitField('Calculate Size')


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    vd_form = VD_Form()
    vd_percent = get_voltage_drop('material', 'phase', 'size', 'length', 'current', 'voltage')
    return render_template('index.html', vd_form=vd_form, vd=vd_percent)

@app.route("/conduitfill", methods=['GET', 'POST'])
def conduitfill():
    cf_form = CF_Form()
    c_fill = get_conduit_size('size', 'number', 'insulation', 'ground', 'conduit')
    return render_template('conduitfill.html', cf_form=cf_form, c_fill=c_fill)

@app.route("/wiresize", methods=['GET', 'POST'])
def wiresize():
    ws_form = WS_Form()
    w_size = get_wire_size('current', 'number', 'insulation', 'temperature', 'continuous')
    return render_template('wiresize.html', ws_form=ws_form, w_size=w_size)

from calculators import get_voltage_drop
from calculators import get_conduit_size
from calculators import get_wire_size

if __name__ == '__main__':
    app.run(debug=True)
