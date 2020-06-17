# -*- coding: utf-8 -*-
"""
/***************************************************************************
All checkings related to Pole
 ***************************************************************************/
"""
from qgis.core import *
# import own custom file
from .dropdown_enum import *
from .rps_utility import *

layer_name = 'Pole'	
pole_field_null = 'ERR_POLE_01'
pole_enum_valid = 'ERR_POLE_02'
pole_duplicate_code = 'ERR_DUPLICATE_ID'
pole_device_id_format_code = 'ERR_DEVICE_ID'
pole_z_m_shapefile_code = 'ERR_Z_M_VALUE'
pole_lv_oh_vertex_code = 'ERR_POLE_03'

# *****************************************
# ****** Check Z-M Value in shapefile *****
# *****************************************

def pole_z_m_shapefile():
        arr = []
        arr = rps_z_m_shapefile(layer_name)
        return arr

def pole_z_m_shapefile_message(device_id):
        longitude = 0
        latitude = 0
        if device_id:
                query = '"device_id" = \'' + str(device_id) + '\''
                feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
        else:
                feat = layer.getFeatures()
        err_detail = ''
        for f in feat:
                geom = f.geometry()
                geom_type = QgsWkbTypes.displayString(geom.wkbType())
                if geom:
                        err_detail = layer_name + ': ' + str(device_id) + ' geometry is ' + geom_type
                else:
                        err_detail = layer_name + ': ' + str(device_id) + ' geometry ERROR. Geometry is ' + geom_type
        e_msg = lv_cj_z_m_shapefile_code + ',' + str(device_id) + ',' + err_detail + ',' + str(longitude) + ',' + str(
                latitude) + ' \n'
        return e_msg

# ****************************************
# ****** Check for Device_Id Format ******
# ****************************************

def pole_device_id_format():
        arr = []
        arr = rps_device_id_format(layer_name)
        return arr

def pole_device_id_format_message(device_id):
        longitude = 0
        latitude = 0
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + str(device_id) + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query)) 
        for f in feat:
                geom = f.geometry()
                point = geom.asPoint()
                longitude = point.x()
                latitude = point.y()
        e_msg = pole_device_id_format_code +',' + str(device_id) + ',' + layer_name + ': ' + str(device_id) + ' device_id format error' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg

# **********************************
# ****** Check for Duplicates ******
# **********************************

def pole_duplicate():
        arr = []
        arr = rps_duplicate_device_id(layer_name)

        return arr

def pole_duplicate_message(device_id):
        longitude = 0
        latitude = 0
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + str(device_id) + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query)) 
        for f in feat:
                geom = f.geometry()
                point = geom.asPoint()
                longitude = point.x()
                latitude = point.y()
        e_msg = pole_duplicate_code +',' + str(device_id) + ',' + layer_name + ': ' + str(device_id) + ' duplicated device_id: ' + str(device_id) + ',' + str(longitude) + ',' + str(latitude) + ' \n'
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
        longitude = 0
        latitude = 0
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + str(device_id) + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query)) 
        for f in feat:
                geom = f.geometry()
                point = geom.asPoint()
                longitude = point.x()
                latitude = point.y()
        e_msg = pole_enum_valid +',' + str(device_id) + ',' + layer_name + ': ' + str(device_id) + ' Invalid Enumerator at: ' + field_name + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg

# **********************************
# ****** Check for Not Null   ******
# **********************************

# user feedback: if pole_no, allow N/A
def pole_field_not_null(field_name):
	arr = []
	layer = QgsProject.instance().mapLayersByName(layer_name)[0]
	query = '"' + field_name + '" is null OR ' + '"' + field_name + '" =  \'N/A\''
	if field_name == 'pole_no':
                query = '"' + field_name + '" is null OR ' + '"' + field_name + '" =  \'NA\''
	feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
	for f in feat:
		device_id = f.attribute('device_id')
		arr.append(device_id)
	return arr

def pole_field_not_null_message(device_id, field_name):
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + str(device_id) + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))        
        longitude = 0
        latitude = 0
        for f in feat:
                geom = f.geometry()
                point = geom.asPoint()
                longitude = point.x()
                latitude = point.y()
        e_msg = pole_field_null +',' + str(device_id) + ',' + layer_name + ': ' + str(device_id) + ' Mandatory field NOT NULL at: ' + field_name + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg

# ************************************************************
# ********* All Pole must have LV OH vertex nearby  **********
# ************************************************************
'''
# each Pole must be close to lv oh vertex (0.9m < x 1.1m)
# 
'''

def get_lv_oh_vertex(arr_lv_oh_exclude_geom):
        arr = []
        layer = QgsProject.instance().mapLayersByName('LV_OH_Conductor')[0]
        feat = layer.getFeatures()
        # arr_exclude_usage = ['5 FOOT WAYS']
        arr_exclude_usage = ['SILAP BUAT']
        for f in feat:
                device_id = f.attribute('device_id')
                if device_id not in arr_lv_oh_exclude_geom:
                        usage = f.attribute('usage')
                        if usage not in arr_exclude_usage:
                                geom = f.geometry()
                                y = geom.mergeLines()
                                for g in y.asPolyline():
                                        arr.append(g)
        return arr

def pole_lv_oh_vertex(arr_lv_oh_exclude_geom):
        arr = []
        # qgis distanceArea
        distance = QgsDistanceArea()
        distance.setEllipsoid('WGS84')
        arr_lv_oh = get_lv_oh_vertex(arr_lv_oh_exclude_geom)
        # print('total lv oh vertex is :', len(arr_lv_oh))

        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        feat = layer.getFeatures()
        for f in feat:
                arr_snapping = []
                device_id = f.attribute('device_id')
                geom = f.geometry()
                geom_pole = geom.asPoint()
                for vertex in arr_lv_oh:
                        m = distance.measureLine(geom_pole,vertex)
                        # user feedback: changed upper limit to 2.6 (previously 1.15)
                        if m >= 0.85 and m <= 2.5:
                                arr_snapping.append(device_id)                        
                        #elif m < 0.85 and m > 1.15 and m > 0.8 and m < 1.5:
                        #        print('WARNING: ' + str(device_id) + ' distance is ' + str(m) + 'm')
                if len(arr_snapping) == 0:
                        # print(device_id + ' arr_snapping is ' + str(len(arr_snapping)))
                        arr.append(device_id)
        return arr

def pole_lv_oh_vertex_message(device_id):
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + str(device_id) + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query)) 
        longitude = 0
        latitude = 0
        for f in feat:
                geom = f.geometry()
                point = geom.asPoint()
                longitude = point.x()
                latitude = point.y()
        e_msg = pole_lv_oh_vertex_code + ',' + str(device_id) + ',' + layer_name + ': ' + str(device_id) + ' distance to LV OH vertex not within 1.0m (too close/too far)' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg        

# **********************************
# ******* End of Validation  *******
# **********************************
