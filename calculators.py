from flask import request
from nec_lib import NECTables as NEC
from nec_lib import ConduitFill as CF

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


def get_conduit_size(size, number, insulation, ground, conduit):
    form = CF_Form()
    if form.is_submitted():
        sz = str(request.form.get(size))
        nmbr = request.form.get(number)
        ins = str(request.form.get(insulation))
        grnd = str(request.form.get(ground))
        cndt = str(request.form.get(conduit))

        if ins == 'PV':
            ins_area = CF.pv_awg_to_area[sz]
            grnd_area = CF.pv_awg_to_area[grnd]

        else:
            ins_area = CF.thhn_awg_to_area[sz]
            grnd_area = CF.thhn_awg_to_area[grnd]

        total_area = (ins_area * float(nmbr)) + grnd_area

        if cndt == "EMT":
            lst = CF.emt_lst
            dict = CF.emt_dict
        else:
            lst = CF.pvc_lst
            dict = CF.pvc_dict

        for x in lst:
            if (total_area / .4) > x:
                continue
            elif (total_area / .4) < x:
                cross_sect = (total_area / x) * 100
                return cross_sect, dict[x]
            else:
                return 0


def get_wire_size(current, number, insulation, temperature, continuous):
    form = WS_Form()
    if form.is_submitted():
        crnt = int(request.form.get(current))
        nmbr = request.form.get(number)
        ins = str(request.form.get(insulation))
        tmp = int(request.form.get(temperature))
        cntns = str(request.form.get(continuous))

        return 0



from vd import VD_Form, CF_Form, WS_Form
