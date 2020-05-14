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
lv_ug_field_null = 'ERR_LVUGCOND_01'
lv_ug_enum_valid = 'ERR_LVUGCOND_02'
lv_ug_lv_db_in_out_geom = 'ERR_LVUGCOND_04'
lv_ug_lvdb_in_out_col = 'ERR_LVUGCOND_03'
lv_ug_length = 'ERR_LVUGCOND_05'
lv_ug_duplicate_code = 'ERR_DUPLICATEID'
lv_ug_device_id_format_code = 'ERR_DEVICE_ID'
lv_ug_coin_code = 'ERR_LVUGCOND_06'
lv_ug_z_m_shapefile_code = 'ERR_Z_M_VALUE'
lv_ug_self_intersect_code = 'ERR_LVUGCOND_10'
lv_ug_1_2_incoming_code = 'ERR_LVUGCOND_08'
lv_ug_1_2_outgoing_code = 'ERR_LVUGCOND_08'
lv_ug_hanging_code = 'ERR_LVUGCOND_07'
lv_ug_buffer_code = 'ERR_LVUGCOND_09'

# *****************************************
# ****** Check Z-M Value in shapefile *****
# *****************************************

def lv_ug_z_m_shapefile():
        arr = []
        arr = rps_z_m_shapefile(layer_name)
        return arr

def lv_ug_z_m_shapefile_message(geom_name):
        longitude = 0
        latitude = 0
        
        e_msg = lv_ug_z_m_shapefile_code + ',' + layer_name + ',' + 'Z M Value for ' + layer_name + ' is ' + geom_name + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg
        

# ****************************************
# ****** Check for Device_Id Format ******
# ****************************************

def lv_ug_device_id_format():
        arr = []
        arr = rps_device_id_format(layer_name)
        return arr

def lv_ug_device_id_format_message(device_id):
        longitude = 0
        latitude = 0

        midpoint = rps_get_midpoint(layer_name, device_id)
        if midpoint:
                longitude = midpoint.x()
                latitude = midpoint.y()
        
        e_msg = lv_ug_device_id_format_code + ',' + device_id + ',' + layer_name + ': ' + device_id + ' device_id format error' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
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
        
        e_msg = lv_ug_duplicate_code +',' + device_id + ',' + 'LV_UG_Conductor: ' + device_id + ' duplicated device_id: ' + device_id + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg



# **********************************
# ****** Check for Enum Value ******
# **********************************

def lv_ug_field_enum(field_name):
        arr = []
        arr_dropdown = []
        if field_name == 'status':
                arr_dropdown = arr_status
        elif field_name == 'phasing':
                arr_dropdown = arr_phasing
        elif field_name == 'usage':
                arr_dropdown = arr_usage
        elif field_name == 'label':
                arr_dropdown = arr_label_lv_ug
        elif field_name == 'dat_qty_cl':
                arr_dropdown = arr_dat_qty_cl
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

def lv_ug_field_enum_message(device_id, field_name):
        longitude = 0
        latitude = 0

        midpoint = rps_get_midpoint(layer_name, device_id)
        if midpoint:
                longitude = midpoint.x()
                latitude = midpoint.y()
        
        e_msg = lv_ug_enum_valid +',' + device_id + ',' + 'LV_UG_Conductor: ' + device_id + ' Invalid Enumerator at: ' + field_name + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg

# **********************************
# ****** Check for Not Null   ******
# **********************************

def lv_ug_field_not_null(field_name):
	arr = []
	layer = QgsProject.instance().mapLayersByName(layer_name)[0]
	query = '"' + field_name + '" is null OR ' + '"' + field_name + '" =  \'N/A\''
	feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
	for f in feat:
		device_id = f.attribute('device_id')
		arr.append(device_id)
	return arr

