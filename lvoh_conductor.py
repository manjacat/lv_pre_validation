# -*- coding: utf-8 -*-
"""
/***************************************************************************
All checkings related to LV OH conductor 
 ***************************************************************************/
"""
from qgis.core import *
# import own custom file
from .dropdown_enum import *
from .rps_utility import *

layer_name = 'LV_OH_Conductor'
lv_oh_field_null = 'ERR_LVOHCOND_01'
lv_oh_enum_valid = 'ERR_LVOHCOND_02'
lv_oh_length_check_code = 'ERR_LVOHCOND_07'
lv_oh_duplicate_code = 'ERR_DUPLICATE_ID'
lv_oh_device_id_format_code = 'ERR_DEVICE_ID'
lv_oh_z_m_shapefile_code = 'ERR_Z_M_VALUE'
lv_oh_vertex_pole_code = 'ERR_LVOHCOND_04'
lv_oh_self_intersect_code = 'ERR_LVOHCOND_08'
lv_oh_hanging_code = 'ERR_LVOHCOND_05'
lv_oh_buffer_code = 'ERR_LVOHCOND_06'
lv_oh_wrong_flow_code = 'ERR_LVOHCOND_03'

# this number is the max number to test for hanging.
# if total LV OH is more than this number, test for hanging is skipped
lv_oh_max_count = 600


# *****************************************
# ****** Check Z-M Value in shapefile *****
# *****************************************

def lv_oh_z_m_shapefile():
    arr = []
    arr = rps_z_m_shapefile(layer_name)
    return arr


def lv_oh_z_m_shapefile_message(device_id):
    longitude = 0
    latitude = 0
    e_msg = rps_z_m_shapefile_message(layer_name, device_id, lv_oh_z_m_shapefile_code)
    return e_msg


# ****************************************
# ****** Check for Device_Id Format ******
# ****************************************

def lv_oh_device_id_format():
    arr = []
    arr = rps_device_id_format(layer_name)
    return arr


def lv_oh_device_id_format_message(device_id):
    # print('lv oh device id mesej')
    e_msg = rps_device_id_format_message(layer_name, device_id, lv_oh_device_id_format_code)
    print(e_msg)
    return e_msg


# **********************************
# ****** Check for Duplicates ******
# **********************************

def lv_oh_duplicate():
    arr = []
    arr = rps_duplicate_device_id(layer_name)

    return arr


def lv_oh_duplicate_message(device_id):
    longitude = 0
    latitude = 0

    midpoint = rps_get_midpoint(layer_name, device_id)
    if midpoint:
        longitude = midpoint.x()
        latitude = midpoint.y()

    e_msg = lv_oh_duplicate_code + ',' + str(device_id) + ',' + layer_name + ': ' + str(
        device_id) + ' duplicated device_id: ' + str(device_id) + ',' + str(longitude) + ',' + str(latitude) + ' \n'
    return e_msg


# **********************************
# ****** Check for Enum Value ******
# **********************************

def lv_oh_field_enum(field_name):
    arr = []
    arr_dropdown = []
    if field_name == 'status':
        arr_dropdown = arr_status
    elif field_name == 'phasing':
        arr_dropdown = arr_phasing
    elif field_name == 'usage':
        arr_dropdown = arr_usage
    elif field_name == 'label':
        arr_dropdown = arr_label_lv_oh
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


def lv_oh_field_enum_message(device_id, field_name):
    longitude = 0
    latitude = 0

    midpoint = rps_get_midpoint(layer_name, device_id)
    if midpoint:
        longitude = midpoint.x()
        latitude = midpoint.y()

    e_msg = lv_oh_enum_valid + ',' + str(device_id) + ',' + layer_name + ': ' + str(
        device_id) + ' Invalid Enumerator at: ' + field_name + ',' + str(longitude) + ',' + str(latitude) + ' \n'
    return e_msg


# **********************************
# ****** Check for Not Null   ******
# **********************************

