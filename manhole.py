# -*- coding: utf-8 -*-
"""
/***************************************************************************
All checkings related to Manhole
 ***************************************************************************/
"""
from qgis.core import *
# import own custom file
from .dropdown_enum import *
from .rps_utility import *

layer_name = 'Manhole'
manhole_field_null = 'ERR_MANHOLE_01'
manhole_enum_valid = 'ERR_MANHOLE_02'
manhole_duplicate_code = 'ERR_DUPLICATE_ID'
manhole_device_id_format_code = 'ERR_DEVICE_ID'
manhole_z_m_shapefile_code = 'ERR_Z_M_VALUE'


# *****************************************
# ****** Check Z-M Value in shapefile *****
# *****************************************

def manhole_z_m_shapefile():
    arr = []
    arr = rps_z_m_shapefile(layer_name)
    return arr


def manhole_z_m_shapefile_message(geom_name):
    longitude = 0
    latitude = 0
    e_msg = manhole_z_m_shapefile_code + ',' + layer_name + ',' + 'Z M Value for ' + layer_name + ' is ' + geom_name + ',' + str(
        longitude) + ',' + str(latitude) + ' \n'
    return e_msg


# ****************************************
# ****** Check for Device_Id Format ******
# ****************************************

def manhole_device_id_format():
    arr = []
    arr = rps_device_id_format(layer_name)
    return arr


def manhole_device_id_format_message(device_id):
    e_msg = rps_device_id_format_message(layer_name, device_id, manhole_device_id_format_code)
    return e_msg


# **********************************
# ****** Check for Duplicates ******
# **********************************

def manhole_duplicate():
    arr = []
    arr = rps_device_id_format(layer_name)

    return arr


def manhole_duplicate_message(device_id):
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

    e_msg = manhole_duplicate_code + ',' + str(device_id) + ',' + layer_name + ': ' + str(
        device_id) + ' duplicated device_id: ' + str(device_id) + ',' + str(longitude) + ',' + str(latitude) + ' \n'
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

    e_msg = manhole_enum_valid + ',' + str(device_id) + ',' + layer_name + ': ' + str(
        device_id) + ' Invalid Enumerator at: ' + field_name + ',' + str(longitude) + ',' + str(latitude) + ' \n'
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

    e_msg = manhole_field_null + ',' + str(device_id) + ',' + layer_name + ': ' + str(
        device_id) + ' Mandatory field NOT NULL at: ' + field_name + ',' + str(longitude) + ',' + str(latitude) + ' \n'
    return e_msg

# **********************************
# ********* TODO  **********
# **********************************


# **********************************
# ******* End of Validation  *******
# **********************************
