# -*- coding: utf-8 -*-
"""
/***************************************************************************
Utility functions
 ***************************************************************************/
"""
from qgis.core import *
# import own custom file
from .dropdown_enum import *
import re

# ****************************************
# ****** Check for Device_Id format ******
# ****************************************

code_lv_ug = 'ugc'
code_lv_oh = 'ohc'
code_lv_fuse = 'fus'
code_lv_cj = 'lcj'
code_lvdb_fp = 'lvdb'
code_pole = 'pole'
code_dmd_pt = 'dmd'
code_st_light = 'stl'
code_manhole = 'man'
code_st_duct = 'std'


def rps_device_id_format(layer_name):
        arr = []
        object_code = ''
        if layer_name == 'LV_UG_Conductor':
                object_code = code_lv_ug

        vendor_code = 'R'
        station_code = '([1-9][0-9]{0,3})' # accepts 1 - 9999
        running_number = '([0-9]{0,3})' # accepts 000 - 999
        pattern = '^' + vendor_code + station_code + object_code + running_number + '$'
        # print(pattern)

        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        feat = layer.getFeatures()
        for f in feat:
                device_id = f.attribute('device_id')
                check = re.search(pattern, device_id)
                # print('device id =' + device_id)
                # print(check)
                if not check:
                        arr.append(device_id)
        return arr


# **********************************
# ********* TODO  **********
# **********************************


# **********************************
# ******* End of Validation  *******
# **********************************
