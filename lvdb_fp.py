# -*- coding: utf-8 -*-
"""
/***************************************************************************
All checkings related to LVDB-FP
 ***************************************************************************/
"""
from qgis.core import *
# import own custom file
from .dropdown_enum import *

layer_name = 'LVDB-FP'	
lvdb_fp_field_null = 'ERR_LVDVFP_01'
lvdb_fp_enum_valid = 'ERR_LVDBFP_02'
lvdb_fp_remarks_db_oper = 'ERR_LVDBFP_03'
lvdb_fp_lvf_vs_design = 'ERR_LVDBFP_04'

# **********************************
# ****** Check for Enum Value ******
# **********************************

def lvdb_fp_field_enum(field_name):
        arr = []
        arr_dropdown = []
        if field_name == 'status':
                arr_dropdown = arr_status
        elif field_name == 'lvdb_loc':
                arr_dropdown = arr_lvdb_loc
        elif field_name == 'design':
                arr_dropdown = arr_design_lvdb
        elif field_name == 'db_oper':
                arr_dropdown = arr_db_oper
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

def lvdb_fp_field_enum_message(device_id, field_name):
        e_msg = lvdb_fp_enum_valid +',' + device_id + ',' + layer_name + ': ' + device_id + ' Invalid Enumerator at: ' + field_name + '\n'
        return e_msg

# **********************************
# ****** Check for Not Null   ******
# **********************************

def lvdb_fp_field_not_null(field_name):
	arr = []
	layer = QgsProject.instance().mapLayersByName(layer_name)[0]
	query = '"' + field_name + '" is null OR ' + '"' + field_name + '" =  \'N/A\''
	feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
	for f in feat:
		device_id = f.attribute('device_id')
		arr.append(device_id)
	return arr

def lvdb_fp_field_not_null_message(device_id, field_name):
	e_msg = lvdb_fp_field_null +',' + device_id + ',' + layer_name + ': ' + device_id + ' Mandatory field NOT NULL at: ' + field_name + '\n'
	return e_msg

# **********************************
# ********* TODO  **********
# **********************************


# **********************************
# ******* End of Validation  *******
# **********************************
