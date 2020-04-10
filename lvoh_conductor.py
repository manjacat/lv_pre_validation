# -*- coding: utf-8 -*-
"""
/***************************************************************************
All checkings related to LV OH conductor 
 ***************************************************************************/
"""
from qgis.core import *
# import own custom file
from .dropdown_enum import *

def lvoh_call_me():
	print('lv_oh_conductor is called')          
	
lv_oh_field_null = 'ERR_LVOHCOND_01'
lv_oh_enum_valid = 'ERR_LVOHCOND_02'
lv_oh_length = 'ERR_LVOHCOND_07'

# **********************************
# ****** Check for Enum Value ******
# **********************************

def lv_oh_field_enum(field_name):
        arr = []
        arr_dropdown = []
        if field_name == 'status':
                arr_dropdown = arr_status
        elif field_name == 'phasing':
                arr_dropdown = arr_phasing
        elif field_name == 'usage':
                arr_dropdown = arr_usage
        elif field_name == 'label':
                arr_dropdown = arr_label_lv_oh       
        elif field_name == 'db_oper':
                arr_dropdown = arr_db_oper
        else:
                arr_dropdown = []
        
        layer = QgsProject.instance().mapLayersByName('LV_OH_Conductor')[0]
        feat = layer.getFeatures()
        for f in feat:
                device_id = f.attribute('device_id')
                field_value = f.attribute(field_name)
                if field_value not in arr_dropdown:
                        arr.append(device_id)
        return arr

def lv_oh_field_enum_message(device_id, field_name):
        e_msg = lv_oh_enum_valid +',' + device_id + ',' + 'LV_OH_Conductor: ' + device_id + ' Invalid Enumerator at: ' + field_name + '\n'
        return e_msg

# **********************************
# ****** Check for Not Null   ******
# **********************************

def lv_oh_field_not_null(field_name):
	arr = []
	layer = QgsProject.instance().mapLayersByName('LV_OH_Conductor')[0]
	query = '"' + field_name + '" is null OR ' + '"' + field_name + '" =  \'N/A\''
	feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
	for f in feat:
		device_id = f.attribute('device_id')
		arr.append(device_id)
	return arr

def lv_oh_field_not_null_message(device_id, field_name):
	e_msg = lv_oh_field_null +',' + device_id + ',' + 'LV_OH_Conductor: ' + device_id + ' Mandatory field NOT NULL at: ' + field_name + '\n'
	return e_msg

# **********************************
# ********* Check Length  **********
# **********************************

def lv_oh_length_check():
	arr = []
	layer = QgsProject.instance().mapLayersByName('LV_OH_Conductor')[0]
	query = '"length" <= 1.5'
	feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
	for f in feat:
		device_id = f.attribute('device_id')
		arr.append(device_id)
	return arr

def lv_oh_length_check_message(device_id):
	e_msg = lv_oh_length + ',' + device_id + ',' + 'LV_OH_Conductor: ' + device_id + ' length less than 1.5' + '\n'
	return e_msg

# **********************************
# ******* End of Validation  *******
# **********************************
