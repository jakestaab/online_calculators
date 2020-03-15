from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, SelectField, IntegerField
from nec_lib import AWGlist


class VD_Form(FlaskForm):
    material = RadioField('Material', choices=[(12.9, 'CU'), (21.2, 'AL')])
    phase = RadioField('Phase', choices=[(2, '1'), (1.732, '3')])
    size = SelectField('Conductor Size', choices=AWGlist)
    length = IntegerField('Length')
    current = IntegerField('Current')
    voltage = IntegerField('Voltage')
    submit = SubmitField('Calculate VD')


class CF_Form(FlaskForm):
    size = SelectField('Conductor Size', choices=AWGlist)
    number = IntegerField('No. of Conductors')
    insulation = SelectField('Ins. Type', choices=[('PV','PV'),('THHN','THHN')])
    ground = SelectField('Ground Size', choices=AWGlist)
    conduit = SelectField('Conduit Type', choices=[('EMT','EMT'),('PVC','PVC')])
    submit = SubmitField('Calculate Size')


class WS_Form(FlaskForm):
    current = IntegerField('Current')
    number = IntegerField('No. of Conductors')
    insulation = SelectField('Ins. Type', choices=[('PV', 'PV'), ('THHN', 'THHN')])
    temperature = IntegerField('Amb. Temp. (F)')
    continuous = RadioField('Continuous Current?', choices=[(1.25, 'Yes'), (1, 'No')])
    submit = SubmitField('Calculate Size')

class RM_Form(FlaskForm):
    masslbs = IntegerField('Mass (lbs.)')
    rpm = IntegerField('RPM')
    radiusInches = IntegerField('Radius (in.)')
    submit = SubmitField('Calculate')
