# -*- coding: utf-8 -*-
"""
/***************************************************************************
All checkings related to LV UG conductor 
 ***************************************************************************/
"""
from qgis.core import *
# import own custom file
from .dropdown_enum import *
from .rps_utility import *
# regex
import re

layer_name = 'LV_UG_Conductor'
lv_ug_field_not_null_code = 'ERR_LVUGCOND_01'
lv_ug_enum_valid_code = 'ERR_LVUGCOND_02'
lv_ug_lv_db_in_out_col_code = 'ERR_LVUGCOND_03'
lv_ug_lv_db_in_out_geom_code = 'ERR_LVUGCOND_04'
lv_ug_length_code = 'ERR_LVUGCOND_05'
lv_ug_coin_code = 'ERR_LVUGCOND_06'
lv_ug_hanging_code = 'ERR_LVUGCOND_07'
lv_ug_1_2_incoming_code = 'ERR_LVUGCOND_08'
lv_ug_1_2_outgoing_code = 'ERR_LVUGCOND_08'
lv_ug_buffer_code = 'ERR_LVUGCOND_09'
lv_ug_self_intersect_code = 'ERR_LVUGCOND_10'
lv_ug_wrong_flow_code = 'ERR_LVUGCOND_11'
lv_ug_duplicate_code = 'ERR_DUPLICATEID'
lv_ug_device_id_format_code = 'ERR_DEVICE_ID'
lv_ug_z_m_shapefile_code = 'ERR_Z_M_VALUE'
lv_ug_angle_mismatch_code = 'ERR_LVUGCOND_12'

# this number is the max number to test for hanging.
# if total LV UG is more than this number, test for hanging is skipped
lv_ug_max_count = 1500


# *****************************************
# ****** Check Z-M Value in shapefile *****
# *****************************************

def lv_ug_z_m_shapefile():
    arr = []
    arr = rps_z_m_shapefile(layer_name)
    # print('z m error is ' + str(len(arr)))
    return arr


def lv_ug_z_m_shapefile_message(device_id):
    longitude = 0
    latitude = 0
    e_msg = rps_z_m_shapefile_message(layer_name, device_id, lv_ug_z_m_shapefile_code)
    return e_msg


# ****************************************
# ****** Check for Device_Id Format ******
# ****************************************

def lv_ug_device_id_format():
    arr = []
    arr = rps_device_id_format(layer_name)
    return arr


def lv_ug_device_id_format_message(device_id):
    e_msg = rps_device_id_format_message(layer_name, device_id, lv_ug_device_id_format_code)
    return e_msg


# **********************************
# ****** Check for Duplicates ******
# **********************************

def lv_ug_duplicate():
    arr = []
    arr = rps_duplicate_device_id(layer_name)
    return arr


def lv_ug_duplicate_message(device_id):
    longitude = 0
    latitude = 0

    midpoint = rps_get_midpoint(layer_name, device_id)
    if midpoint:
        longitude = midpoint.x()
        latitude = midpoint.y()

    e_msg = lv_ug_duplicate_code + ',' + str(device_id) + ',' + 'LV_UG_Conductor: ' + str(
        device_id) + ' duplicated device_id: ' + str(device_id) + ',' + str(longitude) + ',' + str(latitude) + ' \n'
    return e_msg


# **********************************
# ****** Check for Enum Value ******
# **********************************

def lv_ug_field_enum(field_name):
    arr = []
    arr_drop_down = []
    if field_name == 'status':
        arr_drop_down = arr_status
    elif field_name == 'phasing':
        arr_drop_down = arr_phasing
    elif field_name == 'usage':
        arr_drop_down = arr_usage
    elif field_name == 'label':
        arr_drop_down = arr_label_lv_ug
    elif field_name == 'dat_qty_cl':
        arr_drop_down = arr_dat_qty_cl
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


def lv_ug_field_enum_message(device_id, field_name):
    longitude = 0
    latitude = 0

    midpoint = rps_get_midpoint(layer_name, device_id)
    if midpoint:
        longitude = midpoint.x()
        latitude = midpoint.y()

    e_msg = lv_ug_enum_valid_code + ',' + str(device_id) + ',' + 'LV_UG_Conductor: ' + str(
        device_id) + ' Invalid Enumerator at: ' + field_name + ',' + str(longitude) + ',' + str(latitude) + ' \n'
    return e_msg


# **********************************
# ****** Check for Not Null   ******
# **********************************

def lv_ug_field_not_null(field_name):
    arr = rps_field_not_null(layer_name, field_name)
    return arr


