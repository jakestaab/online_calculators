from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, SelectField, IntegerField
from nec_lib import NECTables as NEC

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
    form = VD_Form()
    if form.is_submitted():
        mtrl = float(request.form.get(material))
        phs = float(request.form.get(phase))
        sz = str(request.form.get(size))
        lngth = int(request.form.get(length))
        crnt = int(request.form.get(current))
        vltg = int(request.form.get(voltage))

        numerator = (phs * mtrl * lngth * crnt)
        denominator = NEC.awg_to_circmils[sz]
        resulting_voltage = vltg - (numerator / denominator)
        percentage = resulting_voltage / vltg
        final = round(((1 - percentage) * 100), 3)

        return final
    else:
        return 0


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def voltage_drop():
    form = VD_Form()
    vd_percent = get_voltage_drop('material', 'phase', 'size', 'length', 'current', 'voltage')
    return render_template('index.html', form=form, vd=vd_percent)




if __name__ == '__main__':
    app.run(debug=True)