def lv_ug_field_not_null_message(device_id, field_name):
        longitude = 0
        latitude = 0

        midpoint = rps_get_midpoint(layer_name, device_id)
        if midpoint:
                longitude = midpoint.x()
                latitude = midpoint.y()
        
        e_msg = lv_ug_field_null +',' + device_id + ',' + 'LV_UG_Conductor: ' + device_id + ' Mandatory field NOT NULL at: ' + field_name + ',' + str(longitude) + ',' + str(latitude) + ' \n'
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
def lv_ug_lv_db_in():
	
    arr = []
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    feat = layer.getFeatures()
    for f in feat:
        device_id = f.attribute('device_id')
        lv_db_device_id = f.attribute('in_lvdb_id')
        g_line = f.geometry()
        y = g_line.mergeLines()
        if lv_db_device_id:
            layer_lv_db = QgsProject.instance().mapLayersByName('LVDB-FP')[0]
            query = '"device_id" = \'' + lv_db_device_id + '\''
            feat_lv_db = layer_lv_db.getFeatures(QgsFeatureRequest().setFilterExpression(query))
            for lv_db in feat_lv_db:
                geom = lv_db.geometry()
                geom_x = geom.asPoint()
                distance = QgsDistanceArea()
                distance.setEllipsoid('WGS84')
                distance_xy = distance.measureLine(y.asPolyline()[len(y.asPolyline())-1],geom_x)
                if distance_xy > 0.001:
                    print("WARNING: incoming distance > 0")
                    print("Point1 (LVUG):", y.asPolyline()[len(y.asPolyline())-1])
                    print("Point2 (LVDB):", geom_x)
                    print("difference:", format(distance_xy,'.9f'))
                    arr.append(device_id)
    return arr

def lv_ug_lv_db_in_message(device_id):
        longitude = 0
        latitude = 0

        last_point = rps_get_lastpoint(layer_name, device_id)
        if last_point:
                longitude = last_point.x()
                latitude = last_point.y()

        e_msg = lv_ug_lv_db_in_out_geom + ',' + device_id + ',' + 'LV_UG_Conductor: ' + device_id + ' column in_lvdb_id mismtach ' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg

def lv_ug_lv_db_out():
        arr = []
        distance = QgsDistanceArea()
        distance.setEllipsoid('WGS84')
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        feat = layer.getFeatures()
        for f in feat:
                device_id = f.attribute('device_id')
                g_line = f.geometry()
                y = g_line.mergeLines()
                out_lvdb_id = f.attribute('out_lvdb_i')

                if out_lvdb_id:
                        layer_lvdb = QgsProject.instance().mapLayersByName('LVDB-FP')[0]
                        query = '"device_id" = \'' + out_lvdb_id + '\''
                        feat_lvdb = layer_lvdb.getFeatures(QgsFeatureRequest().setFilterExpression(query))
                        for lvdb in feat_lvdb:
                                geom = lvdb.geometry()
                                geom_x = geom.asPoint()
                                distance_xy = distance.measureLine(y.asPolyline()[0], geom_x)
                                if distance_xy > 0.001:
                                        print("WARNING: outgoing distance > 0:")
                                        print("Point1 (LVUG):",y.asPolyline()[0])
                                        print("Point2 (LVDB):",geom_x)
                                        print("difference:", format(distance_xy, '.9f'))
                                        arr.append(device_id)
        return arr

def lvug_lvdb_out_message(device_id):
        longitude = 0
        latitude = 0

        first_point = rps_get_firstpoint(layer_name, device_id)
        if first_point:
                longitude = first_point.x()
                latitude = first_point.y()

        e_msg = lv_ug_lv_db_in_out_geom + ',' + device_id + ',' + 'LV_UG_Conductor: ' + device_id + ' column out_lvdb_id mismatch' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg

# ************************************
# ****** Check for LVDB in/out  ******
# ************************************

def lv_ug_lvdb_id_in_check():
    arr = []
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    query = '"in_lvdb_id" is not null OR "out_lvdb_i" is not null'
    feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
    for f in feat:
        device_id = f.attribute('device_id')
        in_lvdb_id = f.attribute('in_lvdb_id')
        lvdb_in_no = f.attribute('lvdb_in_no')
        out_lvdb_i = f.attribute('out_lvdb_i')
        lvdb_out_no = f.attribute('lvdb_ot_no')
        if in_lvdb_id:
            if lvdb_in_no is None:
                arr.append(device_id)
    return arr

def lv_ug_lvdb_id_out_check():
    arr = []
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    query = '"in_lvdb_id" is not null OR "out_lvdb_i" is not null'
    feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
    for f in feat:
        device_id = f.attribute('device_id')
        in_lvdb_id = f.attribute('in_lvdb_id')
        lvdb_in_no = f.attribute('lvdb_in_no')
        out_lvdb_i = f.attribute('out_lvdb_i')
        lvdb_out_no = f.attribute('lvdb_ot_no')
        if out_lvdb_i:
            if lvdb_out_no is None:
                arr.append(device_id)
    return arr