def lv_ug_field_not_null_message(device_id, field_name):
    longitude = 0
    latitude = 0

    midpoint = rps_get_midpoint(layer_name, device_id)
    if midpoint:
        longitude = midpoint.x()
        latitude = midpoint.y()

    e_msg = lv_ug_field_not_null_code + ',' + str(device_id) + ',' + 'LV_UG_Conductor: ' + str(
        device_id) + ' Mandatory field NOT NULL at: ' + field_name + ',' + str(longitude) + ',' + str(latitude) + ' \n'
    return e_msg


# **********************************
# ****** Check for LVDB Flow  ******
# **********************************

'''
# Step 1: get lvdb device id from in_lvdb_id column
# Step 2: if in_lvdb_id is not null, get its geometry from LVDB-FP layer
# step 3: get geometry from lv ug conductor and change it to vector list
# Step 4: since its incoming, meaning last vector of lv ug conductor must be the closest to lvdb
# Step 5: check distance between last vector of lv ug and lvdb
# Step 6: if too far (more than 0.001m) meaning its not incoming
'''


def lv_ug_lv_db_in(arr_lv_ug_exclude_geom):
    arr = []
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    feat = layer.getFeatures()
    for f in feat:
        device_id = f.attribute('device_id')
        if device_id not in arr_lv_ug_exclude_geom:
            lv_db_device_id = f.attribute('in_lvdb_id')
            g_line = f.geometry()
            y = g_line.mergeLines()
            if lv_db_device_id:
                layer_lv_db = QgsProject.instance().mapLayersByName('LVDB-FP')[0]
                query = '"device_id" = \'' + lv_db_device_id + '\''
                feat_lv_db = layer_lv_db.getFeatures(QgsFeatureRequest().setFilterExpression(query))
                for lv_db in feat_lv_db:
                    geom = lv_db.geometry()
                    if geom:
                        geom_x = rps_get_qgspoint(geom)
                        distance = QgsDistanceArea()
                        distance.setEllipsoid('WGS84')
                        distance_xy = distance.measureLine(y.asPolyline()[len(y.asPolyline()) - 1], geom_x)
                        if distance_xy > 0.001:
                            # print("WARNING: incoming distance > 0")
                            # print("Point1 (LVUG):", y.asPolyline()[len(y.asPolyline())-1])
                            # print("Point2 (LVDB):", geom_x)
                            # print("difference:", format(distance_xy,'.9f'))
                            arr.append(device_id)

    return arr


def lv_ug_lv_db_in_message(device_id):
    longitude = 0
    latitude = 0

    last_point = rps_get_lastpoint(layer_name, device_id)
    if last_point:
        longitude = last_point.x()
        latitude = last_point.y()

    e_msg = lv_ug_lv_db_in_out_geom_code + ',' + str(device_id) + ',' + 'LV_UG_Conductor: ' + str(
        device_id) + ' column in_lvdb_id mismtach ' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
    return e_msg


def lv_ug_lv_db_out(arr_lv_ug_exclude_geom):
    arr = []
    distance = QgsDistanceArea()
    distance.setEllipsoid('WGS84')
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    feat = layer.getFeatures()
    for f in feat:
        device_id = f.attribute('device_id')
        if device_id not in arr_lv_ug_exclude_geom:
            g_line = f.geometry()
            y = g_line.mergeLines()
            out_lvdb_id = f.attribute('out_lvdb_i')

            if out_lvdb_id:
                layer_lvdb = QgsProject.instance().mapLayersByName('LVDB-FP')[0]
                query = '"device_id" = \'' + out_lvdb_id + '\''
                feat_lvdb = layer_lvdb.getFeatures(QgsFeatureRequest().setFilterExpression(query))
                for lvdb in feat_lvdb:
                    geom = lvdb.geometry()
                    if geom:
                        geom_x = rps_get_qgspoint(geom)
                        distance_xy = distance.measureLine(y.asPolyline()[0], geom_x)
                        if distance_xy > 0.001:
                            # print("WARNING: outgoing distance > 0:")
                            # print("Point1 (LVUG):",y.asPolyline()[0])
                            # print("Point2 (LVDB):",geom_x)
                            # print("difference:", format(distance_xy, '.9f'))
                            arr.append(device_id)
    return arr


def lvug_lvdb_out_message(device_id):
    longitude = 0
    latitude = 0

    first_point = rps_get_firstpoint(layer_name, device_id)
    if first_point:
        longitude = first_point.x()
        latitude = first_point.y()

    e_msg = lv_ug_lv_db_in_out_geom_code + ',' + str(device_id) + ',' + 'LV_UG_Conductor: ' + str(
        device_id) + ' column out_lvdb_id mismatch' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
    return e_msg