def lv_oh_field_not_null(field_name):
    arr = rps_field_not_null(layer_name, field_name)
    return arr


def lv_oh_field_not_null_message(device_id, field_name):
    longitude = 0
    latitude = 0

    midpoint = rps_get_midpoint(layer_name, device_id)
    if midpoint:
        longitude = midpoint.x()
        latitude = midpoint.y()

    e_msg = lv_oh_field_null + ',' + str(device_id) + ',' + layer_name + ': ' + str(
        device_id) + ' Mandatory field NOT NULL at: ' + field_name + ',' + str(longitude) + ',' + str(latitude) + ' \n'
    return e_msg


# **********************************
# ********* Check Length  **********
# **********************************

def lv_oh_length_check():
    arr = []
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    query = '"length" < 1.5'
    feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
    for f in feat:
        device_id = f.attribute('device_id')
        arr.append(device_id)
    return arr


def lv_oh_length_check_message(device_id):
    longitude = 0
    latitude = 0

    midpoint = rps_get_midpoint(layer_name, device_id)
    if midpoint:
        longitude = midpoint.x()
        latitude = midpoint.y()

    e_msg = lv_oh_length_check_code + ',' + str(device_id) + ',' + layer_name + ': ' + str(
        device_id) + ' length less than 1.5' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
    return e_msg


# ********************************************************************
# ********* All LV OH Vertex must has Pole nearby  *******************
# ********************************************************************
# ********* Vertex to Pole distance must be 0.9m < x < 1.1m **********
# ********************************************************************
'''
# each vertex of lv oh must have pole nearby (0.9m < x 1.1m)
# i.e not too close, not too far
# Skipped This Checking, according to Manoj
'''


def get_pole_geom():
    arr = []
    layer = QgsProject.instance().mapLayersByName('Pole')[0]
    feat = layer.getFeatures()
    for f in feat:
        geom = f.geometry()
        geom_point = geom.asPoint()
        arr.append(geom_point)
    return arr


def lv_oh_vertex_pole():
    arr = []

    # qgis distanceArea
    distance = QgsDistanceArea()
    distance.setEllipsoid('WGS84')

    arr_pole_geom = get_pole_geom()
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    feat = layer.getFeatures()
    arr_exclude_usage = ['5 FOOT WAYS', 'SERVICE LINE']
    for f in feat:
        device_id = f.attribute('device_id')
        usage = f.attribute('usage')
        geom = f.geometry()
        y = geom.mergeLines()
        total_vertex = len(y.asPolyline())
        if total_vertex > 2 and usage not in arr_exclude_usage:
            arr_vertex = []
            for i in range(total_vertex):
                for pole_geom in arr_pole_geom:
                    vertex = y.asPolyline()[i]
                    m = distance.measureLine(pole_geom, vertex)
                    if m <= 1.1:
                        arr_vertex.append(vertex)
                    # elif m > 1.1 and m < 4:
                    #       print('WARNING: ' + str(device_id) + ': vertex [' + str(i) + ']- distance pole to vertex is ' + str(round(m,3)) + 'm (more than 1.0m!!)')
            if total_vertex != len(arr_vertex):
                print('total vertex:' + str(total_vertex) + ', vertex near pole: ' + str(len(arr_vertex)))
                arr.append(device_id)
    return arr


def lv_oh_vertex_pole_message(device_id):
    longitude = 0
    latitude = 0

    # not included in testing

    e_msg = lv_oh_vertex_pole_code + ',' + str(device_id) + ',' + layer_name + ': ' + str(
        device_id) + ' has vertex not near a pole ' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
    return e_msg


# ***************************************************
# ********* Check self Intersect  *******************
# ***************************************************
'''
# Step 1: convert geom to polyline
# Step 2: extract all vectors
# Step 3: create lines using vector[i] and vector[i+1]
# Step 4: check each line against all other lines (loop)
# Step 5: count intersection
# Step 6: if intersection >= 3, means self intersect
'''


