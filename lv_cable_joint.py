# -*- coding: utf-8 -*-
"""
/***************************************************************************
All checkings related to LV Cable Joint
 ***************************************************************************/
"""
from qgis.core import *
# import own custom file
from .dropdown_enum import *
from .rps_utility import *

layer_name = 'LV_Cable_Joint'
lv_cj_field_null = 'ERR_LVCJOINT_01'
lv_cj_enum_valid = 'ERR_LVCJOINT_02'
lv_cj_snapping_code = 'ERR_LVCJOINT_04'
lv_cj_class_mismatch_code = 'ERR_LVCJOINT_05'
lv_cj_duplicate_code = 'ERR_DUPLICATE_ID'
lv_cj_device_id_format_code = 'ERR_DEVICE_ID'
lv_cj_z_m_shapefile_code = 'ERR_Z_M_VALUE'

# TODO: CLASS_FIELD_MISMATCH
# - Wrong combination of class and usage for device_id RPS6122lcj5. OH Conductor
# usage is LV LINE and class is SL POT END should be LV POT LINE
# TODO: LV_CABLE_JOINT_SNAPPING_ERROR
# -	LV Cable Joint must be snapped to either lv ugc or lv ohc
# TODO: check LV OH class connected to LV Cable Joint
# if Service Line, then LV Cable Joint is SL Pot End
# if LV Line, then LV Cable Joint is LV Pot End




# *****************************************
# ****** Check Z-M Value in shapefile *****
# *****************************************

def lv_cj_z_m_shapefile():
    arr = []
    arr = rps_z_m_shapefile(layer_name)
    return arr


def lv_cj_z_m_shapefile_message(device_id):
    longitude = 0
    latitude = 0
    e_msg = rps_z_m_shapefile_message(layer_name, device_id, lv_cj_z_m_shapefile_code)
    return e_msg


# ****************************************
# ****** Check for Device_Id Format ******
# ****************************************

def lv_cj_device_id_format():
    arr = []
    arr = rps_device_id_format(layer_name)
    return arr


def lv_cj_device_id_format_message(device_id):
    e_msg = rps_device_id_format_message(layer_name, device_id, lv_cj_device_id_format_code)
    return e_msg


# **********************************
# ****** Check for Duplicates ******
# **********************************

def lv_cj_duplicate():
    arr = []
    arr = rps_duplicate_device_id(layer_name)

    return arr


def lv_cj_duplicate_message(device_id):
    longitude = 0
    latitude = 0
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    query = '"device_id" = \'' + str(device_id) + '\''
    feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
    for f in feat:
        geom = f.geometry()
        if geom:
            point = rps_get_qgspoint(geom)
            longitude = point.x()
            latitude = point.y()

    e_msg = lv_cj_duplicate_code + ',' + str(device_id) + ',' + layer_name + ': ' + str(
        device_id) + ' duplicated device_id: ' + str(device_id) + ',' + str(longitude) + ',' + str(latitude) + ' \n'
    return e_msg


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

    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    feat = layer.getFeatures()
    err_count = 0
    for f in feat:
        device_id = f.attribute('device_id')
        try:
            field_value = f.attribute(field_name)
            if field_value not in arr_dropdown:
                arr.append(device_id)
        except Exception as e:
            err_count += 1

    return arr


def lv_cj_field_enum_message(device_id, field_name):
    longitude = 0
    latitude = 0
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    query = '"device_id" = \'' + str(device_id) + '\''
    feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
    for f in feat:
        geom = f.geometry()
        point = rps_get_qgspoint(geom)
        longitude = point.x()
        latitude = point.y()

    e_msg = lv_cj_enum_valid + ',' + str(device_id) + ',' + layer_name + ': ' + str(
        device_id) + ' Invalid Enumerator at: ' + field_name + ',' + str(longitude) + ',' + str(latitude) + ' \n'
    return e_msg


# **********************************
# ****** Check for Not Null   ******
# **********************************

def lv_cj_field_not_null(field_name):
    arr = rps_field_not_null(layer_name, field_name)
    return arr


def lv_cj_field_not_null_message(device_id, field_name):
    longitude = 0
    latitude = 0
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    query = '"device_id" = \'' + str(device_id) + '\''
    feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
    for f in feat:
        geom = f.geometry()
        if geom:
            point = rps_get_qgspoint(geom)
            longitude = point.x()
            latitude = point.y()

    e_msg = lv_cj_field_null + ',' + str(device_id) + ',' + layer_name + ': ' + str(
        device_id) + ' Mandatory field NOT NULL at: ' + field_name + ',' + str(longitude) + ',' + str(latitude) + ' \n'
    return e_msg


# *********************************************
# ********* LV Cable Joint Snapping  **********
# *********************************************
'''
# The LV Cable Joint must be snapped to either LV UG Conductor or LV OH Conductor.
# There should be a vertex digitized when LV Cable Joint connects to LV UG/LV OH Conductor. 
# Step 1: list all vectors of LV OH/LV UG
# Step 2: list all geom of LV Cable Joint
# Step 3: at least ONE LV Cable joint must have distance between it and LV OH/LV UG == 0
# Step 4: if LV Cable Joint is not nearby LV UG/LV OH Vectors, then error.
'''