# ************************************
# ****** Check for LVDB in/out  ******
# ************************************

def lv_ug_lvdb_id_in_check():
    arr = []
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    # query = '"in_lvdb_id" is not null OR "out_lvdb_i" is not null'
    query = '"in_lvdb_id" is not null'
    feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
    for f in feat:
        device_id = f.attribute('device_id')
        in_lvdb_id = f.attribute('in_lvdb_id')
        lvdb_in_no = f.attribute('lvdb_in_no')
        # out_lvdb_i = f.attribute('out_lvdb_i')
        # lvdb_out_no = f.attribute('lvdb_ot_no')
        if in_lvdb_id:
            if not lvdb_in_no:
                arr.append(device_id)
    return arr


def lv_ug_lvdb_id_out_check():
    arr = []
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    # query = '"in_lvdb_id" is not null OR "out_lvdb_i" is not null'
    query = '"out_lvdb_i" is not null'
    feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
    for f in feat:
        device_id = f.attribute('device_id')
        # in_lvdb_id = f.attribute('in_lvdb_id')
        # lvdb_in_no = f.attribute('lvdb_in_no')
        out_lvdb_i = f.attribute('out_lvdb_i')
        lvdb_out_no = f.attribute('lvdb_ot_no')
        if out_lvdb_i:
            if not lvdb_out_no:
                arr.append(device_id)
    return arr


def lv_ug_lvdb_no_in_check():
    arr = []
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    # query = '"lvdb_in_no" is not null OR "lvdb_ot_no" is not null'
    query = '"lvdb_in_no" is not null'
    feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
    for f in feat:
        device_id = f.attribute('device_id')
        in_lvdb_id = f.attribute('in_lvdb_id')
        lvdb_in_no = f.attribute('lvdb_in_no')
        # out_lvdb_i = f.attribute('out_lvdb_i')
        # lvdb_out_no = f.attribute('lvdb_ot_no')
        if lvdb_in_no:
            if not in_lvdb_id:
                arr.append(device_id)
    return arr


def lv_ug_lvdb_no_out_check():
    arr = []
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    query = '"lvdb_ot_no" is not null'
    feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
    for f in feat:
        device_id = f.attribute('device_id')
        # in_lvdb_id = f.attribute('in_lvdb_id')
        # lvdb_in_no = f.attribute('lvdb_in_no')
        out_lvdb_i = f.attribute('out_lvdb_i')
        lvdb_out_no = f.attribute('lvdb_ot_no')
        if lvdb_out_no:
            if not out_lvdb_i:
                arr.append(device_id)
    return arr


def lv_ug_lvdb_id_check_message(device_id):
    longitude = 0
    latitude = 0

    midpoint = rps_get_midpoint(layer_name, device_id)
    if midpoint:
        longitude = midpoint.x()
        latitude = midpoint.y()

    e_msg = lv_ug_lv_db_in_out_col_code + ',' + str(device_id) + ',' + 'LV_UG_Conductor: ' + str(
        device_id) + ' lvdb_in_no/lvdb_ot_no MISSING' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
    return e_msg


def lv_ug_lvdb_no_check_message(device_id):
    longitude = 0
    latitude = 0

    midpoint = rps_get_midpoint(layer_name, device_id)
    if midpoint:
        longitude = midpoint.x()
        latitude = midpoint.y()

    e_msg = lv_ug_lv_db_in_out_col_code + ',' + str(device_id) + ',' + 'LV_UG_Conductor: ' + str(
        device_id) + ' lvdb_in_id/lvdb_out_i MISSING' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
    return e_msg


# **********************************
# ********* Check Length  **********
# **********************************

def lv_ug_length_check():
    arr = []
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    query = '"length" < 1.5'
    feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
    for f in feat:
        device_id = f.attribute('device_id')
        arr.append(device_id)
    return arr


def lv_ug_length_check_message(device_id):
    longitude = 0
    latitude = 0

    midpoint = rps_get_midpoint(layer_name, device_id)
    if midpoint:
        longitude = midpoint.x()
        latitude = midpoint.y()

    e_msg = lv_ug_length_code + ',' + str(device_id) + ',' + layer_name + ': ' + str(
        device_id) + ' length less than 1.5' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
    return e_msg


# ********************************************
# ****** Check for LVDB 1st/2nd Vertex  ******
# ********************************************

