# -*- coding: utf-8 -*-
"""
/***************************************************************************
Utility functions
 ***************************************************************************/
"""
from qgis.core import *
# import own custom file
from .dropdown_enum import *
import re

# *********************************************
# ****** Check for Field not null or N/A ******
# *********************************************

def rps_field_not_null(layer_name, field_name):
    arr = []
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    # TODO : if Pole No, allow N/A but don't allow NA
    query = ''
    if field_name == 'pole_no' and layer_name == 'Pole':
        query = '"' + field_name + '" is null OR ' + '"' + field_name + '" =  \'NA\''
    else:
        query = '"' + field_name + '" is null OR ' + '"' + field_name + '" =  \'N/A\''
    feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
    for f in feat:
        device_id = f.attribute('device_id')
        arr.append(device_id)
    return arr

def rps_field_not_null_message(device_id, field_name, layer_name, error_code):
    longitude = 0
    latitude = 0

    # customer has no geom, so no need to get geom
    if layer_name != 'Customer':
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + str(device_id) + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
        for f in feat:
            geom = f.geometry()
            if geom:
                # check what type of geometry (Point, Line or Error Geom)
                geom_type = QgsWkbTypes.displayString(geom.wkbType())
                # print('geom type is ' + geom_type)
                if geom_type == 'Point':
                    point = geom.asPoint()
                    longitude = point.x()
                    latitude = point.y()
                elif geom_type == 'MultiLineString':
                    midpoint = rps_get_midpoint(layer_name, device_id)
                    if midpoint:
                        longitude = midpoint.x()
                        latitude = midpoint.y()
                else:
                    longitude = 0
                    latitude = 0

    e_msg = error_code + ',' + str(device_id) + ',' + layer_name + ': ' + str(
        device_id) + ' Mandatory field NOT NULL at: ' + field_name + ',' + str(longitude) + ',' + str(latitude) + ' \n'
    return e_msg

# ****************************************
# ****** Check for Device_Id format ******
# ****************************************

code_lv_ug = 'ugc'
code_lv_oh = 'ohc'
code_lv_fuse = 'fus'
code_lv_cj = 'lcj'
code_lvdb_fp = 'lvdb'
code_pole = 'pol'
code_dmd_pt = 'dmd'
code_st_light = 'stl'
code_manhole = 'man'
code_st_duct = 'std'

'''
# Step 1: import Python Regex, re
# Step 2: Generate pattern: vendor code + station code + object code + running number
# Step 3: test device_id against pattern
'''
def rps_device_id_format(layer_name):
    arr = []
    object_code = ''
    if layer_name == 'LV_UG_Conductor':
        object_code = code_lv_ug
    elif layer_name == 'LV_OH_Conductor':
        object_code = code_lv_oh
    elif layer_name == 'LV_Fuse':
        object_code = code_lv_fuse
    elif layer_name == 'LV_Cable_Joint':
        object_code = code_lv_cj
    elif layer_name == 'LVDB-FP':
        object_code = code_lvdb_fp
    elif layer_name == 'Pole':
        object_code = code_pole
    elif layer_name == 'Demand_Point':
        object_code = code_dmd_pt
    elif layer_name == 'Street_Light':
        object_code = code_st_light
    elif layer_name == 'Manhole':
        object_code = code_manhole
    elif layer_name == 'Structure_Duct':
        object_code = code_st_duct
    else:
        object_code = 'MMM'

    vendor_code = 'RPS'
    station_code = '([1-9][0-9]{0,3})'  # accepts 1 - 9999
    running_number = '([0-9]{0,6})'  # accepts 000 - 999999
    pattern = '^' + vendor_code + station_code + object_code + running_number + '$'
    # print(pattern)

    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    feat = layer.getFeatures()
    for f in feat:
        device_id = f.attribute('device_id')
        # check for null device id
        if not device_id:
            device_id = str(device_id)
        check = re.search(pattern, device_id)
        # print('device id =' + device_id)
        # print(check)
        if not check:
            arr.append(device_id)
    print('total device id error ' + layer_name + ' = ' + str(len(arr)))
    return arr


