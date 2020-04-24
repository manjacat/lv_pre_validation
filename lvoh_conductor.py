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

# *****************************************
# ****** Check Z-M Value in shapefile *****
# *****************************************

def lv_oh_z_m_shapefile():
        arr = []
        arr = rps_z_m_shapefile(layer_name)
        return arr

def lv_oh_z_m_shapefile_message(geom_name):
        e_msg = lv_oh_z_m_shapefile_code + ',' + layer_name + ',' + 'Z M Value for ' + layer_name + ' is ' + geom_name+ '\n'
        return e_msg

# ****************************************
# ****** Check for Device_Id Format ******
# ****************************************

def lv_oh_device_id_format():
        arr = []
        arr = rps_device_id_format(layer_name)
        return arr

def lv_oh_device_id_format_message(device_id):
        e_msg = lv_oh_device_id_format_code +',' + device_id + ',' + layer_name + ': ' + device_id + ' device_id format error \n'
        return e_msg
# **********************************
# ****** Check for Duplicates ******
# **********************************

def lv_oh_duplicate():
        arr = []
        arr = rps_duplicate_device_id(layer_name)

        return arr

def lv_oh_duplicate_message(device_id):
        e_msg = lv_oh_duplicate_code +',' + device_id + ',' + layer_name + ': ' + device_id + ' duplicated device_id: ' + device_id + '\n'
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
        e_msg = lv_oh_enum_valid +',' + device_id + ',' + layer_name +': ' + device_id + ' Invalid Enumerator at: ' + field_name + '\n'
        return e_msg

# **********************************
# ****** Check for Not Null   ******
# **********************************

def lv_oh_field_not_null(field_name):
	arr = []
	layer = QgsProject.instance().mapLayersByName(layer_name)[0]
	query = '"' + field_name + '" is null OR ' + '"' + field_name + '" =  \'N/A\''
	feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
	for f in feat:
		device_id = f.attribute('device_id')
		arr.append(device_id)
	return arr

def lv_oh_field_not_null_message(device_id, field_name):
	e_msg = lv_oh_field_null +',' + device_id + ',' + layer_name + ': ' + device_id + ' Mandatory field NOT NULL at: ' + field_name + '\n'
	return e_msg

# **********************************
# ********* Check Length  **********
# **********************************

def lv_oh_length_check():
	arr = []
	layer = QgsProject.instance().mapLayersByName(layer_name)[0]
	query = '"length" <= 1.5'
	feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
	for f in feat:
		device_id = f.attribute('device_id')
		arr.append(device_id)
	return arr

def lv_oh_length_check_message(device_id):
	e_msg = lv_oh_length_check_code + ',' + device_id + ',' + layer_name + ': ' + device_id + ' length less than 1.5' + '\n'
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
        arr_exclude_usage = ['5 FOOT WAYS','SERVICE LINE']
        for f in feat:
                device_id = f.attribute('device_id')
                usage = f.attribute('usage')
                geom = f.geometry()
                y = geom.mergeLines()
                total_vertex = len(y.asPolyline())
                if total_vertex > 2 and usage not in arr_exclude_usage :
                        arr_vertex = []
                        for i in range(total_vertex):
                                for pole_geom in arr_pole_geom:
                                        vertex = y.asPolyline()[i]
                                        m = distance.measureLine(pole_geom, vertex)
                                        if m <= 1.1:
                                                arr_vertex.append(vertex)
                                        elif m > 1.1 and m < 4:
                                                print('WARNING: ' + device_id + ': vertex [' + str(i) + ']- distance pole to vertex is ' + str(round(m,3)) + 'm (more than 1.0m!!)')                        
                        if total_vertex != len(arr_vertex):
                                print('total vertex:' + str(total_vertex) + ', vertex near pole: ' + str(len(arr_vertex)))
                                arr.append(device_id)
        return arr

def lv_oh_vertex_pole_message(device_id):
        e_msg = lv_oh_vertex_pole_code + ',' + device_id + ',' + layer_name + ': ' + device_id + ' has vertex not near a pole ' + '\n'
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
def lv_oh_self_intersect():
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

def lv_oh_self_intersect_message(device_id):
        e_msg = lv_oh_self_intersect_code + ',' + device_id + ',' + layer_name + ': ' + device_id + ' has self intersect geometry ' + '\n'
        return e_msg

# **********************************
# ******* End of Validation  *******
# **********************************
