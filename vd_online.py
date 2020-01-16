from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, SelectField, IntegerField
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '987kjhgh(*Lz4d09wfh'

class VD_Form(FlaskForm):
    material = RadioField('Material', choices=[(12.9, "CU"), (21.2, "AL")])
    phase = RadioField('Phase', choices=[(2, "1"), (1.732, "3")])
    size = SelectField('Conductor Size', choices=[(10,10),(8,8),(6,6)])
    length = IntegerField('length')
    current = IntegerField('current')
    voltage = IntegerField('voltage')
    submit = SubmitField("Calculate VD")


def get_voltage_drop(material, phase, size, length, current, voltage):
    mtrl = request.form.get(material)
    phs = request.form.get(phase)
    sz = request.form.get(size)
    lngth = request.form.get(length)
    crnt = request.form.get(current)
    vltg = request.form.get(voltage)

    numerator = (phs * mtrl * crnt * lngth)


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def voltage_drop():
    form = VD_Form()
    mate = get_voltage_drop('material')
    return render_template('index.html', form=form, mate=mate)







if __name__ == '__main__':
    app.run(debug=True)