def lv_oh_self_intersect(arr_lv_oh_exclude_geom):
    arr = []
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    feat = layer.getFeatures()

    for f in feat:
        device_id = f.attribute('device_id')
        if device_id not in arr_lv_oh_exclude_geom:
            geom = f.geometry()
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

            # print(str(len(poly_line_y)) + ' vector(s) found, with ' + str(len(arr_line)) + ' total lines')
            for h in range(len(arr_line)):
                arr_temp = []
                arr_temp.extend(arr_line)
                if arr_line[h] in arr_temp:
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

    return arr


def lv_oh_self_intersect_message(arr_lv_oh_exclude_geom, device_id):
    longitude = 0
    latitude = 0

    geom = rps_get_midpoint(layer_name, device_id)
    if geom:
        longitude = geom.x()
        latitude = geom.y()

    e_msg = lv_oh_self_intersect_code + ',' + str(device_id) + ',' + layer_name + ': ' + str(
        device_id) + ' has self intersect geometry ' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
    return e_msg


# *******************************
# ****** Hanging Geometry  ******
# *******************************

'''
# Get vertex[0] and vertex[last] from LV OH Conductor
# List down all possible vertext that these two might connect to:
# - all other vectors in LV OH
# - vector[0] and vector[last] in LV UG
# - Demand Point
# - LV Cable Joint
# check if the vertex[0] is connected to any of those above.
# check if the vertex[last] is connected to any of those above.
# if not connected to anything, return error
'''


def lv_oh_hanging(arr_lv_ug_exclude_geom, arr_lv_oh_exclude_geom):
    arr = []
    # qgis distanceArea
    distance = QgsDistanceArea()
    distance.setEllipsoid('WGS84')

    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    # query = '"device_id" = \'' + 'R6142ugc017' + '\''
    # feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
    feat_count = layer.featureCount()
    # print(feat_count)

    # skip check if feat count is too many
    if feat_count > lv_oh_max_count:
        print('too many objects: skipped checking for LV OH hanging')
    else:
        feat = layer.getFeatures()
        for f in feat:
            device_id = f.attribute('device_id')
            if device_id not in arr_lv_oh_exclude_geom:
                geom = f.geometry()
                y = geom.mergeLines()
                polyline_y = y.asPolyline()
                v_one = polyline_y[0]
                v_last = polyline_y[len(polyline_y) - 1]
                # print('len polyline is ', len(polyline_y))
                # print(v_one)

                # get other vertex of LV OH
                arr_point = []
                arr_device_id = []
                layer_lv_oh = QgsProject.instance().mapLayersByName(layer_name)[0]
                query = '"device_id" != \'' + str(device_id) + '\''
                feat_lv_oh = layer_lv_oh.getFeatures(QgsFeatureRequest().setFilterExpression(query))
                for g in feat_lv_oh:
                    device_temp = g.attribute('device_id')
                    if device_temp not in arr_lv_oh_exclude_geom:
                        arr_device_id.append(device_temp)
                        geom_g = g.geometry()
                        y_g = geom_g.mergeLines()
                        polyline_y_g = y_g.asPolyline()
                        for g1 in range(len(polyline_y_g)):
                            if polyline_y_g[g1] not in arr_point:
                                arr_point.append(polyline_y_g[g1])
                                # print(arr_device_id)
                # print(arr_point)

                # get lv ug vector: (1st point and last point is enough)
                layer_lv_ug = QgsProject.instance().mapLayersByName('LV_UG_Conductor')[0]
                feat_lv_ug = layer_lv_ug.getFeatures()
                for h in feat_lv_ug:
                    device_temp = h.attribute('device_id')
                    if device_temp not in arr_lv_ug_exclude_geom:
                        geom_h = h.geometry()
                        if geom_h:
                            y_h = geom_h.mergeLines()
                            polyline_y = y_h.asPolyline()
                            v1_one = polyline_y[0]
                            v1_last = polyline_y[len(polyline_y) - 1]
                            arr_point.append(v1_one)
                            arr_point.append(v1_last)

                # get demand point point
                layer_dmd_pt = QgsProject.instance().mapLayersByName('Demand_Point')[0]
                feat_dmd_pt = layer_dmd_pt.getFeatures()
                for j in feat_dmd_pt:
                    devide_temp = j.attribute('device_id')
                    geom_j = j.geometry()
                    if geom_j:
                        j_point = geom_j.asPoint()
                        arr_point.append(j_point)

                # get LV Cable Joint
                layer_lv_cj = QgsProject.instance().mapLayersByName('LV_Cable_Joint')[0]
                feat_lv_cj = layer_lv_cj.getFeatures()
                for j in feat_lv_cj:
                    devide_temp = j.attribute('device_id')
                    geom_j = j.geometry()
                    if geom_j:
                        j_point = geom_j.asPoint()
                        arr_point.append(j_point)

                # print('arr point is:' + str(len(arr_point)))

                # check distance between v_one / v_last with arr_point
                arr_snap_v_one = []
                arr_snap_v_last = []
                for v_point in arr_point:
                    distance_v_one = distance.measureLine(v_one, v_point)
                    if distance_v_one <= 0.001:
                        # print(j)
                        # print('distance is ' + format(distance_xy,'.9f') + 'm')
                        arr_snap_v_one.append(device_id)
                    # print('v point to check:' + str(v_point))
                    distance_v_last = distance.measureLine(v_last, v_point)
                    if distance_v_last <= 0.001:
                        # print('v last is ' + str(v_last))
                        # print('lv point is ' + str(v_point))
                        # print('distance is ' + format(distance_v_last,'.9f') + 'm')
                        arr_snap_v_last.append(device_id)
                        # print(device_id + ': total arr_snap_v_one ' + str(len(arr_snap_v_one)))
                if len(arr_snap_v_one) == 0 or len(arr_snap_v_last) == 0 and device_id not in arr:
                    arr.append(device_id)
    return arr