def lv_ug_lvdb_no_in_check():
    arr = []
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    query = '"lvdb_in_no" is not null OR "lvdb_ot_no" is not null'
    feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
    for f in feat:
        device_id = f.attribute('device_id')
        in_lvdb_id = f.attribute('in_lvdb_id')
        lvdb_in_no = f.attribute('lvdb_in_no')
        out_lvdb_i = f.attribute('out_lvdb_i')
        lvdb_out_no = f.attribute('lvdb_ot_no')
        if lvdb_in_no is None:
            if in_lvdb_id:
                arr.append(device_id)
    return arr

def lv_ug_lvdb_no_out_check():
    arr = []
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    query = '"lvdb_in_no" is not null OR "lvdb_ot_no" is not null'
    feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
    for f in feat:
        device_id = f.attribute('device_id')
        in_lvdb_id = f.attribute('in_lvdb_id')
        lvdb_in_no = f.attribute('lvdb_in_no')
        out_lvdb_i = f.attribute('out_lvdb_i')
        lvdb_out_no = f.attribute('lvdb_ot_no')
        if lvdb_out_no is None:
            if out_lvdb_i:
                arr.append(device_id)
    return arr

def lv_ug_lvdb_id_check_message(device_id):
        longitude = 0
        latitude = 0

        midpoint = rps_get_midpoint(layer_name, device_id)
        if midpoint:
                longitude = midpoint.x()
                latitude = midpoint.y()

        e_msg = lv_ug_lvdb_in_out_col + ',' + device_id + ',' + 'LV_UG_Conductor: ' + device_id + ' lvdb_in_no/lvdb_ot_no MISSING' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg

def lv_ug_lvdb_no_check_message(device_id):
        longitude = 0
        latitude = 0

        midpoint = rps_get_midpoint(layer_name, device_id)
        if midpoint:
                longitude = midpoint.x()
                latitude = midpoint.y()

        e_msg = lv_ug_lvdb_in_out_col + ',' + device_id + ',' + 'LV_UG_Conductor: ' + device_id + ' lvdb_in_id/lvdb_out_i MISSING' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
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

        e_msg = lv_ug_length + ',' + device_id + ',' + layer_name + ': ' + device_id + ' length less than 1.5' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
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
        query = '"device_id" = \'' + device_id + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
        for f in feat:
                device_id = f.attribute('device_id')
                geom = f.geometry()
        return geom

def lv_ug_1_2_incoming():
        arr = []
        # qgis distanceArea
        distance = QgsDistanceArea()
        distance.setEllipsoid('WGS84')
        
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        feat = layer.getFeatures()        
        for f in feat:
                device_id = f.attribute('device_id')
                # get geometry of LV UG
                geom = f.geometry()
                y = geom.mergeLines()
                polyline_y = y.asPolyline()
                # get incoming and outgoing distance
                # distance_0 = distance.measureLine(polyline_y[0],polyline_y[1])
                distance_n = distance.measureLine(polyline_y[len(polyline_y) - 1],polyline_y[len(polyline_y) - 2])                
                # get incoming/outgoing lvdb, if any
                in_lv_db_device_id = f.attribute('in_lvdb_id')
                out_lv_db_device_id = f.attribute('out_lvdb_i')
                if in_lv_db_device_id:
                        geom_lvdb = get_lvdb_by_device_id(in_lv_db_device_id)                        
                        if distance_n < 1:
                                # print(device_id + '/' + in_lv_db_device_id + ' incoming dist is ' + str(distance_n))
                                arr.append(device_id)
        return arr

def lv_ug_1_2_incoming_message(device_id):
        longitude = 0
        latitude = 0

        lastpoint = rps_get_lastpoint(layer_name, device_id)
        if lastpoint:
                longitude = lastpoint.x()
                latitude = lastpoint.y()        

        e_msg = lv_ug_1_2_incoming_code + ',' + device_id + ',' + layer_name + ': ' + device_id + ' INCOMING vertex to LVDB must be more than 1.0m' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg

def lv_ug_1_2_outgoing():
        arr = []
        # qgis distanceArea
        distance = QgsDistanceArea()
        distance.setEllipsoid('WGS84')
        
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        feat = layer.getFeatures()        
        for f in feat:
                device_id = f.attribute('device_id')
                # get geometry of LV UG
                geom = f.geometry()
                y = geom.mergeLines()
                polyline_y = y.asPolyline()
                # get incoming and outgoing distance
                distance_0 = distance.measureLine(polyline_y[0],polyline_y[1])
                # distance_n = distance.measureLine(polyline_y[len(polyline_y) - 1],polyline_y[len(polyline_y) - 2])                
                # get incoming/outgoing lvdb, if any
                in_lv_db_device_id = f.attribute('in_lvdb_id')
                out_lv_db_device_id = f.attribute('out_lvdb_i')
                if out_lv_db_device_id:
                        geom_lvdb = get_lvdb_by_device_id(out_lv_db_device_id)                        
                        if distance_0 < 1:
                                # print(device_id + '/' + out_lv_db_device_id + ' outgoing distance is ' + str(distance_0))
                                arr.append(device_id)
        return arr