'''
# Step 1: get LV UG device ID which are connected to LVDB
# Step 2: get nearest Vertex to LVDB. this will be Vertex [0] / Last vertex
# Step 3: get the 2nd nearest vertex. this will be Vertex [1] / 2nd last vertex
# Step 4: get distance between these 2 points
# Step 5: if distance < 1m, then error
'''


def get_lvdb_by_device_id(device_id):
    layer = QgsProject.instance().mapLayersByName('LVDB-FP')[0]
    query = '"device_id" = \'' + str(device_id) + '\''
    feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
    for f in feat:
        device_id = f.attribute('device_id')
        geom = f.geometry()
    return geom


def lv_ug_1_2_incoming(arr_lv_ug_exclude_geom):
    arr = []
    # qgis distanceArea
    distance = QgsDistanceArea()
    distance.setEllipsoid('WGS84')

    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    feat = layer.getFeatures()
    for f in feat:
        device_id = f.attribute('device_id')
        if device_id not in arr_lv_ug_exclude_geom:
            # get geometry of LV UG
            geom = f.geometry()
            try:
                y = geom.mergeLines()
                polyline_y = y.asPolyline()
                # get incoming and outgoing distance
                # distance_0 = distance.measureLine(polyline_y[0],polyline_y[1])
                distance_n = distance.measureLine(polyline_y[len(polyline_y) - 1], polyline_y[len(polyline_y) - 2])
                # get incoming/outgoing lvdb, if any
                in_lv_db_device_id = f.attribute('in_lvdb_id')
                if in_lv_db_device_id and distance_n < 1:
                        # print(device_id + '/' + in_lv_db_device_id + ' incoming dist is ' + str(distance_n))
                        arr.append(device_id)
            except Exception as e:
                arr.append(device_id)
    return arr


def lv_ug_1_2_incoming_message(device_id):
    longitude = 0
    latitude = 0

    last_point = rps_get_lastpoint(layer_name, device_id)
    if last_point:
        longitude = last_point.x()
        latitude = last_point.y()

    e_msg = lv_ug_1_2_incoming_code + ',' + str(device_id) + ',' + layer_name + ': ' + str(
        device_id) + ' INCOMING vertex to LVDB-FP must be more than 1.0m' + ',' + str(longitude) + ',' + str(
        latitude) + ' \n'
    return e_msg


def lv_ug_1_2_outgoing(arr_lv_ug_exclude_geom):
    arr = []
    # qgis distanceArea
    distance = QgsDistanceArea()
    distance.setEllipsoid('WGS84')

    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    feat = layer.getFeatures()
    for f in feat:
        device_id = f.attribute('device_id')
        if device_id not in arr_lv_ug_exclude_geom:
            try:

                # get geometry of LV UG
                geom = f.geometry()
                y = geom.mergeLines()
                polyline_y = y.asPolyline()
                # get incoming and outgoing distance
                distance_0 = distance.measureLine(polyline_y[0], polyline_y[1])
                # distance_n = distance.measureLine(polyline_y[len(polyline_y) - 1],polyline_y[len(polyline_y) - 2])
                # get incoming/outgoing lvdb, if any
                out_lv_db_device_id = f.attribute('out_lvdb_i')
                if out_lv_db_device_id and distance_0 < 1:
                    # print(device_id + '/' + out_lv_db_device_id + ' outgoing distance is ' + str(distance_0))
                    arr.append(device_id)

            except Exception as e:
                arr.append(device_id)

    return arr


def lv_ug_1_2_outgoing_message(device_id):
    longitude = 0
    latitude = 0

    second_point = rps_get_secondpoint(layer_name, device_id)
    if second_point:
        longitude = second_point.x()
        latitude = second_point.y()

    e_msg = lv_ug_1_2_outgoing_code + ',' + str(device_id) + ',' + layer_name + ': ' + str(
        device_id) + ' OUTGOING vertex from LVDB-FP must be more than 1.0m' + ',' + str(longitude) + ',' + str(
        latitude) + ' \n'
    return e_msg


# ***************************************************
# ********* Check self Intersect  *******************
# ***************************************************
'''
# Step 1: convert geom to polyline
# Step 2: extract all vectors
# Step 3: create lines using vector[i] and vector[i+1]
# Step 4: check each line against all other lines (loop)
# Step 5: add +1 to number of intersection for first and last lines
# Step 6: count intersection
# Step 7: if intersection >= 3, means self intersect
'''


