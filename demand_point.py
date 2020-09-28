# -*- coding: utf-8 -*-
"""
/***************************************************************************
All checkings related to Demand Point
 ***************************************************************************/
"""
from qgis.core import *
# import own custom file
from .dropdown_enum import *
from .rps_utility import *

layer_name = 'Demand_Point'
dmd_pt_field_null_code = 'ERR_DEMANDPT_01'
dmd_pt_enum_valid_code = 'ERR_DEMANDPT_02'
dmd_pt_duplicate_code = 'ERR_DUPLICATE_ID'
dmd_pt_device_id_format_code = 'ERR_DEVICE_ID'
dmd_pt_remarks_code = 'ERR_DEMANDPT_04'
dmd_pt_snapping_code = 'ERR_DEMANDPT_03'
dmd_pt_z_m_shapefile_code = 'ERR_Z_M_VALUE'

# TODO: check dist_tx value. if Unknown = Allow. If UNKNOWN = dont allow
# TODO: house number, street name (allow N/A)

# *****************************************
# ****** Check Z-M Value in shapefile *****
# *****************************************

def dmd_pt_z_m_shapefile():
    arr = []
    arr = rps_z_m_shapefile(layer_name)
    return arr


def dmd_pt_z_m_shapefile_message(device_id):
    longitude = 0
    latitude = 0
    e_msg = rps_z_m_shapefile_message(layer_name, device_id, dmd_pt_z_m_shapefile_code)
    return e_msg


# ****************************************
# ****** Check for Device_Id Format ******
# ****************************************

def dmd_pt_device_id_format():
    arr = []
    print('running demand point device id format check')
    arr = rps_device_id_format(layer_name)
    print('total error demand is ' + str(len(arr)))
    return arr


def dmd_pt_device_id_format_message(device_id):
    e_msg = rps_device_id_format_message(layer_name, device_id, dmd_pt_z_m_shapefile_code)
    return e_msg


# **********************************
# ****** Check for Duplicates ******
# **********************************

def dmd_pt_duplicate():
    arr = rps_duplicate_device_id(layer_name)
    return arr


def dmd_pt_duplicate_message(device_id):
    longitude = 0
    latitude = 0
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    query = '"device_id" = \'' + str(device_id) + '\''
    feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
    err_count = 0
    for f in feat:
        try:
            geom = f.geometry()
            if geom:
                point = rps_get_qgspoint(geom)
                longitude = point.x()
                latitude = point.y()
        except Exception as e:
            err_count += 1
    e_msg = dmd_pt_duplicate_code + ',' + str(device_id) + ',' + layer_name + ': ' + str(
        device_id) + ' duplicated device_id: ' + str(device_id) + ',' + str(longitude) + ',' + str(latitude) + ' \n'
    return e_msg


# **********************************
# ****** Check for Enum Value ******
# **********************************

def dmd_pt_field_enum(field_name):
    arr = []
    arr_drop_down = []
    if field_name == 'status':
        arr_drop_down = arr_status
    elif field_name == 'db_oper':
        arr_drop_down = arr_db_oper
    else:
        arr_drop_down = []

    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    feat = layer.getFeatures()
    for f in feat:
        device_id = f.attribute('device_id')
        field_value = f.attribute(field_name)
        if field_value not in arr_drop_down:
            arr.append(device_id)
    return arr


def dmd_pt_field_enum_message(device_id, field_name):
    longitude = 0
    latitude = 0
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    query = '"device_id" = \'' + str(device_id) + '\''
    feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
    err_count = 0
    for f in feat:
        try:
            geom = f.geometry()
            if geom:
                point = rps_get_qgspoint(geom)
                longitude = point.x()
                latitude = point.y()
        except Exception as e:
            err_count += 1
    e_msg = dmd_pt_enum_valid_code + ',' + str(device_id) + ',' + layer_name + ': ' + str(
        device_id) + ' Invalid Enumerator at: ' + field_name + ',' + str(longitude) + ',' + str(latitude) + ' \n'
    return e_msg


# **********************************
# ****** Check for Not Null   ******
# **********************************

def dmd_pt_field_not_null(field_name):
    arr = rps_field_not_null(layer_name, field_name)
    return arr


def dmd_pt_field_not_null_message(device_id, field_name):
    e_msg = rps_field_not_null_message(device_id, field_name, layer_name, dmd_pt_field_null_code)
    return e_msg


# ***************************************
# ********* Check for Remarks  **********
# ***************************************

'''
# Step 1 : list down all demand point device id from Street Light
# Step 2 : check Demand Point where Device Id in arr_device_id
# Step 3 : check Remarks column. Remarks must be == 'STREET LIGHT PANEL'
'''