def lv_ug_1_2_outgoing_message(device_id):
        longitude = 0
        latitude = 0

        second_point = rps_get_secondpoint(layer_name, device_id)
        if second_point:
                longitude = second_point.x()
                latitude = second_point.y()         
        
        e_msg = lv_ug_1_2_outgoing_code + ',' + device_id + ',' + layer_name + ': ' + device_id + ' OUTGOING vertex from LVDB-FP must be more than 1.0m' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
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
def lv_ug_self_intersect():
        arr = []
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        # query = '"device_id" = \'' + 'R6142ugc031' + '\''
        # feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
        feat = layer.getFeatures()

        for f in feat:
                device_id = f.attribute('device_id')
                geom = f.geometry()
                y = geom.mergeLines()
                polyLine_y = y.asPolyline()

                arr_line = []
                for i in range(len(polyLine_y)):
                        geom_i = polyLine_y[i]
                        if i < len(polyLine_y) - 1:
                                geom_i2 = polyLine_y[i+1]
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
                        
        return arr

'''
# copy from function above
'''
def lv_ug_self_intersect_message(device_id):
        longitude = 0
        latitude = 0
        arr_self_intersect = []

        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + device_id + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))

        for f in feat:
                geom = f.geometry()
                y = geom.mergeLines()
                polyLine_y = y.asPolyline()

                arr_line = []
                for i in range(len(polyLine_y)):
                        geom_i = polyLine_y[i]
                        if i < len(polyLine_y) - 1:
                                geom_i2 = polyLine_y[i+1]
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
                        arr_points = []
                        for i in range(len(arr_temp)):
                                intersect = QgsGeometry.intersection(arr_line[h], arr_temp[i])
                                if intersect:
                                        if intersect.asPoint() not in arr_points:
                                                # print('different point found!' + str(intersect.asPoint()))
                                                arr_points.append(intersect.asPoint())
                                        polyline_h = arr_line[h].asPolyline()
                                        for i in polyline_h:
                                                if i in arr_points:
                                                        arr_points.remove(i)
                                        no_of_intersect += 1
                        # print('intersect: ' + str(no_of_intersect))
                        # remove duplicate device_id
                        if no_of_intersect > 2 and arr_points[0] not in arr_self_intersect:
                                # print(arr_points)
                                # take last intersect point
                                arr_self_intersect.append(arr_points[0])
                        if(len(arr_self_intersect) > 0):
                                qgs_point_0 = arr_self_intersect[0]
                                # pass longitude/latitude
                                longitude = qgs_point_0.x()
                                latitude = qgs_point_0.y()
                                # print('device id: ' + device_id + ' ' + str(qgs_point_0))                
                        
        
        e_msg = lv_ug_self_intersect_code + ',' + device_id + ',' + layer_name + ': ' + device_id + ' has self intersect geometry ' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
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