def lv_ug_self_intersect(arr_exclude_geom):
    arr = []
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    # query = '"device_id" = \'' + 'R6142ugc031' + '\''
    # feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
    feat = layer.getFeatures()

    for f in feat:
        device_id = f.attribute('device_id')
        geom = f.geometry()
        display_str = QgsWkbTypes.displayString(geom.wkbType())
        # print(device_id + ' display string is: ' + display_str)
        try:
            if device_id not in arr_exclude_geom:
                y = geom.mergeLines()
                poly_line_y = y.asPolyline()

                arr_line = []
                for i in range(len(poly_line_y)):
                    geom_i = poly_line_y[i]
                    if i < len(poly_line_y) - 1:
                        geom_i2 = poly_line_y[i + 1]
                        arr_temp_line = [QgsPoint(geom_i), QgsPoint(geom_i2)]
                        new_line = QgsGeometry.fromPolyline(arr_temp_line)
                        arr_line.append(new_line)

                # print(str(len(polyLine_y)) + ' vector(s) found, with ' + str(len(arr_line)) + ' total lines')
                for h in range(len(arr_line)):
                    arr_temp = []
                    arr_temp.extend(arr_line)
                    # remove self
                    arr_temp.remove(arr_line[h])
                    no_of_intersect = 0
                    # for first lines and last line, we (+1) so that all lines will have 2 intersect points at the start
                    if h == 0 or h == len(arr_line) - 1:
                        no_of_intersect += 1
                    for i in range(len(arr_temp)):
                        intersect = QgsGeometry.intersection(arr_line[h], arr_temp[i])
                        if intersect:
                            no_of_intersect += 1
                    # print('intersect: ' + str(no_of_intersect))
                    # remove duplicate device_id
                    if no_of_intersect > 2 and device_id not in arr:
                        arr.append(device_id)
        except Exception as e:
            # print('I found one error SELF INTERSECT! ' + device_id)
            arr.append(device_id)

    return arr


'''
# copy from function above
'''


def lv_ug_self_intersect_message(device_id):
    longitude = 0
    latitude = 0

    geom = rps_get_midpoint(layer_name, device_id)
    if geom:
        longitude = geom.x()
        latitude = geom.y()

    e_msg = lv_ug_self_intersect_code + ',' + str(device_id) + ',' + layer_name + ': ' + str(
        device_id) + ' has self intersect geometry ' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
    return e_msg


# *******************************
# ****** Hanging Geometry  ******
# *******************************

'''
# Get vertex[0] and vertex[last] from LV UG Conductor
# List down all possible vertext that these two might connect to:
# - all other vectors in LV UG
# - vector[0] and vector[last] in LV OH
# - Demand Point
# - LV Cable Joint
# check if the vertex[0] is connected to any of those above.
# check if the vertex[last] is connected to any of those above.
# if not connected to anything, return error
'''