def rps_device_id_format_message(layer_name, device_id, error_code):
    longitude = 0
    latitude = 0
    # print('enter ' + layer_name)
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    query = '"device_id" = \'' + str(device_id) + '\''
    feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
    # print('exit ' + layer_name)
    for f in feat:
        geom = f.geometry()
        if geom:
            # check what type of geometry (Point, Line or Error Geom)
            geom_type = QgsWkbTypes.displayString(geom.wkbType())
            # print('geom type is ' + geom_type)
            if geom_type == 'Point':
                point = geom.asPoint()
                longitude = point.x()
                latitude = point.y()
            elif geom_type == 'MultiLineString':
                midpoint = rps_get_midpoint(layer_name, device_id)
                if midpoint:
                    longitude = midpoint.x()
                    latitude = midpoint.y()
            else:
                longitude = 0
                latitude = 0
    e_msg = error_code + ',' + str(device_id) + ',' + layer_name + ': ' + str(
        device_id) + ' device_id format error' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
    # print(e_msg)
    return e_msg


# ***************************************************
# ********* Check for Device_Id Duplicate  **********
# ***************************************************

'''
# moved duplicate id checking (all features) to this function
# Step 1: store all device_id in array (arr_device_id)
# Step 2: loop through all [arr_device_id] and put into new array, [arr_seen]
# Step 3: if items in [arr_device_id] is already in [arr_seen], means its a duplicate
# Step 4: store all duplicate device_id in [arr_dupes]
# Step 5: skip step 4 :D
'''


def rps_duplicate_device_id(layer_name):
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


# ********************************************
# ********* Check for Z-M Geometry  **********
# ********************************************
'''
# moved all Z-M checking to this function
# Step 1: check geometry column
# Step 2: type must be correct
'''


def rps_z_m_shapefile(layer_name):
    arr = []
    wkb_type = ''

    arr_line_type = ['LV_UG_Conductor', 'LV_OH_Conductor']
    arr_point_type = ['LV_Fuse', 'LV_Cable_Joint', 'LVDB-FP', 'Pole', 'Demand_Point', 'Street_Light', 'Manhole',
                      'Structure_Duct']
    if layer_name in arr_line_type:
        wkb_type = 'MultiLineString'
    elif layer_name in arr_point_type:
        wkb_type = 'Point'
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    feat = layer.getFeatures()
    for f in feat:
        device_id = f.attribute('device_id')
        geom = f.geometry()
        if geom:
            geom_type = QgsWkbTypes.displayString(geom.wkbType())
            # print('geometry type is ', geom_type)
            if geom_type != wkb_type:
                # print('found one mismatch! ' + device_id)
                arr.append(device_id)
            elif geom_type == 'MultiLineString':
                try:
                    # try merge as polyline
                    y = geom.mergeLines()
                    polyline_y = y.asPolyline()
                except Exception as e:
                    # print('ah hah! caught you finally! ' + device_id + str(e))
                    arr.append(device_id)
        else:
            arr.append(device_id)

    return arr


def rps_z_m_shapefile_message(layer_name, device_id, error_code):
    e_msg = ''
    longitude = 0
    latitude = 0

    # correct wkb type based on layer name
    wkb_type = ''

    arr_line_type = ['LV_UG_Conductor', 'LV_OH_Conductor']
    arr_point_type = ['LV_Fuse', 'LV_Cable_Joint', 'LVDB-FP', 'Pole', 'Demand_Point', 'Street_Light', 'Manhole',
                      'Structure_Duct']

    if layer_name in arr_line_type:
        wkb_type = 'MultiLineString'
    elif layer_name in arr_point_type:
        wkb_type = 'Point'

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

        # if conductor is MultiLineString, there is possibility that the vector goes at least 2 ways
        if geom_type == 'MultiLineString' and wkb_type == 'MultiLineString':
            err_detail = layer_name + ': ' + str(
                device_id) + ' geometry ERROR. Check if possible 2 way vector direction.'
        else:
            err_detail = layer_name + ': ' + str(
            device_id) + ' geometry ERROR. Geometry is ' + geom_type + ' (correct is ' + wkb_type + ') '
    e_msg = error_code + ',' + str(device_id) + ',' + err_detail + ',' + str(longitude) + ',' + str(
        latitude) + ' \n'
    print(e_msg)

    return e_msg