def lv_cj_snapping(arr_lv_ug_exclude_geom, arr_lv_oh_exclude_geom):
    arr = []
    arr_lv = []
    # qgis distanceArea
    distance = QgsDistanceArea()
    distance.setEllipsoid('WGS84')

    layerLV_01 = QgsProject.instance().mapLayersByName('LV_OH_Conductor')[0]
    feat_01 = layerLV_01.getFeatures()
    for f in feat_01:
        device_temp = f.attribute('device_id')
        if device_temp not in arr_lv_oh_exclude_geom:
            geom = f.geometry()
            y = geom.mergeLines()
            polyline_y = y.asPolyline()
            # loop all vertex in this line
            for geom_01 in polyline_y:
                arr_lv.append(geom_01)

    layerLV_02 = QgsProject.instance().mapLayersByName('LV_UG_Conductor')[0]
    feat_02 = layerLV_02.getFeatures()
    for f in feat_02:
        device_temp = f.attribute('device_id')
        if device_temp not in arr_lv_ug_exclude_geom:
            geom = f.geometry()
            y = geom.mergeLines()
            polyline_y = y.asPolyline()
            # loop all vertex in this line
            for geom_02 in polyline_y:
                arr_lv.append(geom_02)
    # print(arr_lv)
    # print('total vertex:',len(arr_lv))

    # get geom of LV Cable Joint
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    feat = layer.getFeatures()
    for f in feat:
        device_id = f.attribute('device_id')
        geom = f.geometry()
        if geom:
            geom_x = rps_get_qgspoint(geom)
            # new arr_snapping each loop
            arr_snapping = []
            for geom_lv in arr_lv:
                m = distance.measureLine(geom_lv, geom_x)
                if m < 0.001:
                    arr_snapping.append(device_id)
            if len(arr_snapping) == 0:
                arr.append(device_id)
    return arr


def lv_cj_snapping_message(device_id):
    longitude = 0
    latitude = 0
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    query = '"device_id" = \'' + str(device_id) + '\''
    feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
    for f in feat:
        geom = f.geometry()
        if geom:
            point = rps_get_qgspoint(geom)
            longitude = point.x()
            latitude = point.y()

    e_msg = lv_cj_snapping_code + ',' + str(device_id) + ',' + layer_name + ': ' + str(
        device_id) + ' LV Cable joint not snap to LV OH/LV UG ' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
    return e_msg

# ******************************************
# ****** LV Cable Joint Class Mismatch *****
# ******************************************

# get LV OH closest to LV Cable Joint
# if got LV OH, get its USAGE
# compare with LV CJ's CLASS

def lv_cj_class_mismatch(arr_lv_ug_exclude_geom, arr_lv_oh_exclude_geom):
    arr = []
    arr_lv = []
    # qgis distanceArea
    distance = QgsDistanceArea()
    distance.setEllipsoid('WGS84')

    layerLV_01 = QgsProject.instance().mapLayersByName('LV_OH_Conductor')[0]
    feat_01 = layerLV_01.getFeatures()
    for f in feat_01:
        device_temp = f.attribute('device_id')
        if device_temp not in arr_lv_oh_exclude_geom:
            geom = f.geometry()
            y = geom.mergeLines()
            polyline_y = y.asPolyline()
            # loop all vertex in this line
            for geom_01 in polyline_y:
                # store in multidimension array (LV OH device id, geom)
                arr_lv.append([device_temp, geom_01])
    
    # get geom of LV Cable Joint
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    feat = layer.getFeatures()
    for f in feat:
        device_id = f.attribute('device_id')
        geom = f.geometry()
        if geom:
            geom_x = rps_get_qgspoint(geom)
            # new arr_snapping each loop
            arr_snapping = []
            for arr_device_geom in arr_lv:
                device_id_lv = arr_device_geom[0]
                geom_lv = arr_device_geom[1]
                m = distance.measureLine(geom_lv, geom_x)
                if m < 0.001:
                    # TODO
                    arr_snapping.append(device_id)
                    print('LVCJ id is ' + str(device_id) + ' and LVOH id is ' + str(device_id_lv))
            if len(arr_snapping) == 0:
                arr.append(device_id)

    print(str(len(arr)))
          
    return arr

def lv_cj_class_mismatch_message(device_id):
    longitude = 0
    latitude = 0
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    query = '"device_id" = \'' + str(device_id) + '\''
    feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
    for f in feat:
        geom = f.geometry()
        if geom:
            point = rps_get_qgspoint(geom)
            longitude = point.x()
            latitude = point.y()
    e_msg = lv_cj_class_mismatch_code + ',' + str(device_id) + ',' + layer_name + ': ' + str(
        device_id) + ' Wrong combination of class and usage for ' + str(device_id) + ' and its LV OH ' + ',' + str(longitude) + ',' + str(latitude) + ' \n'

    return e_msg


# **********************************
# ******* End of Validation  *******
# **********************************