def lv_ug_hanging(arr_lv_ug_exclude_geom, arr_lv_oh_exclude_geom):
    arr = []
    # qgis distanceArea
    distance = QgsDistanceArea()
    distance.setEllipsoid('WGS84')

    # for debugging purpose
    # print(arr_lv_ug_exclude_geom)
    # print(arr_lv_oh_exclude_geom)

    # get all LV UG vertex
    arr_point = []
    layer_lv_ug = QgsProject.instance().mapLayersByName(layer_name)[0]
    feat_lv_ug = layer_lv_ug.getFeatures()
    for g in feat_lv_ug:
        device_temp = g.attribute('device_id')
        if device_temp not in arr_lv_ug_exclude_geom:
            geom_g = g.geometry()
            if geom_g:
                y_g = geom_g.mergeLines()
                polyline_y_g = y_g.asPolyline()
                for g1 in range(len(polyline_y_g)):
                    if polyline_y_g[g1] not in arr_point:
                        arr_point.append(polyline_y_g[g1])

    # get all Demand Point vertex
    layer_dmd_pt = QgsProject.instance().mapLayersByName('Demand_Point')[0]
    feat_dmd_pt = layer_dmd_pt.getFeatures()
    for j in feat_dmd_pt:
        geom_j = j.geometry()
        if geom_j:
            j_point = rps_get_qgspoint(geom_j)
            arr_point.append(j_point)

    # 14/8/2020: get all LVDB-FP vertex
    layer_lv_db_fp = QgsProject.instance().mapLayersByName('LVDB-FP')[0]
    feat_lv_db_fp = layer_lv_db_fp.getFeatures()
    for j in feat_lv_db_fp:
        geom_j = j.geometry()
        if geom_j:
            j_point = rps_get_qgspoint(geom_j)
            arr_point.append(j_point)
    
    # 14/8/2020: get all LV Cable Joint vertex
    layer_lv_cj = QgsProject.instance().mapLayersByName('LV_Cable_Joint')[0]
    feat_lv_cj = layer_lv_cj.getFeatures()
    for j in feat_lv_cj:
        geom_j = j.geometry()
        if geom_j:
            j_point = rps_get_qgspoint(geom_j)
            arr_point.append(j_point)

    # 29/6/2020 - changed from only read start and end of LV OH, instead check all vectors
    # 20/7/2020 - get all LV OH vertex (1st and last)
    layer_lv_oh = QgsProject.instance().mapLayersByName('LV_OH_Conductor')[0]
    feat_lv_oh = layer_lv_oh.getFeatures()
    for h in feat_lv_oh:
        device_temp = h.attribute('device_id')
        if device_temp not in arr_lv_oh_exclude_geom:
            geom_h = h.geometry()
            if geom_h:
                y_h = geom_h.mergeLines()
                # print('current polyline to check is ' + device_temp)
                polyline_y = y_h.asPolyline()
                for i in range(len(polyline_y)):
                    vector = polyline_y[i]
                    arr_point.append(vector)

    print('total vectors to check are = ' + str(len(arr_point)))

    # main calculation
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    # query = '"device_id" = \'' + 'R6142ugc017' + '\''
    # feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
    feat = layer.getFeatures()
    feat_count = layer.featureCount()
    if feat_count > lv_ug_max_count:
        print('too many objects: skipped checking for LV UG hanging')
    else:
        for f in feat:
            device_id = f.attribute('device_id')
            if device_id not in arr_lv_ug_exclude_geom:
                geom = f.geometry()
                if geom:
                    y = geom.mergeLines()
                    polyline_y = y.asPolyline()
                    v_one = polyline_y[0]
                    v_last = polyline_y[len(polyline_y) - 1]
                    # print('len polyline is ', len(polyline_y))
                    # print('arr point is:' + str(len(arr_point)))

                    # check distance between v_one / v_last with arr_point
                    arr_snap_v_one = []
                    arr_snap_v_last = []
                    for v_point in arr_point:
                        bool_test = rps_is_too_close(v_one, v_point)
                        if bool_test:
                            distance_v_one = distance.measureLine(v_one, v_point)
                            if distance_v_one <= 0.001:
                                # print(j)
                                # print('distance is ' + format(distance_xy,'.9f') + 'm')
                                arr_snap_v_one.append(device_id)
                        bool_test = rps_is_too_close(v_last, v_point)
                        if bool_test:
                            distance_v_last = distance.measureLine(v_last, v_point)
                            if distance_v_last <= 0.001:
                                # print('v last is ' + str(v_last))
                                # print('lv point is ' + str(v_point))
                                # print('distance is ' + format(distance_v_last,'.9f') + 'm')
                                arr_snap_v_last.append(device_id)
                        if len(arr_snap_v_one) > 1 and len(arr_snap_v_last) > 1:
                            break  # break out of for loop
                    if len(arr_snap_v_one) <= 1 or len(arr_snap_v_last) <= 1:
                        arr.append(device_id)

    return arr


# 20 / 7 / 2020 simplify how to zoom to LV location
def lv_ug_hanging_message(device_id):
    longitude = 0
    latitude = 0

    geom = rps_get_lastpoint(layer_name, device_id)
    if geom:
        longitude = geom.x()
        latitude = geom.y()

    e_msg = lv_ug_hanging_code + ',' + str(device_id) + ',' + layer_name + ': ' + str(
        device_id) + ' is hanging ' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
    return e_msg


# ********************************************
# ****** Check for Coincidence Geometry ******
# ********************************************

def lv_ug_coin():
    arr = []
    arr_geom = []
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    feat = layer.getFeatures()

    # create 1st loop to store all geom
    for f in feat:
        geom = f.geometry()
        geom_f = geom.mergeLines()
        arr_geom.append(geom_f)

        # create another loop
        for g in feat:
            device_id = g.attribute('device_id')
            geom = g.geometry()
            geom_g = geom.mergeLines()
            for geom_2 in arr_geom:
                # check for overlap
                if geom_g.overlaps(geom_2):
                    arr.append(device_id)
    return arr


def lv_ug_coin_message(device_id):
    longitude = 0
    latitude = 0

    e_msg = lv_ug_coin_code + ',' + str(device_id) + ',' + layer_name + ': ' + str(
        device_id) + ' has coincidence geometry ' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
    return e_msg


# *************************************************
# ****** Buffer between LV UG must be > 0.3  ******
# *************************************************

# get all vertex of a LV UG conductor
# check distance between this vertex and other vertex of another conductor

'''
# buat last
'''


