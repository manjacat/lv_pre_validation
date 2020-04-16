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

'''
# Step 1: import Python Regex, re
# Step 2: Generate pattern: vendor code + station code + object code + running number
# Step 3: test device_id against pattern
'''

def rps_device_id_format(layer_name):
        arr = []
        object_code = ''
        if layer_name == 'LV_UG_Conductor':
                object_code = code_lv_ug
        elif layer_name == 'LV_OH_Conductor':
                object_code = code_lv_oh
        elif layer_name == 'LV_Fuse':
                object_code = code_lv_fuse
        elif layer_name == 'LV_Cable_Joint':
                object_code = code_lv_cj
        elif layer_name == 'LVDB-FP':
                object_code = code_lvdb_fp
        elif layer_name == 'Pole':
                object_code = code_pole
        elif layer_name == 'Demand_Point':
                object_code = code_dmd_pt
        elif layer_name == 'Street_Light':
                object_code = code_st_light
        elif layer_name == 'Manhole':
                object_code = code_manhole
        elif layer_name == 'Structure_Duct':
                object_code = code_st_duct
        else:
                object_code = 'MMM'
                

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


# ***************************************************
# ********* Check for Device_Id Duplicate  **********
# ***************************************************

'''
# TODO: move to this function
# Step 1: store all device_id in array (arr_device_id)
# Step 2: loop through all [arr_device_id] and put into new array, [arr_seen]
# Step 3: if items in [arr_device_id] is already in [arr_seen], means its a duplicate
# Step 4: store all duplicate device_id in [arr_dupes]
# Step 5: skip step 4 :D
'''
def duplicate_device_id(layer_name):
        arr = []
        arr_device_id = []
        arr_seen = []
        arr_dupes = []

        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        feat = layer.getFeatures()
        for f in feat:
                device_id = f.attribute('device_id')
                arr_device_id.append(device_id)

        for device_id in arr_device_id:
                # check if device id is seen before
                if device_id in arr_seen and device_id not in arr_dupes:
                        arr.append(device_id)
                        # arr_dupes.append(device_id)
                else:
                        arr_seen.append(device_id)

        # print(arr_seen)
        # print(arr_device_id)
        # print(arr_dupes)

        return arr

# **********************************
# ******* End of Validation  *******
# **********************************
