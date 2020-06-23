# -*- coding: utf-8 -*-
"""
/***************************************************************************
All checkings related to Structure Duct
 ***************************************************************************/
"""
from qgis.core import *
# import own custom file
from .dropdown_enum import *
from .rps_utility import *

layer_name = 'Structure_Duct'
st_duct_field_null = 'ERR_STDUCT_01'
st_duct_enum_valid = 'ERR_STDUCT_02'
st_duct_duplicate_code = 'ERR_DUPLICATE_ID'
st_duct_device_id_format_code = 'ERR_DEVICE_ID'
st_duct_z_m_shapefile_code = 'ERR_Z_M_VALUE'


# *****************************************
# ****** Check Z-M Value in shapefile *****
# *****************************************

def st_duct_z_m_shapefile():
    arr = []
    arr = rps_z_m_shapefile(layer_name)
    return arr


def st_duct_z_m_shapefile_message(device_id):
    longitude = 0
    latitude = 0

    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
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

def st_duct_device_id_format():
    arr = []
    arr = rps_device_id_format(layer_name)
    return arr


def st_duct_device_id_format_message(device_id):
    e_msg = rps_device_id_format_message(layer_name, device_id, st_duct_device_id_format_code)
    return e_msg


# **********************************
# ****** Check for Duplicates ******
# **********************************

def st_duct_duplicate():
    arr = []
    arr = rps_duplicate_device_id(layer_name)

    return arr


def st_duct_duplicate_message(device_id):
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

    e_msg = st_duct_duplicate_code + ',' + str(device_id) + ',' + layer_name + ': ' + str(
        device_id) + ' duplicated device_id: ' + str(device_id) + ',' + str(longitude) + ',' + str(latitude) + ' \n'
    return e_msg


# **********************************
# ****** Check for Enum Value ******
# **********************************

def st_duct_field_enum(field_name):
    arr = []
    arr_dropdown = []
    if field_name == 'status':
        arr_dropdown = arr_status
    elif field_name == 'db_oper':
        arr_dropdown = arr_db_oper
    elif field_name == 'size':
        arr_dropdown = arr_size_st_duct
    elif field_name == 'method':
        arr_dropdown = arr_method_st_duct
    elif field_name == 'way':
        arr_dropdown = arr_way_st_duct
    else:
        arr_dropdown = []

    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    feat = layer.getFeatures()
    err_count = 0
    for f in feat:
        try:
            device_id = f.attribute('device_id')
            field_value = f.attribute(field_name)
            if field_value not in arr_dropdown:
                arr.append(device_id)
        except Exception as e:
            err_count += 1

    return arr


def st_duct_field_enum_message(device_id, field_name):
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

    e_msg = st_duct_enum_valid + ',' + str(device_id) + ',' + layer_name + ': ' + str(
        device_id) + ' Invalid Enumerator at: ' + field_name + ',' + str(longitude) + ',' + str(latitude) + ' \n'
    return e_msg


# **********************************
# ****** Check for Not Null   ******
# **********************************

def st_duct_field_not_null(field_name):
    arr = rps_field_not_null(layer_name, field_name)
    return arr


def st_duct_field_not_null_message(device_id, field_name):
    longitude = 0
    latitude = 0
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    query = '"device_id" = \'' + str(device_id) + '\''
    feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
    for f in feat:
        geom = f.geometry()
        if geom:
            point = geom.asPoint()
            longitude = point.x()
            latitude = point.y()

    e_msg = st_duct_field_null + ',' + str(device_id) + ',' + layer_name + ': ' + str(
        device_id) + ' Mandatory field NOT NULL at: ' + field_name + ',' + str(longitude) + ',' + str(latitude) + ' \n'
    return e_msg

# **********************************
# ********* TODO  **********
# **********************************


# **********************************
# ******* End of Validation  *******
# **********************************