def get_all_lv_ug_vector(arr_exclude_geom):
    arr_lv_ug = []
    # get vectors of all LV UG (for comparison)
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    feat = layer.getFeatures()
    for f in feat:
        device_id = f.attribute('device_id')
        geom = f.geometry()
        if device_id not in arr_exclude_geom:
            try:
                y = geom.mergeLines()
                polyline_y = y.asPolyline()
                for geom_y in polyline_y:
                    arr_lv_ug.append(geom_y)
            except Exception as e:
                print('failed to read geometry!' + str(e))

    return arr_lv_ug


def lv_ug_buffer(arr_lv_ug_exclude_geom):
    arr = []
    arr_lv_ug = []

    # qgis distanceArea
    distance = QgsDistanceArea()
    distance.setEllipsoid('WGS84')

    arr_lv_ug = get_all_lv_ug_vector(arr_lv_ug_exclude_geom)

    # main function
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    feat = layer.getFeatures()
    for f in feat:
        # reset array values
        arr_temp = []
        arr_temp.extend(arr_lv_ug)
        arr_cur_lv_ug = []

        # get arr_cur_lv_ug (list of vectors to in one device id)
        device_id = f.attribute('device_id')
        if device_id not in arr_lv_ug_exclude_geom:
            try:
                geom = f.geometry()
                y = geom.mergeLines()
                polyline_y = y.asPolyline()
                for geom_y in polyline_y:
                    arr_cur_lv_ug.append(geom_y)

                # remove own vector from arr_temp
                for cur_lv_ug in arr_cur_lv_ug:
                    arr_temp.remove(cur_lv_ug)

                arr_too_close = []
                arr_too_far = []

                for i in range(len(arr_cur_lv_ug)):
                    # remove first and last vertex from checking
                    if 0 < i < len(arr_cur_lv_ug) - 1:
                        for vector_all in arr_temp:
                            vector = arr_cur_lv_ug[i]
                            m = distance.measureLine(vector, vector_all)
                            if 0.29 > m > 0.005:
                                # print(device_id + '[' + str(i + 1) + '/' + str(len(arr_cur_lv_oh)) + ']' + ' is too
                                # close to another conductor!')
                                arr_too_close.append(device_id)
                            elif 0.31 < m < 0.5:
                                # print(device_id + ' is too far from another conductor')
                                arr_too_far.append(device_id)
                if len(arr_too_close) > 0:
                    arr.append(device_id)
            except Exception as e:
                print('lv ug buffer error: ' + str(e))
                arr.append(device_id)

    return arr


'''
# copy back the method above, but only do it for one device id
'''


def lv_ug_buffer_message(device_id):
    longitude = 0
    latitude = 0

    geom = rps_get_lastpoint(layer_name, device_id)
    if geom:
        longitude = geom.x()
        latitude = geom.y()

    e_msg = lv_ug_buffer_code + ',' + str(device_id) + ',' + layer_name + ': ' + str(
        device_id) + ' is too close to another conductor! (distance < 0.3m) ' + ',' + str(longitude) + ',' + str(
        latitude) + ' \n'
    return e_msg


# ***********************************************
# ******* Check for Wrong flow direction  *******
# ***********************************************

def get_all_lv_ug_vector_outgoing(arr_lv_ug_exclude_geom, device_id_exclude):
    arr_lv_oh = []
    # get vectors of all LV OH (for comparison)
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    feat = layer.getFeatures()
    for f in feat:
        device_id = f.attribute('device_id')
        if device_id not in arr_lv_ug_exclude_geom and device_id != device_id_exclude:
            geom = f.geometry()
            if geom:
                y = geom.mergeLines()
                polyline_y = y.asPolyline()
                # if only have 2 vectors, do not add any vectors
                if len(polyline_y) > 0:
                    # add vector 0 (outgoing vector)
                   arr_lv_oh.append(polyline_y[0])

    return arr_lv_oh


def get_all_lv_ug_vector_incoming(arr_lv_ug_exclude_geom, device_id_exclude):
    arr_lv_ug = []
    # get vectors of all LV OH (for comparison)
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    feat = layer.getFeatures()
    for f in feat:
        device_id = f.attribute('device_id')
        if device_id not in arr_lv_ug_exclude_geom and device_id != device_id_exclude:
            geom = f.geometry()
            if geom:
                y = geom.mergeLines()
                polyline_y = y.asPolyline()
                # if only have 2 vectors, do not add any vectors
                if len(polyline_y) > 0:
                    # add vector last (incoming vector)
                    total_vector = len(polyline_y)
                    arr_lv_ug.append(polyline_y[total_vector - 1])

    return arr_lv_ug


