from flask import Flask, render_template
from forms import VD_Form, CF_Form, WS_Form

app = Flask(__name__)
app.config['SECRET_KEY'] = '987kjhgh(*Lz4d09wfh'


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