def dmd_pt_remarks():
    arr = []
    arr_dmd_pnt_id = get_dmd_pnt_id()
    # print(arr_dmd_pnt_id)
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    feat = layer.getFeatures()
    for f in feat:
        device_id = f.attribute('device_id')
        if device_id in arr_dmd_pnt_id:
            remarks = f.attribute('remarks')
            if remarks != 'STREET LIGHT PANEL':
                arr.append(device_id)
    return arr


def get_dmd_pnt_id():
    arr_dmd_pnt_id = []
    layer = QgsProject.instance().mapLayersByName('Street_Light')[0]
    query = '"dmd_pnt_id" is not null'
    feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
    for f in feat:
        dmd_pnt_id = f.attribute('dmd_pnt_id')
        arr_dmd_pnt_id.append(dmd_pnt_id)

    return arr_dmd_pnt_id;


def dmd_pt_remarks_message(device_id):
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    query = '"device_id" = \'' + str(device_id) + '\''
    feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
    longitude = 0
    latitude = 0
    err_count = 0
    for f in feat:
        try:
            geom = f.geometry()
            if geom:
                point = rps_get_qgspoint(geom)
                longitude = point.x()
                latitude = point.y()
        except Exception as e:
            err_count += 1

    e_msg = dmd_pt_remarks_code + ',' + str(device_id) + ',' + layer_name + ': ' + str(
        device_id) + ' remarks must be STREET LIGHT PANEL' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
    return e_msg


# **********************************************************************
# ********* Check for Demand Point not in end point/snapping  **********
# **********************************************************************

'''
# Step 1: Get geometry of all conductors (LV UG, LV OH)
# Step 2: Get last vertex of all geometry of Step 1
# Step 3: Get geometry of all demand point
# Step 4: Geometry of demand point must snap to at least one of LV UG/LV OH
# Step 5: if not snap to any cable == error
'''


def dmd_pt_snapping():
    arr = []
    arr_lv_vertex = []
    # qgis distanceArea
    distance = QgsDistanceArea()
    distance.setEllipsoid('WGS84')

    # Get geometry of LV OH, LV UG
    arr_layer_name = ['LV_OH_Conductor', 'LV_UG_Conductor']
    for lyr in arr_layer_name:
        layer_lv_01 = QgsProject.instance().mapLayersByName(lyr)[0]
        feat_lv_01 = layer_lv_01.getFeatures()
        # query = '"device_id" = \'' + 'RPS6122ohc724' + '\''
        # feat_lv_01 = layer_lv_01.getFeatures(QgsFeatureRequest().setFilterExpression(query))

        for f in feat_lv_01:
            dev_id_temp = f.attribute('device_id')
            geom = f.geometry()
            display_str = QgsWkbTypes.displayString(geom.wkbType())
            geom_get = geom.get()
            if display_str != 'Unknown' and geom_get.isEmpty() == False:
                y = geom.mergeLines()
                y_type = QgsWkbTypes.displayString(y.wkbType())
                # if y_type != 'LineString':
                #        print(dev_id_temp + ' ' + QgsWkbTypes.displayString(y.wkbType()))
                if y_type != 'MultiLineString':
                    # Get first vertex
                    arr_lv_vertex.append(y.asPolyline()[0])
                    # Get last vertex
                    arr_lv_vertex.append(y.asPolyline()[len(y.asPolyline()) - 1])

    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    feat = layer.getFeatures()

    err_counter = 0
    for f in feat:
        device_id = f.attribute('device_id')
        geom = f.geometry()
        display_str = QgsWkbTypes.displayString(geom.wkbType())
        # new arr_snapping each loop
        arr_snapping = []
        # loop through all LV OH & LV UG
        for geom_lv in arr_lv_vertex:
            try:
                geom_x = rps_get_qgspoint(geom)
                m = distance.measureLine(geom_lv, geom_x)
                # if m < 0.001 or str(m) == 'nan':
                if m < 0.001:
                    arr_snapping.append(device_id)
                # elif m >= 0.001 and m < 0.01:
                #        print(device_id + ' distance is ' + str("{:.5f}".format(m)))
            except Exception as e:
                err_counter += 1

        if len(arr_snapping) == 0:
            arr.append(device_id)
    print('total error is ' + str(err_counter))
    return arr


def dmd_pt_snapping_message(device_id):
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
    e_msg = dmd_pt_snapping_code + ',' + str(device_id) + ',' + layer_name + ': ' + str(
        device_id) + ' hanging' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
    return e_msg

# **********************************
# ******* End of Validation  *******
# **********************************