def lv_ug_hanging():
        arr = []
        # qgis distanceArea
        distance = QgsDistanceArea()
        distance.setEllipsoid('WGS84')
        
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        # query = '"device_id" = \'' + 'R6142ugc017' + '\''
        # feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
        feat = layer.getFeatures()
        for f in feat:
                device_id = f.attribute('device_id')
                geom = f.geometry()
                y = geom.mergeLines()
                polyline_y = y.asPolyline()
                v_one = polyline_y[0]
                v_last = polyline_y[len(polyline_y) - 1]
                # print('len polyline is ', len(polyline_y))

                # print(v_one)

                # get other vertex
                arr_point = []
                arr_device_id = []
                layer_lv_ug = QgsProject.instance().mapLayersByName(layer_name)[0]
                query = '"device_id" != \'' + device_id + '\''
                feat_lv_ug = layer_lv_ug.getFeatures(QgsFeatureRequest().setFilterExpression(query))
                for g in feat_lv_ug:
                        device_temp = g.attribute('device_id')
                        arr_device_id.append(device_temp)
                        geom_g = g.geometry()
                        y_g = geom_g.mergeLines()
                        polyline_y_g = y_g.asPolyline()
                        for g1 in range(len(polyline_y_g)):
                                if polyline_y_g[g1] not in arr_point:
                                        arr_point.append(polyline_y_g[g1])                                
                # print(arr_device_id)
                # print(arr_point)

                layer_lv_oh = QgsProject.instance().mapLayersByName('LV_OH_Conductor')[0]
                feat_lv_oh = layer_lv_oh.getFeatures()
                for h in feat_lv_oh:
                        device_temp = g.attribute('device_id')
                        geom_h = h.geometry()
                        y_h = geom_h.mergeLines()
                        polyline_y = y_h.asPolyline()
                        v1_one = polyline_y[0]
                        v1_last = polyline_y[len(polyline_y) - 1]
                        arr_point.append(v1_one)
                        arr_point.append(v1_last)

                layer_dmd_pt = QgsProject.instance().mapLayersByName('Demand_Point')[0]
                feat_dmd_pt = layer_dmd_pt.getFeatures()
                for j in feat_dmd_pt:
                        devide_temp = j.attribute('device_id')
                        geom_j = j.geometry()
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
                if len(arr_snap_v_one) == 0 or len(arr_snap_v_last) == 0:
                        arr.append(device_id)
        return arr

'''
# copy from function above, but only do to one device id
'''

def lv_ug_hanging_message(device_id):
        longitude = 0
        latitude = 0

        # qgis distanceArea
        distance = QgsDistanceArea()
        distance.setEllipsoid('WGS84')

        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + device_id + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))

        for f in feat:
                device_id = f.attribute('device_id')
                geom = f.geometry()
                y = geom.mergeLines()
                polyline_y = y.asPolyline()
                v_one = polyline_y[0]
                v_last = polyline_y[len(polyline_y) - 1]
                # print('len polyline is ', len(polyline_y))

                # print(v_one)

                # get other vertex
                arr_point = []
                arr_device_id = []
                layer_lv_ug = QgsProject.instance().mapLayersByName(layer_name)[0]
                query = '"device_id" != \'' + device_id + '\''
                feat_lv_ug = layer_lv_ug.getFeatures(QgsFeatureRequest().setFilterExpression(query))
                for g in feat_lv_ug:
                        device_temp = g.attribute('device_id')
                        arr_device_id.append(device_temp)
                        geom_g = g.geometry()
                        y_g = geom_g.mergeLines()
                        polyline_y_g = y_g.asPolyline()
                        for g1 in range(len(polyline_y_g)):
                                if polyline_y_g[g1] not in arr_point:
                                        arr_point.append(polyline_y_g[g1])                                
                # print(arr_device_id)
                # print(arr_point)

                layer_lv_oh = QgsProject.instance().mapLayersByName('LV_OH_Conductor')[0]
                feat_lv_oh = layer_lv_oh.getFeatures()
                for h in feat_lv_oh:
                        device_temp = g.attribute('device_id')
                        geom_h = h.geometry()
                        y_h = geom_h.mergeLines()
                        polyline_y = y_h.asPolyline()
                        v1_one = polyline_y[0]
                        v1_last = polyline_y[len(polyline_y) - 1]
                        arr_point.append(v1_one)
                        arr_point.append(v1_last)

                layer_dmd_pt = QgsProject.instance().mapLayersByName('Demand_Point')[0]
                feat_dmd_pt = layer_dmd_pt.getFeatures()
                for j in feat_dmd_pt:
                        devide_temp = j.attribute('device_id')
                        geom_j = j.geometry()
                        j_point = geom_j.asPoint()
                        arr_point.append(j_point)
                       
                                        
                # print('arr point is:' + str(len(arr_point)))

                # check distance between v_one / v_last with arr_point
                arr_snap_v_one = []
                arr_snap_v_last = []
                error_vector = []
                
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
                if len(arr_snap_v_one) == 0:
                        longitude = v_one.x()
                        latitude = v_one.y()                        
                elif len(arr_snap_v_last) == 0:
                        longitude = v_last.x()
                        latitude = v_last.y()
                        
        e_msg = lv_ug_hanging_code + ',' + device_id + ',' + layer_name + ': ' + device_id + ' is hanging ' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg
        

# ********************************************
# ****** Check for Coincidence Geometry ******
# * (same with buffer)
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

                #create another loop
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
        
        e_msg = lv_ug_coin_code + ',' + device_id + ',' + layer_name + ': ' + device_id + ' has coincidence geometry ' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg

# *************************************************
# ****** Buffer between LV UG must be > 0.3  ******
# *************************************************