# ********************************************
# ********* Get Midpoint of Line  **********
# ********************************************

def rps_get_midpoint(layer_name, device_id):
    try:

        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + device_id + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))

        vector_midpoint = QgsPoint(0, 0)

        for f in feat:
            geom = f.geometry()
            if geom:
                y = geom.mergeLines()
                polyline_y = y.asPolyline()
                # get total no of vectors
                total = len(polyline_y)
                # print('total is ', total)
                # get midpoint (no need to + 1 since the index is zero based)
                midpoint = (total // 2)
                # print('midpoint is ', divide2)
                vector_midpoint = polyline_y[midpoint]

        return vector_midpoint

    except Exception as e:
        return QgsPoint(0, 0)


# ********************************************
# ********* Get Vector Zero of Line  **********
# ********************************************

def rps_get_firstpoint(layer_name, device_id):
    try:

        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + device_id + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))

        vector_first_point = QgsPoint(0, 0)

        for f in feat:
            geom = f.geometry()
            if geom:
                # check the geom type
                geom_type = QgsWkbTypes.displayString(geom.wkbType())
                # print('geometry type is ', geom_type)
                if geom_type != 'MultiLineString':
                    y = geom.mergeLines()
                    polyline_y = y.asPolyline()
                    # get total no of vectors
                    total = len(polyline_y)
                    first_point = 0
                    # print('midpoint is ', divide2)
                    vector_first_point = polyline_y[first_point]
                else:
                    vector_first_point = QgsPoint(0,0)

        return vector_first_point
    except Exception as e:
        return QgsPoint(0, 0)


# ********************************************
# ********* Get Second Point of Line  **********
# ********************************************

def rps_get_secondpoint(layer_name, device_id):
    try:

        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + device_id + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))

        vector_second_point = QgsPoint(0, 0)

        for f in feat:
            geom = f.geometry()
            if geom:
                # check the geom type
                geom_type = QgsWkbTypes.displayString(geom.wkbType())
                # print('geometry type is ', geom_type)
                if geom_type != 'MultiLineString':
                    y = geom.mergeLines()
                    polyline_y = y.asPolyline()
                    # get total no of vectors
                    total = len(polyline_y)
                    second_point = 1
                    # print('midpoint is ', divide2)
                    vector_second_point = polyline_y[second_point]
                else:
                    return QgsPoint(0, 0)

        return vector_second_point

    except Exception as e:
        return QgsPoint(0, 0)


# ********************************************
# ********* Get Last Point of Line  **********
# ********************************************

def rps_get_lastpoint(layer_name, device_id):
    try:

        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + device_id + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))

        vector_last_point = QgsPoint(0, 0)

        for f in feat:
            geom = f.geometry()
            if geom:
                # check the geom type
                geom_type = QgsWkbTypes.displayString(geom.wkbType())
                # print('geometry type is ', geom_type)
                if geom_type != 'MultiLineString':
                    y = geom.mergeLines()
                    polyline_y = y.asPolyline()
                    # get total no of vectors
                    total = len(polyline_y)
                    last_point = total - 1
                    # print('midpoint is ', divide2)
                    vector_last_point = polyline_y[last_point]
                else:
                    return QgsPoint(0, 0)

        return vector_last_point
    except Exception as e:
        return QgsPoint(0, 0)

# **********************************
# ******* End of Validation  *******
# **********************************
