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

# *****************************************
# ****** Check Z-M Value in shapefile *****
# *****************************************

def lv_ug_z_m_shapefile():
        arr = []
        arr = rps_z_m_shapefile(layer_name)
        return arr

def lv_ug_z_m_shapefile_message(geom_name):
        e_msg = lv_ug_z_m_shapefile_code + ',' + layer_name + ',' + 'Z M Value for ' + layer_name + ' is ' + geom_name+ '\n'
        return e_msg
        

# ****************************************
# ****** Check for Device_Id Format ******
# ****************************************

def lv_ug_device_id_format():
        arr = []
        arr = rps_device_id_format(layer_name)
        return arr

def lv_ug_device_id_format_message(device_id):
        e_msg = lv_ug_device_id_format_code + ',' + device_id + ',' + layer_name + ': ' + device_id + ' device_id format error \n'
        return e_msg

# **********************************
# ****** Check for Duplicates ******
# **********************************

def lv_ug_duplicate():
        arr = []
        arr = rps_duplicate_device_id(layer_name)
        return arr

def lv_ug_duplicate_message(device_id):
        e_msg = lv_ug_duplicate_code +',' + device_id + ',' + 'LV_UG_Conductor: ' + device_id + ' duplicated device_id: ' + device_id + '\n'
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
    e_msg = lv_ug_enum_valid +',' + device_id + ',' + 'LV_UG_Conductor: ' + device_id + ' Invalid Enumerator at: ' + field_name + '\n'
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
	e_msg = lv_ug_field_null +',' + device_id + ',' + 'LV_UG_Conductor: ' + device_id + ' Mandatory field NOT NULL at: ' + field_name + '\n'
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
	e_msg = lv_ug_lv_db_in_out_geom + ',' + device_id + ',' + 'LV_UG_Conductor: ' + device_id + ' column in_lvdb_id mismtach ' + '\n'
	return e_msg

def lv_ug_lv_db_out():
	#TODO
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
	e_msg = lv_ug_lv_db_in_out_geom + ',' + device_id + ',' + 'LV_UG_Conductor: ' + device_id + ' column out_lvdb_id mismatch' + '\n'
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
	e_msg = lv_ug_lvdb_in_out_col + ',' + device_id + ',' + 'LV_UG_Conductor: ' + device_id + ' lvdb_in_no/lvdb_ot_no MISSING' + '\n'
	return e_msg

def lv_ug_lvdb_no_check_message(device_id):
	e_msg = lv_ug_lvdb_in_out_col + ',' + device_id + ',' + 'LV_UG_Conductor: ' + device_id + ' lvdb_in_id/lvdb_out_i MISSING' + '\n'
	return e_msg

# **********************************
# ********* Check Length  **********
# **********************************

def lv_ug_length_check():
	arr = []
	
	return arr

def lv_ug_length_check_message(device_id):
	e_msg = lv_ug_length + ',' + device_id + ',' + layer_name + ': ' + device_id + ' length less than 1.5' + '\n'
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
def lv_ug_self_intersect():
        arr = []
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
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
                        arr_temp.remove(arr_line[h])
                        no_of_intersect = 0
                        for i in range(len(arr_temp)):
                                intersect = QgsGeometry.intersection(arr_line[h], arr_temp[i])
                                if intersect:
                                        no_of_intersect += 1
                        # print('intersect: ' + str(no_of_intersect))
                        if no_of_intersect > 2:
                                arr.append(device_id)
                        
        return arr

def lv_ug_self_intersect_message(device_id):
        e_msg = lv_ug_self_intersect_code + ',' + device_id + ',' + layer_name + ': ' + device_id + ' has self intersect geometry ' + '\n'
        return e_msg


# *************************************************
# ****** Buffer between LV UG must be > 0.3  ******
# *************************************************

# get all vertex of a LV UG conductor
# check distance between this vertex and other vertex of another conductor

'''
# buat last
'''

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
        for geom2 in arr_geom:
            # check for overlap
            if geom_g.overlaps(geom_2):
                arr.append(device_id)
    return arr

def lv_ug_coin_message(device_id):
    e_msg = lv_ug_coin_code + ',' + device_id + ',' + layer_name + ': ' + device_id + ' has coincidence geometry \n'
    return e_msg        

# **********************************
# ******* End of Validation  *******
# **********************************