def lv_oh_hanging_message(device_id):
    longitude = 0
    latitude = 0

    geom = rps_get_lastpoint(layer_name, device_id)
    if geom:
        longitude = geom.x()
        latitude = geom.y()

    e_msg = lv_oh_hanging_code + ',' + str(device_id) + ',' + layer_name + ': ' + str(
        device_id) + ' is hanging ' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
    return e_msg


# **************************************
# ********* Check Buffer 0.3  **********
# **************************************

# get all the vectors inside LV OH except Vector 0 and Vector last
def get_all_lv_oh_vector_between(arr_lv_oh_exclude_geom):
    arr_lv_oh = []
    # get vectors of all LV OH (for comparison)
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    feat = layer.getFeatures()
    for f in feat:
        device_id = f.attribute('device_id')
        if device_id not in arr_lv_oh_exclude_geom:
            geom = f.geometry()
            y = geom.mergeLines()
            polyline_y = y.asPolyline()
            # if only have 2 vectors, do not add any vectors
            if len(polyline_y) > 2:
                for i in range(len(polyline_y)):
                    # remove first and last
                    if 0 < i < len(polyline_y) - 1:
                        arr_lv_oh.append(polyline_y[i])

    return arr_lv_oh


def lv_oh_buffer(arr_lv_oh_exclude_geom):
    arr = []
    arr_lv_oh = []

    # qgis distanceArea
    distance = QgsDistanceArea()
    distance.setEllipsoid('WGS84')

    # get vectors of all LV OH (for comparison)
    arr_lv_oh = get_all_lv_oh_vector_between(arr_lv_oh_exclude_geom)

    # main function
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    feat = layer.getFeatures()
    for f in feat:
        # reset array values
        arr_temp = []
        arr_temp.extend(arr_lv_oh)
        arr_cur_lv_oh = []

        # get arr_cur_lv_oh (list of vectors to in one deviceid)
        device_id = f.attribute('device_id')
        if device_id not in arr_lv_oh_exclude_geom:
            geom = f.geometry()
            y = geom.mergeLines()
            polyline_y = y.asPolyline()
            for geom_y in polyline_y:
                arr_cur_lv_oh.append(geom_y)

            # remove own vector from arr_temp
            for cur_lv_oh in arr_cur_lv_oh:
                if cur_lv_oh in arr_temp:
                    arr_temp.remove(cur_lv_oh)

            arr_too_close = []
            arr_too_far = []

            for i in range(len(arr_cur_lv_oh)):
                # remove first and last vertex from checking
                if 0 < i < len(arr_cur_lv_oh) - 1:
                    for vector_all in arr_temp:
                        vector = arr_cur_lv_oh[i]
                        m = distance.measureLine(vector, vector_all)
                        if 0.29 > m > 0.005:
                            # print(device_id + '[' + str(i + 1) + '/' + str(len(arr_cur_lv_oh)) + ']' + ' is too close to another conductor!')
                            arr_too_close.append(device_id)
                        elif 0.31 < m < 0.5:
                            # print(device_id + ' is too far from another conductor')
                            arr_too_far.append(device_id)
            if len(arr_too_close) > 0:
                arr.append(device_id)

    return arr


