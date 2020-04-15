# -*- coding: utf-8 -*-
"""
/***************************************************************************
All checkings related to Street Light
 ***************************************************************************/
"""
from qgis.core import *
# import own custom file
from .dropdown_enum import *

layer_name = 'Street_Light'	
st_light_field_null = 'ERR_STLIGHT_01'
st_light_enum_valid = 'ERR_STLIGHT_02'
st_light_phasing_code = 'ERR_STLIGHT_04'
st_light_duplicate_code = 'ERR_DUPLICATE_ID'

# **********************************
# ****** Check for Duplicates ******
# **********************************

def st_light_duplicate():
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

def st_light_duplicate_message(device_id):
        e_msg = st_light_duplicate_code +',' + device_id + ',' + layer_name + ': ' + device_id + ' duplicated device_id: ' + device_id + '\n'
        return e_msg

# **********************************
# ****** Check for Enum Value ******
# **********************************

def st_light_field_enum(field_name):
        arr = []
        arr_dropdown = []
        # phasing moved to 'Phasing should be R'
        if field_name == 'status':
                arr_dropdown = arr_status
        elif field_name == 'db_oper':
                arr_dropdown = arr_db_oper
        elif field_name == 'cont_dev':
                arr_dropdown = arr_cont_dev
        else:
                arr_dropdown = []

        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        feat = layer.getFeatures()
        for f in feat:
                device_id = f.attribute('device_id')
                field_value = f.attribute(field_name)
                if field_value not in arr_dropdown:
                        arr.append(device_id)
        return arr

def st_light_field_enum_message(device_id, field_name):
        e_msg = st_light_enum_valid +',' + device_id + ',' + layer_name + ': ' + device_id + ' Invalid Enumerator at: ' + field_name + '\n'
        return e_msg

# **********************************
# ****** Check for Not Null   ******
# **********************************

def st_light_field_not_null(field_name):
	arr = []
	layer = QgsProject.instance().mapLayersByName(layer_name)[0]
	query = '"' + field_name + '" is null OR ' + '"' + field_name + '" =  \'N/A\''
	feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
	for f in feat:
		device_id = f.attribute('device_id')
		arr.append(device_id)
	return arr

def st_light_field_not_null_message(device_id, field_name):
	e_msg = st_light_field_null + ',' + device_id + ',' + layer_name + ': ' + device_id + ' Mandatory field NOT NULL at: ' + field_name + '\n'
	return e_msg

# *******************************************
# ********* Phasing should be 'R'  **********
# *******************************************

def st_light_phasing():
        arr = []
        arr_dropdown = []
        field_name = 'phasing'
        arr_dropdown = arr_phasing_st_light
        
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        feat = layer.getFeatures()
        for f in feat:
                device_id = f.attribute('device_id')
                field_value = f.attribute(field_name)
                if field_value not in arr_dropdown:
                        arr.append(device_id)
        return arr

def st_light_phasing_message(device_id):
	e_msg = st_light_phasing_code + ',' + device_id + ',' + layer_name + ': ' + device_id + ' phasing should be "R" \n'
	return e_msg


# **********************************
# ******* End of Validation  *******
# **********************************