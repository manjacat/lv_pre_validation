# -*- coding: utf-8 -*-
"""
/***************************************************************************
All checkings related to Pole
 ***************************************************************************/
"""
from qgis.core import *
# import own custom file
from .dropdown_enum import *
from .rps_utility import rps_device_id_format

layer_name = 'Pole'	
pole_field_null = 'ERR_POLE_01'
pole_enum_valid = 'ERR_POLE_02'
pole_duplicate_code = 'ERR_DUPLICATE_ID'
pole_device_id_format_code = 'ERR_DEVICE_ID'

# ****************************************
# ****** Check for Device_Id Format ******
# ****************************************

def pole_device_id_format():
        arr = []
        arr = rps_device_id_format(layer_name)
        return arr

def pole_device_id_format_message(device_id):
        e_msg = pole_device_id_format_code +',' + device_id + ',' + layer_name + ': ' + device_id + ' device_id format error \n'
        return e_msg

# **********************************
# ****** Check for Duplicates ******
# **********************************

def pole_duplicate():
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

def pole_duplicate_message(device_id):
        e_msg = pole_duplicate_code +',' + device_id + ',' + layer_name + ': ' + device_id + ' duplicated device_id: ' + device_id + '\n'
        return e_msg

# **********************************
# ****** Check for Enum Value ******
# **********************************

def pole_field_enum(field_name):
        arr = []
        arr_dropdown = []
        if field_name == 'status':
                arr_dropdown = arr_status
        elif field_name == 'light_ares':
                arr_dropdown = arr_ares
        elif field_name == 'struc_type':
                arr_dropdown = arr_struc_type
        elif field_name == 'db_oper':
                arr_dropdown = arr_db_oper
        elif field_name == 'lv_ptc':
                arr_dropdown = arr_lv_ptc
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

def pole_field_enum_message(device_id, field_name):
        e_msg = pole_enum_valid +',' + device_id + ',' + layer_name + ': ' + device_id + ' Invalid Enumerator at: ' + field_name + '\n'
        return e_msg

# **********************************
# ****** Check for Not Null   ******
# **********************************

def pole_field_not_null(field_name):
	arr = []
	layer = QgsProject.instance().mapLayersByName(layer_name)[0]
	query = '"' + field_name + '" is null OR ' + '"' + field_name + '" =  \'N/A\''
	feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
	for f in feat:
		device_id = f.attribute('device_id')
		arr.append(device_id)
	return arr

def pole_field_not_null_message(device_id, field_name):
	e_msg = pole_field_null +',' + device_id + ',' + layer_name + ': ' + device_id + ' Mandatory field NOT NULL at: ' + field_name + '\n'
	return e_msg

# **********************************
# ********* TODO  **********
# **********************************


# **********************************
# ******* End of Validation  *******
# **********************************