def lv_oh_buffer_message(device_id, arr_lv_oh_exclude_geom):
    longitude = 0
    latitude = 0
    # qgis distanceArea
    distance = QgsDistanceArea()
    distance.setEllipsoid('WGS84')

    arr_lv_oh = []
    # get vectors of all LV OH (for comparison)
    arr_lv_oh = get_all_lv_oh_vector_between(arr_lv_oh_exclude_geom)

    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    query = '"device_id" = \'' + str(device_id) + '\''
    feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))

    for f in feat:
        # reset array values
        arr_temp = []
        arr_temp.extend(arr_lv_oh)
        arr_cur_lv_oh = []

        # get arr_cur_lv_oh (list of vectors to in one device id)
        device_id = f.attribute('device_id')
        geom = f.geometry()
        y = geom.mergeLines()
        polyline_y = y.asPolyline()
        for geom_y in polyline_y:
            arr_cur_lv_oh.append(geom_y)

        # remove own vector from arr_temp
        for cur_lv_oh in arr_cur_lv_oh:
            if cur_lv_oh in arr_temp:
                arr_temp.remove(cur_lv_oh)

        arr_too_close = []
        arr_too_far = []

        for i in range(len(arr_cur_lv_oh)):
            # remove first and last vertex from checking
            if 0 < i < len(arr_cur_lv_oh) - 1:
                for vector_all in arr_temp:
                    vector = arr_cur_lv_oh[i]
                    m = distance.measureLine(vector, vector_all)
                    if 0.29 > m > 0.005:
                        # print(device_id + '[' + str(i + 1) + '/' + str(len(arr_cur_lv_oh)) + ']' + ' is too close to another conductor!')
                        arr_too_close.append(i)
                    elif 0.31 < m < 0.5:
                        # print(device_id + ' is too far from another conductor')
                        arr_too_far.append(i)

        if len(arr_too_close) > 0:
            # get vector geometry
            vector_no = arr_too_close[0]
            qgs_point_0 = arr_cur_lv_oh[vector_no]
            # pass longitude/latitude
            longitude = qgs_point_0.x()
            latitude = qgs_point_0.y()
            # print('device id: ' + str(device_id) + ' ' + str(qgs_point_0))

    e_msg = lv_oh_buffer_code + ',' + str(device_id) + ',' + layer_name + ': ' + str(
        device_id) + ' is too close to another conductor! (distance < 0.3m) ' + ',' + str(longitude) + ',' + str(
        latitude) + ' \n'
    return e_msg

# ***********************************************
# ******* Check for Wrong flow direction  *******
# ***********************************************

