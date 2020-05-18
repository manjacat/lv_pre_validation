# -*- coding: utf-8 -*-
"""
/***************************************************************************
All checkings related to LV Fuse
 ***************************************************************************/
"""
from qgis.core import *
# import own custom file
from .dropdown_enum import *
from .rps_utility import *

layer_name = 'LV_Fuse'	
lv_fuse_field_null = 'ERR_LVFUSE_01'
lv_fuse_enum_valid = 'ERR_LVFUSE_02'
lv_fuse_pole_distance_code = 'ERR_LVFUSE_03'
lv_fuse_snapping_code = 'ERR_LVFUSE_04'
lv_fuse_duplicate_code = 'ERR_DUPLICATE_ID'
lv_fuse_device_id_format_code = 'ERR_DEVICE_ID'
lv_fuse_z_m_shapefile_code = 'ERR_Z_M_VALUE'

# *****************************************
# ****** Check Z-M Value in shapefile *****
# *****************************************

def lv_fuse_z_m_shapefile():
        arr = []
        arr = rps_z_m_shapefile(layer_name)
        return arr

def lv_fuse_z_m_shapefile_message(geom_name):
        longitude = 0
        latitude = 0
        e_msg = lv_fuse_z_m_shapefile_code + ',' + layer_name + ',' + 'Z M Value for ' + layer_name + ' is ' + geom_name+ + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg

# ****************************************
# ****** Check for Device_Id Format ******
# ****************************************

def lv_fuse_device_id_format():
        arr = []
        arr = rps_device_id_format(layer_name)
        return arr

def lv_fuse_device_id_format_message(device_id):
        longitude = 0
        latitude = 0

        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + device_id + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
        for f in feat:
                geom = f.geometry()
                point = geom.asPoint()
                longitude = point.x()
                latitude = point.y()
        e_msg = lv_fuse_device_id_format_code +',' + device_id + ',' + layer_name + ': ' + device_id + ' device_id format error' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg

# **********************************
# ****** Check for Duplicates ******
# **********************************

def lv_fuse_duplicate():
        arr = []
        arr = rps_duplicate_device_id(layer_name)

        return arr

def lv_fuse_duplicate_message(device_id):
        longitude = 0
        latitude = 0

        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + device_id + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
        for f in feat:
                geom = f.geometry()
                point = geom.asPoint()
                longitude = point.x()
                latitude = point.y()
        e_msg = lv_fuse_duplicate_code +',' + device_id + ',' + layer_name + ': ' + device_id + ' duplicated device_id: ' + device_id + + ',' + str(longitude) + ',' + str(latitude) + ' \n'
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
        longitude = 0
        latitude = 0

        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + device_id + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
        for f in feat:
                geom = f.geometry()
                point = geom.asPoint()
                longitude = point.x()
                latitude = point.y()
        e_msg = lv_fuse_enum_valid +',' + device_id + ',' + layer_name + ': ' + device_id + ' Invalid Enumerator at: ' + field_name + + ',' + str(longitude) + ',' + str(latitude) + ' \n'
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
        longitude = 0
        latitude = 0

        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + device_id + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
        for f in feat:
                geom = f.geometry()
                point = geom.asPoint()
                longitude = point.x()
                latitude = point.y()
        e_msg = lv_fuse_field_null +',' + device_id + ',' + layer_name + ': ' + device_id + ' Mandatory field NOT NULL at: ' + field_name + + ',' + str(longitude) + ',' + str(latitude) + ' \n'
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
                                # print('distance between lv fuse:' + device_id + ' to nearby pole: ' + str(m) + 'm')
                if len(arr_snapping) == 0:
                        # print('NO POLE is nearby ', device_id)
                        arr.append(device_id)
        return arr

def lv_fuse_pole_distance_message(device_id):
        longitude = 0
        latitude = 0

        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + device_id + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
        for f in feat:
                geom = f.geometry()
                point = geom.asPoint()
                longitude = point.x()
                latitude = point.y()
        e_msg = lv_fuse_pole_distance_code +',' + device_id + ',' + layer_name + ': ' + device_id + ' A pole must be within 2.5m range.' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg

# ********************************************************
# ********* LV Fuse(Blackbox) Snapping Error    **********
# ********************************************************
'''
# LV Fuse should always interact with LV OH Conductor. It should be digitized on top of the lv oh conductor
# Step 1: list all geometry of LV OH (no need LV UG)
# Step 2: list all geom of LV Fuse
# Step 3: at least ONE LV Fuse must have distance between it and LV OH == 0
# Step 4: if LV Fuse is not nearby LV OH Vectors, then error.
'''

def lv_fuse_snapping(arr_lv_oh_exclude_geom):

        # trylukis()
        # try_lukis_line()
        
        arr = []
        arr_lv_vector = []
        arr_lv_line = []
        arr_pole_geom = []
        #qgis distanceArea
        distance = QgsDistanceArea()
        distance.setEllipsoid('WGS84')

        layerLV_01 = QgsProject.instance().mapLayersByName('LV_OH_Conductor')[0]
        # query = '"device_id" = \'R6142ohc120\''
        # feat_01 = layerLV_01.getFeatures(QgsFeatureRequest().setFilterExpression(query))
        feat_01 = layerLV_01.getFeatures()        
        for f in feat_01:
                device_temp = f.attribute('device_id')
                if device_temp not in arr_lv_oh_exclude_geom: 
                        geom = f.geometry()                
                        y = geom.mergeLines()
                        arr_lv_line.append(geom)
                        polyline_y = y.asPolyline()
                        for geom_02 in polyline_y:
                                arr_lv_vector.append(geom_02)

        #print('arr lv line')
        #print(arr_lv_line)
        #print('arr lv vector')
        #print(arr_lv_vector)

        # get geom of lv fuse layer
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        # query = '"device_id" = \'R6142fus02\''
        # feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
        feat = layer.getFeatures()
        for f in feat:
                device_id = f.attribute('device_id')
                # print('device_id insert:', device_id)
                geom_lvf = f.geometry()
                geom_x = geom_lvf.asPoint()
                # my_buffer = geom_lvf.buffer(0.1, 5)
                # print(geom_lvf)
                # print(geom_lvf)
                # new arr_snapping each loop
                arr_snapping = []
                for geom_lv in arr_lv_vector:
                        m = distance.measureLine(geom_lv, geom_x)
                        if m < 0.35:
                                # print('distance is '+  str(m) + 'm')                        
                                arr_snapping.append(device_id)
                                # print('LV fuse ' + device_id + ' is touching lv oh vector!!')
                if len(arr_snapping) == 0:
                        # print(arr_snapping)
                        arr.append(device_id)
        
        return arr

def lv_fuse_snapping_message(device_id):
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + device_id + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
        longitude = 0
        latitude = 0
        for f in feat:
                geom = f.geometry()
                point = geom.asPoint()
                longitude = point.x()
                latitude = point.y()
        
        e_msg = lv_fuse_snapping_code + ',' + device_id + ',' + layer_name + ': ' + device_id + ' LV Fuse is not near LV OH vertex' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg

# **********************************
# ******* End of Validation  *******
# **********************************