def lv_ug_wrong_flow(arr_lv_ug_exclude_geom):
    arr = []

    # qgis distanceArea
    distance = QgsDistanceArea()
    distance.setEllipsoid('WGS84')

    # main function
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    feat = layer.getFeatures()
    # temporary: for testing
    # device_id_test = 'RPS6122ohc364'
    # query = '"device_id" = \'' + str(device_id_test) + '\''
    # feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))

    for f in feat:
        # get all vectors
        device_id = f.attribute('device_id')
        if device_id not in arr_lv_ug_exclude_geom:
            geom = f.geometry()
            if geom:
                y = geom.mergeLines()
                polyline_y = y.asPolyline()
                # if only have 2 vectors, do not add any vectors
                if len(polyline_y) > 0:
                    # add vector 0 (outgoing vector)
                    total_vector = len(polyline_y)
                    vector_last = polyline_y[total_vector - 1]
                    # check if any incoming LV OH vertex nearby
                    arr_lv_ug_incoming = get_all_lv_ug_vector_incoming(arr_lv_oh_exclude_geom, device_id)
                    count = arr_lv_ug_incoming.count(vector_last)
                    if count > 1:
                        # check if there is any outgoing
                        total_outgoing = 0
                        arr_lv_ug_outgoing = get_all_lv_oh_vector_outgoing(arr_lv_oh_exclude_geom, device_id)
                        for geom_lv_ug in arr_lv_ug_outgoing:
                            m = distance.measureLine(vector_last, geom_lv_ug)
                            if m < 0.001:
                                total_outgoing += 1
                                # print(device_id + ' has 2 incoming but ' + str(total_outgoing) + ' outgoing geom.')
                        if total_outgoing == 0:
                            # print(device_id + ' has no outgoing! ')
                            arr.append(device_id)

    # add demand point wrong flow error
    # print('before adding demand point wrong flow error is ' + str(len(arr)))
    arr.extend(lv_ug_wrong_flow_dmd_pt(arr_lv_ug_exclude_geom))
    # print('total wrong flow error is ' + str(len(arr)))

    return arr


def lv_ug_wrong_flow_dmd_pt(arr_lv_ug_exclude_geom):
    # Special condition: all conductors connected to demand point MUST be INCOMING.
    arr = []

    arr_dmd_pt = rps_get_all_dmd_pt()

    # qgis distanceArea
    distance = QgsDistanceArea()
    distance.setEllipsoid('WGS84')

    # main function
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    feat = layer.getFeatures()
    # temporary: for testing
    # device_id_test = 'RPS6122ohc364'
    # query = '"device_id" = \'' + str(device_id_test) + '\''
    # feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))

    for f in feat:
        device_id = f.attribute('device_id')
        if device_id not in arr_lv_ug_exclude_geom:
            geom = f.geometry()
            if geom:
                y = geom.mergeLines()
                polyline_y = y.asPolyline()
                # if only have 2 vectors, do not add any vectors
                if len(polyline_y) > 0:
                    # check distance vector 0 (outgoing) to demand point
                    vertex_zero = polyline_y[0]
                    # print('vertex zero is :' + str(vertex_zero))
                    for geom_dmd_pt in arr_dmd_pt:
                        m = distance.measureLine(vertex_zero, geom_dmd_pt)
                        if m < 0.001:
                            # means it is outgoing lv_ug, so we add lv ug's device id
                            arr.append(device_id)

    return arr


def lv_ug_wrong_flow_message(device_id):
    longitude = 0
    latitude = 0
    error_code = lv_ug_wrong_flow_code
    error_desc = str(device_id) + ' has wrong flow direction! '

    first_point = rps_get_firstpoint(layer_name, device_id)
    if first_point:
        longitude = first_point.x()
        latitude = first_point.y()

    e_msg = rps_write_line(error_code, device_id, layer_name, error_desc, longitude, latitude)
    return e_msg

# *************************************************
# ****** Angle ******
# *************************************************

def lv_ug_angle_mismatch():
    arr = []
    return arr

def lv_ug_angle_mismatch_message(device_id):
    longitude = 0
    latitude = 0
    error_code = lv_ug_wrong_flow_code
    error_desc = str(device_id) + ' has wrong flow direction! '

    first_point = rps_get_firstpoint(layer_name, device_id)
    if first_point:
        longitude = first_point.x()
        latitude = first_point.y()

    e_msg = lv_ug_angle_mismatch_code + '' + '' + ''
    return e_msg


# **********************************
# ******* End of Validation  *******
# **********************************