def get_all_lv_oh_vector_outgoing(arr_lv_oh_exclude_geom, device_id_exclude):
    arr_lv_oh = []
    # get vectors of all LV OH (for comparison)
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    feat = layer.getFeatures()
    for f in feat:
        device_id = f.attribute('device_id')
        if device_id not in arr_lv_oh_exclude_geom and device_id != device_id_exclude:
            geom = f.geometry()
            if geom:
                y = geom.mergeLines()
                polyline_y = y.asPolyline()
                # if only have 2 vectors, do not add any vectors
                if len(polyline_y) > 0:
                    # add vector 0 (outgoing vector)
                   arr_lv_oh.append(polyline_y[0])

    return arr_lv_oh

def get_all_lv_oh_vector_incoming(arr_lv_oh_exclude_geom, device_id_exclude):
    arr_lv_oh = []
    # get vectors of all LV OH (for comparison)
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    feat = layer.getFeatures()
    for f in feat:
        device_id = f.attribute('device_id')
        if device_id not in arr_lv_oh_exclude_geom and device_id != device_id_exclude:
            geom = f.geometry()
            if geom:
                y = geom.mergeLines()
                polyline_y = y.asPolyline()
                # if only have 2 vectors, do not add any vectors
                if len(polyline_y) > 0:
                    # add vector last (incoming vector)
                    total_vector = len(polyline_y)
                    arr_lv_oh.append(polyline_y[total_vector - 1])

    return arr_lv_oh

def lv_oh_wrong_flow(arr_lv_oh_exclude_geom):
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
        if device_id not in arr_lv_oh_exclude_geom:
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
                    arr_lv_oh_incoming = get_all_lv_oh_vector_incoming(arr_lv_oh_exclude_geom, device_id)
                    count = arr_lv_oh_incoming.count(vector_last)
                    if count > 1:
                        # check if there is any outgoing
                        total_outgoing = 0
                        arr_lv_oh_outgoing = get_all_lv_oh_vector_outgoing(arr_lv_oh_exclude_geom, device_id)
                        for geom_lv_oh in arr_lv_oh_outgoing:
                            m = distance.measureLine(vector_last, geom_lv_oh)
                            if m < 0.001:
                                total_outgoing += 1
                                print(device_id + ' has 2 incoming but ' + total_outgoing + ' outgoing geom.')
                        if total_outgoing == 0:
                            print(device_id + ' has no outgoing! ')
                            arr.append(device_id)

    # add demand point wrong flow error
    print('before adding demand point wrong flow error is ' + str(len(arr)))
    arr.extend(lv_oh_wrong_flow_dmd_pt(arr_lv_oh_exclude_geom))
    print('total wrong flow error is ' + str(len(arr)))

    return arr

def get_all_dmd_pt():
    arr_dmd_pt = []
    layer = QgsProject.instance().mapLayersByName('Demand_Point')[0]
    feat = layer.getFeatures()
    # temporary: for testing
    # device_id_test = 'RPS6122ohc364'
    # query = '"device_id" = \'' + str(device_id_test) + '\''
    # feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
    for f in feat:
        # get demand point vectors
        geom = f.geometry()
        if geom:
            geom_point = geom.asPoint()
            arr_dmd_pt.append(geom_point)

    return arr_dmd_pt

def lv_oh_wrong_flow_dmd_pt(arr_lv_oh_exclude_geom):
    # Special condition: all conductors connected to demand point MUST be INCOMING.
    arr = []

    arr_dmd_pt = get_all_dmd_pt()

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
        if device_id not in arr_lv_oh_exclude_geom:
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
                            # means it is outgoing lv_oh, so we add lv oh's device id
                            arr.append(device_id)

    return arr

def lv_oh_wrong_flow_message(device_id):
    longitude = 0
    latitude = 0
    error_code = lv_oh_wrong_flow_code
    error_desc = str(device_id) + ' has wrong flow direction! '

    midpoint = rps_get_firstpoint(layer_name, device_id)
    if midpoint:
        longitude = midpoint.x()
        latitude = midpoint.y()

    e_msg = rps_write_line(error_code, device_id, layer_name, error_desc, longitude, latitude)
    return e_msg


# **********************************
# ******* End of Validation  *******
# **********************************