# get all vertex of a LV UG conductor
# check distance between this vertex and other vertex of another conductor

'''
# buat last
'''

def get_all_lv_ug_vector():
        arr_lv_ug = []
        # get vectors of all LV UG (for comparison)
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        feat =  layer.getFeatures()
        for f in feat:
                geom = f.geometry()
                y = geom.mergeLines()
                polyline_y = y.asPolyline()
                for geom_y in polyline_y:
                        arr_lv_ug.append(geom_y)
        
        return arr_lv_ug

def lv_ug_buffer():
        arr = []
        arr_lv_ug = []

        # qgis distanceArea
        distance = QgsDistanceArea()
        distance.setEllipsoid('WGS84')

        arr_lv_ug = get_all_lv_ug_vector()

        # main function
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        feat =  layer.getFeatures()
        for f in feat:
                # reset array values
                arr_temp = []
                arr_temp.extend(arr_lv_ug)
                arr_cur_lv_ug = []

                # get arr_cur_lv_ug (list of vectors to in one deviceid)
                device_id = f.attribute('device_id')
                geom = f.geometry()
                y = geom.mergeLines()
                polyline_y = y.asPolyline()
                for geom_y in polyline_y:
                        arr_cur_lv_ug.append(geom_y)

                #remove own vector from arr_temp
                for cur_lv_ug in arr_cur_lv_ug:
                        arr_temp.remove(cur_lv_ug)

                arr_too_close = []
                arr_too_far = []

                for i in range(len(arr_cur_lv_ug)):
                        # remove first and last vertex from checking
                        if i > 0 and i < len(arr_cur_lv_ug) - 1:
                                for vector_all in arr_temp:
                                        vector = arr_cur_lv_ug[i]
                                        m = distance.measureLine(vector, vector_all)
                                        if m < 0.29 and m > 0.005:
                                                # print(device_id + '[' + str(i + 1) + '/' + str(len(arr_cur_lv_oh)) + ']' + ' is too close to another conductor!')
                                                arr_too_close.append(device_id)
                                        elif m > 0.31 and m < 0.5:
                                                # print(device_id + ' is too far from another conductor')
                                                arr_too_far.append(device_id)
                if(len(arr_too_close) > 0):
                        arr.append(device_id)

        return arr

'''
# copy back the method above, but only do it for one device id
'''
def lv_ug_buffer_message(device_id):
        longitude = 0
        latitude = 0

        arr_lv_ug = []

        # qgis distanceArea
        distance = QgsDistanceArea()
        distance.setEllipsoid('WGS84')

        # get vectors of all LV UG (for comparison)
        arr_lv_ug = get_all_lv_ug_vector()

        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \''+ device_id + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
        for f in feat:
                # reset array values
                arr_temp = []
                arr_temp.extend(arr_lv_ug)
                arr_cur_lv_ug = []

                # get arr_cur_lv_ug (list of vectors to in one deviceid)
                device_id = f.attribute('device_id')
                geom = f.geometry()
                y = geom.mergeLines()
                polyline_y = y.asPolyline()
                for geom_y in polyline_y:
                        arr_cur_lv_ug.append(geom_y)

                #remove own vector from arr_temp
                for cur_lv_ug in arr_cur_lv_ug:
                        arr_temp.remove(cur_lv_ug)

                arr_too_close = []
                arr_too_far = []

                for i in range(len(arr_cur_lv_ug)):
                        
                        # remove first and last vertex from checking
                        if i > 0 and i < len(arr_cur_lv_ug) - 1:
                                for vector_all in arr_temp:
                                        vector = arr_cur_lv_ug[i]
                                        m = distance.measureLine(vector, vector_all)
                                        if m < 0.29 and m > 0.005:
                                                arr_too_close.append(i)
                                        elif m > 0.31 and m < 0.5:
                                                arr_too_far.append(i)
                if(len(arr_too_close) > 0):
                        # get vector geometry
                        vector_no = arr_too_close[0]
                        qgs_point_0 = arr_cur_lv_ug[vector_no]
                        # pass longitude/latitude
                        longitude = qgs_point_0.x()
                        latitude = qgs_point_0.y()
                        # print('device id: ' + device_id + ' ' + str(qgs_point_0))                
        
        e_msg = lv_ug_buffer_code + ',' + device_id + ',' + layer_name + ': ' + device_id + ' is too close to another conductor! (distance < 0.3m) ' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg


# **********************************
# ******* End of Validation  *******
# **********************************
