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
lv_fuse_pole_distance_code = 'ERR_LVFUSE_03'
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
        
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        feat = layer.getFeatures()
        for f in feat:
                device_id = f.attribute('device_id')
                field_value = f.attribute(field_name)
                if field_value not in arr_dropdown:
                        arr.append(device_id)
        return arr

def lv_fuse_field_enum_message(device_id, field_name):
        e_msg = lv_fuse_enum_valid +',' + device_id + ',' + layer_name + ': ' + device_id + ' Invalid Enumerator at: ' + field_name + '\n'
        return e_msg

# **********************************
# ****** Check for Not Null   ******
# **********************************

def lv_fuse_field_not_null(field_name):
	arr = []
	layer = QgsProject.instance().mapLayersByName(layer_name)[0]
	query = '"' + field_name + '" is null OR ' + '"' + field_name + '" =  \'N/A\''
	feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
	for f in feat:
		device_id = f.attribute('device_id')
		arr.append(device_id)
	return arr

def lv_fuse_field_not_null_message(device_id, field_name):
	e_msg = lv_fuse_field_null +',' + device_id + ',' + layer_name + ': ' + device_id + ' Mandatory field NOT NULL at: ' + field_name + '\n'
	return e_msg

# *****************************************************************************************************
# ********* Check Geom: there must be a pole nearby LV Fuse(Blackbox) - range 2.4m & 2.6m    **********
# *****************************************************************************************************
'''
# Step 1: get pole geom in array
# Step 2: check distance of LV Fuse to pole.
# if 2.4m < distance < 2.6m , error (must be at least 1)
'''

def lv_fuse_pole_distance():
        arr = []
        arr_pole_geom = []
        # qgis distanceArea
        distance = QgsDistanceArea()
        distance.setEllipsoid('WGS84')
        
        # get pole geom
        lyr_pole = QgsProject.instance().mapLayersByName('Pole')[0]
        feat_pole = lyr_pole.getFeatures()
        for f in feat_pole:
                geom = f.geometry()
                geom_pole = geom.asPoint()
                arr_pole_geom.append(geom_pole)
        
        # get lv fuse geom
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        feat = layer.getFeatures()
        for f in feat:
                device_id = f.attribute('device_id')
                geom = f.geometry()
                # new arr_snapping each loop
                arr_snapping = []
                geom_lv_fuse = geom.asPoint()
                for pole_geom in arr_pole_geom:
                        m = distance.measureLine(pole_geom, geom_lv_fuse)
                        # print('distance in meters',m)
                        if m >= 2.4 and m <= 2.6:
                                arr_snapping.append(device_id)
                                print('distance between lv fuse:' + device_id + ' to nearby pole: ' + str(m) + 'm')
                if len(arr_snapping) == 0:
                        print('NO POLE is nearby ', device_id)
                        arr.append(device_id)
        return arr

def lv_fuse_pole_distance_message(device_id):
	e_msg = lv_fuse_pole_distance_code +',' + device_id + ',' + layer_name + ': ' + device_id + ' No nearby pole within range: \n'
	return e_msg


# **********************************
# ******* End of Validation  *******
# **********************************
