from flask import request
from nec_lib import NECTables as NEC
from nec_lib import ConduitFill as CF
from nec_lib import WireDerate as WD

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
                return round(cross_sect, 1), dict[x]
            else:
                return 0


def get_wire_size(current, number, insulation, temperature, continuous):
    form = WS_Form()
    if form.is_submitted():
        crnt = int(request.form.get(current))
        nmbr = int(request.form.get(number))
        ins = str(request.form.get(insulation))
        tmp = int(request.form.get(temperature))
        cntns = float(request.form.get(continuous))

        fill_factor = 1
        temp_factor = 1
        copper_tuple = (0, 0)
        al_tuple = (0, 0)

        for x in WD.fill_lst:
            if nmbr > x:
                continue
            elif nmbr < x:
                fill_factor = WD.fill_dict[x]
                break

        for y in WD.temp_lst:
            if tmp > y:
                continue
            elif tmp < y:
                temp_factor = WD.temp_dict_90[y]
                break

        required_ampacity = (crnt / fill_factor / temp_factor) * cntns

        for z in WD.cu_ampacity_90:
            if required_ampacity > z:
                continue
            elif required_ampacity < z:
                copper_tuple = (WD.cu_ampacity_to_awg_90[z], z)
                break

        for z in WD.al_ampacity_90:
            if required_ampacity > z:
                continue
            elif required_ampacity < z:
                al_tuple = (WD.al_ampacity_to_awg_90[z], z)
                break
        return_list = [copper_tuple[0], al_tuple[0], round(required_ampacity,2)]
        return return_list

def rotational_mass(masslbs, rpm, radius):
    form = RM_Form()
    if form.is_submitted():
        mss = float(request.form.get(masslbs))
        RPM = float(request.form.get(rpm))
        rds_inch = float(request.form.get(radius))

        mass_kg = mss * .453592
        radius_meters = rds_inch * .0254

        velocity_in_inch = (rds_inch * 3.141592653) * (RPM / 60)
        velocity_in_meters = (radius_meters * 3.141592653) * (RPM / 60)

        centripetal_force = (mass_kg * (velocity_in_meters ** 2)) / radius_meters
        centrifugal_force = centripetal_force * .224809
        horsepower = centripetal_force * .00134102209

        output_list = [velocity_in_inch, velocity_in_meters, centripetal_force,
                       centrifugal_force, horsepower]

        return output_list
    else:
        return 0

from vd import VD_Form, CF_Form, WS_Form, RM_Form
