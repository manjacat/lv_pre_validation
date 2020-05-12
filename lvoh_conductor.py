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

# *****************************************
# ****** Check Z-M Value in shapefile *****
# *****************************************

def lv_oh_z_m_shapefile():
        arr = []
        arr = rps_z_m_shapefile(layer_name)
        return arr

def lv_oh_z_m_shapefile_message(geom_name):
        longitude = 0
        latitude = 0
        e_msg = lv_oh_z_m_shapefile_code + ',' + layer_name + ',' + 'Z M Value for ' + layer_name + ' is ' + geom_name + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg

# ****************************************
# ****** Check for Device_Id Format ******
# ****************************************

def lv_oh_device_id_format():
        arr = []
        arr = rps_device_id_format(layer_name)
        return arr

def lv_oh_device_id_format_message(device_id):
        longitude = 0
        latitude = 0

        e_msg = lv_oh_device_id_format_code +',' + device_id + ',' + layer_name + ': ' + device_id + ' device_id format error' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
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
        
        e_msg = lv_oh_duplicate_code +',' + device_id + ',' + layer_name + ': ' + device_id + ' duplicated device_id: ' + device_id + ',' + str(longitude) + ',' + str(latitude) + ' \n'
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
        
        e_msg = lv_oh_enum_valid +',' + device_id + ',' + layer_name +': ' + device_id + ' Invalid Enumerator at: ' + field_name + ',' + str(longitude) + ',' + str(latitude) + ' \n'
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
        longitude = 0
        latitude = 0

        e_msg = lv_oh_field_null +',' + device_id + ',' + layer_name + ': ' + device_id + ' Mandatory field NOT NULL at: ' + field_name + ',' + str(longitude) + ',' + str(latitude) + ' \n'
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
        longitude = 0
        latitude = 0

        e_msg = lv_oh_length_check_code + ',' + device_id + ',' + layer_name + ': ' + device_id + ' length less than 1.5' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
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
                                        # elif m > 1.1 and m < 4:
                                        #       print('WARNING: ' + device_id + ': vertex [' + str(i) + ']- distance pole to vertex is ' + str(round(m,3)) + 'm (more than 1.0m!!)')                        
                        if total_vertex != len(arr_vertex):
                                print('total vertex:' + str(total_vertex) + ', vertex near pole: ' + str(len(arr_vertex)))
                                arr.append(device_id)
        return arr

def lv_oh_vertex_pole_message(device_id):
        longitude = 0
        latitude = 0
        
        e_msg = lv_oh_vertex_pole_code + ',' + device_id + ',' + layer_name + ': ' + device_id + ' has vertex not near a pole ' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
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
                        # remove duplicate device_id
                        if no_of_intersect > 2 and device_id not in arr:
                                arr.append(device_id)
                        
        return arr

def lv_oh_self_intersect_message(device_id):
        longitude = 0
        latitude = 0
        
        e_msg = lv_oh_self_intersect_code + ',' + device_id + ',' + layer_name + ': ' + device_id + ' has self intersect geometry ' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
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

def lv_oh_hanging():
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

                # get other vertex of LV OH
                arr_point = []
                arr_device_id = []
                layer_lv_oh = QgsProject.instance().mapLayersByName(layer_name)[0]
                query = '"device_id" != \'' + device_id + '\''
                feat_lv_oh = layer_lv_oh.getFeatures(QgsFeatureRequest().setFilterExpression(query))
                for g in feat_lv_oh:
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

                # get lv ug vector: (1st point and last point is enough)
                layer_lv_ug = QgsProject.instance().mapLayersByName('LV_UG_Conductor')[0]
                feat_lv_ug = layer_lv_ug.getFeatures()
                for h in feat_lv_ug:
                        device_temp = g.attribute('device_id')
                        geom_h = h.geometry()
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
                        j_point = geom_j.asPoint()
                        arr_point.append(j_point)

                # get LV Cable Joint
                layer_lv_cj = QgsProject.instance().mapLayersByName('LV_Cable_Joint')[0]
                feat_lv_cj = layer_lv_cj.getFeatures()
                for j in feat_lv_cj:
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
                if len(arr_snap_v_one) == 0 or len(arr_snap_v_last) == 0 and device_id not in arr:
                        arr.append(device_id)
        return arr

def lv_oh_hanging_message(device_id):
        longitude = 0
        latitude = 0
        
        e_msg = lv_oh_hanging_code + ',' + device_id + ',' + layer_name + ': ' + device_id + ' is hanging ' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg

# **************************************
# ********* Check Buffer 0.3  **********
# **************************************

def lv_oh_buffer():
        arr = []
        arr_lv_oh = []

        # qgis distanceArea
        distance = QgsDistanceArea()
        distance.setEllipsoid('WGS84')

        # get vectors of all LV OH (for comparison)
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        feat =  layer.getFeatures()
        for f in feat:
                geom = f.geometry()
                y = geom.mergeLines()
                polyline_y = y.asPolyline()
                for geom_y in polyline_y:
                        arr_lv_oh.append(geom_y)

        # main function
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        feat =  layer.getFeatures()
        for f in feat:
                # reset array values
                arr_temp = []
                arr_temp.extend(arr_lv_oh)
                arr_cur_lv_oh = []

                # get arr_cur_lv_oh (list of vectors to in one deviceid)
                device_id = f.attribute('device_id')
                geom = f.geometry()
                y = geom.mergeLines()
                polyline_y = y.asPolyline()
                for geom_y in polyline_y:
                        arr_cur_lv_oh.append(geom_y)

                #remove own vector from arr_temp
                for cur_lv_oh in arr_cur_lv_oh:
                        arr_temp.remove(cur_lv_oh)

                arr_too_close = []
                arr_too_far = []

                for i in range(len(arr_cur_lv_oh)):
                        # remove first and last vertex from checking
                        if i > 0 and i < len(arr_cur_lv_oh) - 1:
                                for vector_all in arr_temp:
                                        vector = arr_cur_lv_oh[i]
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

def lv_oh_buffer_message(device_id):
        longitude = 0
        latitude = 0
        
        e_msg = lv_oh_buffer_code + ',' + device_id + ',' + layer_name + ': ' + device_id + ' is too close to another conductor! (distance < 0.3m) ' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg


# **********************************
# ******* End of Validation  *******
# **********************************
