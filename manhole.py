# -*- coding: utf-8 -*-
"""
/***************************************************************************
All checkings related to Manhole
 ***************************************************************************/
"""
from qgis.core import *
# import own custom file
from .dropdown_enum import *

layer_name = 'Manhole'	
manhole_field_null = 'ERR_MANHOLE_01'
manhole_enum_valid = 'ERR_MANHOLE_02'
manhole_duplicate_code = 'ERR_DUPLICATE_ID'

# **********************************
# ****** Check for Duplicates ******
# **********************************

def manhole_duplicate():
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

def manhole_duplicate_message(device_id):
        e_msg = manhole_duplicate_code +',' + device_id + ',' + layer_name + ': ' + device_id + ' duplicated device_id: ' + device_id + '\n'
        return e_msg

# **********************************
# ****** Check for Enum Value ******
# **********************************

def manhole_field_enum(field_name):
        arr = []
        arr_dropdown = []
        if field_name == 'status':
                arr_dropdown = arr_status        
        elif field_name == 'db_oper':
                arr_dropdown = arr_db_oper
        elif field_name == 'type':
                arr_dropdown = arr_type_manhole
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

def manhole_field_enum_message(device_id, field_name):
        e_msg = manhole_enum_valid +',' + device_id + ',' + layer_name + ': ' + device_id + ' Invalid Enumerator at: ' + field_name + '\n'
        return e_msg

# **********************************
# ****** Check for Not Null   ******
# **********************************

def manhole_field_not_null(field_name):
	arr = []
	layer = QgsProject.instance().mapLayersByName(layer_name)[0]
	query = '"' + field_name + '" is null OR ' + '"' + field_name + '" =  \'N/A\''
	feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
	for f in feat:
		device_id = f.attribute('device_id')
		arr.append(device_id)
	return arr

def manhole_field_not_null_message(device_id, field_name):
	e_msg = manhole_field_null +',' + device_id + ',' + layer_name + ': ' + device_id + ' Mandatory field NOT NULL at: ' + field_name + '\n'
	return e_msg

# **********************************
# ********* TODO  **********
# **********************************


# **********************************
# ******* End of Validation  *******
# **********************************
