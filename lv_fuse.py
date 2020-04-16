# -*- coding: utf-8 -*-
"""
/***************************************************************************
All checkings related to LV Fuse
 ***************************************************************************/
"""
from qgis.core import *
# import own custom file
from .dropdown_enum import *
from .rps_utility import rps_device_id_format

layer_name = 'LV_Fuse'	
lv_fuse_field_null = 'ERR_LVFUSE_01'
lv_fuse_enum_valid = 'ERR_LVFUSE_02'
lv_fuse_duplicate_code = 'ERR_DUPLICATE_ID'
lv_fuse_device_id_format_code = 'ERR_DEVICE_ID'

# ****************************************
# ****** Check for Device_Id Format ******
# ****************************************

def lv_fuse_device_id_format():
        arr = []
        arr = rps_device_id_format(layer_name)
        return arr

def lv_fuse_device_id_format_message(device_id):
        e_msg = lv_fuse_device_id_format_code +',' + device_id + ',' + layer_name + ': ' + device_id + ' device_id format error \n'
        return e_msg

# **********************************
# ****** Check for Duplicates ******
# **********************************

def lv_fuse_duplicate():
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

def lv_fuse_duplicate_message(device_id):
        e_msg = lv_fuse_duplicate_code +',' + device_id + ',' + layer_name + ': ' + device_id + ' duplicated device_id: ' + device_id + '\n'
        return e_msg

# **********************************
# ****** Check for Enum Value ******
# **********************************

def lv_fuse_field_enum(field_name):
        arr = []
        arr_dropdown = []
        if field_name == 'status':
                arr_dropdown = arr_status
        elif field_name == 'phasing':
                arr_dropdown = arr_phasing
        elif field_name == 'class':
                arr_dropdown = arr_class_lv_fuse
        elif field_name == 'normal_sta':
                arr_dropdown = arr_normal_sta       
        elif field_name == 'db_oper':
                arr_dropdown = arr_db_oper
        else:
                arr_dropdown = []
        
        layer = QgsProject.instance().mapLayersByName('LV_Fuse')[0]
        feat = layer.getFeatures()
        for f in feat:
                device_id = f.attribute('device_id')
                field_value = f.attribute(field_name)
                if field_value not in arr_dropdown:
                        arr.append(device_id)
        return arr

def lv_fuse_field_enum_message(device_id, field_name):
        e_msg = lv_fuse_enum_valid +',' + device_id + ',' + 'LV_Fuse: ' + device_id + ' Invalid Enumerator at: ' + field_name + '\n'
        return e_msg

# **********************************
# ****** Check for Not Null   ******
# **********************************

def lv_fuse_field_not_null(field_name):
	arr = []
	layer = QgsProject.instance().mapLayersByName('LV_Fuse')[0]
	query = '"' + field_name + '" is null OR ' + '"' + field_name + '" =  \'N/A\''
	feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
	for f in feat:
		device_id = f.attribute('device_id')
		arr.append(device_id)
	return arr

def lv_fuse_field_not_null_message(device_id, field_name):
	e_msg = lv_fuse_field_null +',' + device_id + ',' + 'LV_Fuse: ' + device_id + ' Mandatory field NOT NULL at: ' + field_name + '\n'
	return e_msg

# **********************************
# ********* Check Geom    **********
# **********************************



# **********************************
# ******* End of Validation  *******
# **********************************
