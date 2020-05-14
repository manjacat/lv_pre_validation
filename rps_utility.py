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
                

        vendor_code = 'R'
        station_code = '([1-9][0-9]{0,3})' # accepts 1 - 9999
        running_number = '([0-9]{0,6})' # accepts 000 - 999999
        pattern = '^' + vendor_code + station_code + object_code + running_number + '$'
        # print(pattern)

        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        feat = layer.getFeatures()
        for f in feat:
                device_id = f.attribute('device_id')
                check = re.search(pattern, device_id)
                # print('device id =' + device_id)
                # print(check)
                if not check:
                        arr.append(device_id)
        return arr


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
        arr_line_type = ['LV_UG_Conductor','LV_OH_Conductor']
        arr_point_type = ['LV_Fuse','LV_Cable_Joint','LVDB-FP','Pole','Demand_Point','Street_Light','Manhole','Structure_Duct']
        if layer_name in arr_line_type:
                wkb_type = 'MultiLineString'
        elif layer_name in arr_point_type:
                wkb_type = 'Point'
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        feat = layer.getFeatures()
        # run once only
        check = 0
        for f in feat:
                device_id = f.attribute('device_id')
                geom = f.geometry()
                if check == 0:
                        geom_type = QgsWkbTypes.displayString(geom.wkbType())
                        # print('geometry type is ', geom_type)
                        if geom_type != wkb_type:
                                arr.append(geom_type)
                        check += 1
                
        return arr

# ********************************************
# ********* Get Midpoint of Line  **********
# ********************************************

def rps_get_midpoint(layer_name, device_id):

        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + device_id + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))

        vector_midpoint = None

        for f in feat:
                geom = f.geometry()
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

# ********************************************
# ********* Get Vector Zero of Line  **********
# ********************************************

def rps_get_firstpoint(layer_name, device_id):

        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + device_id + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))

        vector_firstpoint = None

        for f in feat:
                geom = f.geometry()
                y = geom.mergeLines()
                polyline_y = y.asPolyline()
                # get total no of vectors
                total = len(polyline_y)
                firstpoint = 0
                # print('midpoint is ', divide2)
                vector_firstpoint = polyline_y[firstpoint]

        return vector_firstpoint

# ********************************************
# ********* Get Second Point of Line  **********
# ********************************************

def rps_get_secondpoint(layer_name, device_id):

        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + device_id + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))

        vector_second_point = None

        for f in feat:
                geom = f.geometry()
                y = geom.mergeLines()
                polyline_y = y.asPolyline()
                # get total no of vectors
                total = len(polyline_y)
                second_point = 1
                # print('midpoint is ', divide2)
                vector_second_point = polyline_y[second_point]

        return vector_second_point

# ********************************************
# ********* Get Last Point of Line  **********
# ********************************************

def rps_get_lastpoint(layer_name, device_id):

        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + device_id + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))

        vector_lastpoint = None

        for f in feat:
                geom = f.geometry()
                y = geom.mergeLines()
                polyline_y = y.asPolyline()
                # get total no of vectors
                total = len(polyline_y)
                lastpoint = total - 1
                # print('midpoint is ', divide2)
                vector_lastpoint = polyline_y[lastpoint]

        return vector_lastpoint

# **********************************
# ******* End of Validation  *******
# **********************************
