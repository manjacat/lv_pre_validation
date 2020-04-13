# -*- coding: utf-8 -*-
"""
/***************************************************************************
All checkings related to LV OH conductor 
 ***************************************************************************/
"""
from qgis.core import *
# import own custom file
from .dropdown_enum import *
	
lv_cj_field_null = 'ERR_LVCJOINT_01'
lv_cj_enum_valid = 'ERR_LVCJOINT_02'

# **********************************
# ****** Check for Enum Value ******
# **********************************

def lv_cj_field_enum(field_name):
        arr = []
        arr_dropdown = []
        if field_name == 'status':
                arr_dropdown = arr_status
        elif field_name == 'class':
                arr_dropdown = arr_class_lv_cj
        elif field_name == 'type':
                arr_dropdown = arr_type_lv_cj
        elif field_name == 'db_oper':
                arr_dropdown = arr_db_oper
        else:
                arr_dropdown = []
        
        layer = QgsProject.instance().mapLayersByName('LV_Cable_Joint')[0]
        feat = layer.getFeatures()
        for f in feat:
                device_id = f.attribute('device_id')
                field_value = f.attribute(field_name)
                if field_value in arr_dropdown:
                        arr.append(device_id)
        return arr

def lv_cj_field_enum_message(device_id, field_name):
        e_msg = lv_cj_enum_valid +',' + device_id + ',' + 'LV_Cable_Joint: ' + device_id + ' Invalid Enumerator at: ' + field_name + '\n'
        return e_msg

# **********************************
# ****** Check for Not Null   ******
# **********************************

def lv_cj_field_not_null(field_name):
	arr = []
	layer = QgsProject.instance().mapLayersByName('LV_Cable_Joint')[0]
	query = '"' + field_name + '" is not null OR ' + '"' + field_name + '" =  \'N/A\''
	feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
	for f in feat:
		device_id = f.attribute('device_id')
		arr.append(device_id)
	return arr

def lv_cj_field_not_null_message(device_id, field_name):
	e_msg = lv_cj_field_null +',' + device_id + ',' + 'LV_Cable_Joint: ' + device_id + ' Mandatory field NOT NULL at: ' + field_name + '\n'
	return e_msg

# **********************************
# ********* TODO  **********
# **********************************


# **********************************
# ******* End of Validation  *******
# **********************************
