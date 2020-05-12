# -*- coding: utf-8 -*-
"""
/***************************************************************************
All checkings related to Street Light
 ***************************************************************************/
"""
from qgis.core import *
# import own custom file
from .dropdown_enum import *
from .rps_utility import *

layer_name = 'Street_Light'	
st_light_field_null = 'ERR_STLIGHT_01'
st_light_enum_valid = 'ERR_STLIGHT_02'
st_light_cont_dev_code = 'ERR_STLIGHT_03'
st_light_overlap_pole_code = 'ERR_STLIGHT_04'
st_light_phasing_code = 'ERR_STLIGHT_05'
st_light_duplicate_code = 'ERR_DUPLICATE_ID'
st_light_device_id_format_code = 'ERR_DEVICE_ID'
max_distance_m = 0.001
st_light_z_m_shapefile_code = 'ERR_Z_M_VALUE'

# *****************************************
# ****** Check Z-M Value in shapefile *****
# *****************************************

def st_light_z_m_shapefile():
        arr = []
        arr = rps_z_m_shapefile(layer_name)
        return arr

def st_light_z_m_shapefile_message(geom_name):
        e_msg = st_light_z_m_shapefile_code + ',' + layer_name + ',' + 'Z M Value for ' + layer_name + ' is ' + geom_name+ '\n'
        return e_msg

# ****************************************
# ****** Check for Device_Id Format ******
# ****************************************

def st_light_device_id_format():
        arr = []
        arr = rps_device_id_format(layer_name)
        return arr

def st_light_device_id_format_message(device_id):
        longitude = 0
        latitude = 0
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + device_id + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query)) 
        for f in feat:
                geom = f.geometry()
                point = geom.asPoint()
                longitude = point.x()
                latitude = point.y()
        e_msg = st_light_device_id_format_code +',' + device_id + ',' + layer_name + ': ' + device_id + ' device_id format error' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg

# **********************************
# ****** Check for Duplicates ******
# **********************************

def st_light_duplicate():
        arr = []
        arr = rps_duplicate_device_id(layer_name)

        return arr

def st_light_duplicate_message(device_id):
        longitude = 0
        latitude = 0
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + device_id + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query)) 
        for f in feat:
                geom = f.geometry()
                point = geom.asPoint()
                longitude = point.x()
                latitude = point.y()
        e_msg = st_light_duplicate_code +',' + device_id + ',' + layer_name + ': ' + device_id + ' duplicated device_id: ' + device_id + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg

# **********************************
# ****** Check for Enum Value ******
# **********************************

def st_light_field_enum(field_name):
        arr = []
        arr_dropdown = []
        # phasing moved to 'Phasing should be R'
        if field_name == 'status':
                arr_dropdown = arr_status
        elif field_name == 'db_oper':
                arr_dropdown = arr_db_oper
        elif field_name == 'cont_dev':
                arr_dropdown = arr_cont_dev
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

def st_light_field_enum_message(device_id, field_name):
        longitude = 0
        latitude = 0
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + device_id + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query)) 
        for f in feat:
                geom = f.geometry()
                point = geom.asPoint()
                longitude = point.x()
                latitude = point.y()
        e_msg = st_light_enum_valid +',' + device_id + ',' + layer_name + ': ' + device_id + ' Invalid Enumerator at: ' + field_name + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg

# ********************************************
# ****** Check for Street Light Panel   ******
# ********************************************

'''
# If dmd_pnt_it is not null, Street Light control device (cont_dev) should be 'PANEL'
# at the same time, the demand point's remarks should be 'STREET LIGHT PANEL'
'''

def st_light_cont_dev():
        arr = []
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        feat = layer.getFeatures()
        for f in feat:
                device_id = f.attribute('device_id')
                dmd_pnt_id = f.attribute('dmd_pnt_id')                
                if dmd_pnt_id:
                        cont_dev = f.attribute('cont_dev')
                        if cont_dev != 'PANEL':                        
                                arr.append(device_id)
        return arr
        
def st_light_cont_dev_message(device_id):
        longitude = 0
        latitude = 0
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + device_id + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query)) 
        for f in feat:
                geom = f.geometry()
                point = geom.asPoint()
                longitude = point.x()
                latitude = point.y()
        e_msg = st_light_cont_dev_code +',' + device_id + ',' + layer_name + ': ' + device_id + ' cont_device should be PANEL if dmd_pnt_id is not null' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg

# **********************************
# ****** Check for Not Null   ******
# **********************************

def st_light_field_not_null(field_name):
	arr = []
	layer = QgsProject.instance().mapLayersByName(layer_name)[0]
	query = '"' + field_name + '" is null OR ' + '"' + field_name + '" =  \'N/A\''
	feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
	for f in feat:
		device_id = f.attribute('device_id')
		arr.append(device_id)
	return arr

def st_light_field_not_null_message(device_id, field_name):
        longitude = 0
        latitude = 0
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + device_id + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query)) 
        for f in feat:
                geom = f.geometry()
                point = geom.asPoint()
                longitude = point.x()
                latitude = point.y()
        e_msg = st_light_field_null + ',' + device_id + ',' + layer_name + ': ' + device_id + ' Mandatory field NOT NULL at: ' + field_name + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg

# *******************************************
# ********* Phasing should be 'R'  **********
# *******************************************

def st_light_phasing():
        arr = []
        arr_dropdown = []
        field_name = 'phasing'
        arr_dropdown = arr_phasing_st_light
        
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        feat = layer.getFeatures()
        for f in feat:
                device_id = f.attribute('device_id')
                field_value = f.attribute(field_name)
                if field_value not in arr_dropdown:
                        arr.append(device_id)
        return arr

def st_light_phasing_message(device_id):
        longitude = 0
        latitude = 0
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + device_id + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query)) 
        for f in feat:
                geom = f.geometry()
                point = geom.asPoint()
                longitude = point.x()
                latitude = point.y()

        e_msg = st_light_phasing_code + ',' + device_id + ',' + layer_name + ': ' + device_id + ' phasing should be "R" ' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg

# ********************************************************
# ********* Street Light MUST overlap with Pole  **********
# ********************************************************

'''
# Step 1: list all Pole Geom
# Step 2: list all Street Light Geom
# Step 3: check if distance between Street Light Geom && Pole Geom > allowable distance
# FIXED: actual rule is Street Light must overlap pole
'''

def st_light_overlap_pole():
        arr = []
        # qgis distanceArea
        distance = QgsDistanceArea()
        distance.setEllipsoid('WGS84')
        
        #get pole geom
        arr_geom_pole = []
        layer_pole = QgsProject.instance().mapLayersByName('Pole')[0]
        feat_pole = layer_pole.getFeatures()
        for f in feat_pole:
                geom_pole = f.geometry()
                arr_geom_pole.append(geom_pole)
        # print('total arr_geom_pole is ', str(len(arr_geom_pole)))

        # get street light geom
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        feat = layer.getFeatures()
        # query = '"device_id" = \'R6142stl020\''
        # feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
        
        for f in feat:
                no_touches = 0
                device_id = f.attribute('device_id')
                # compare with geom pole array
                for geom_p in arr_geom_pole:
                        geom_st_light = f.geometry()
                        # print('geom pole is :', geom_p)
                        # print('geom st_light is :',geom_st_light)
                        m = distance.measureLine(geom_p.asPoint(), geom_st_light.asPoint())
                        touches1 = QgsGeometry.touches(geom_p, geom_st_light)
                        if touches1:
                                print('geom pole is :', geom_p)
                                print('geom st_light is :',geom_st_light)
                                no_touches += 1
                        if m < max_distance_m:
                                no_touches += 1
                # print('total touches ' + device_id + ': ' + str(no_touches))
                if no_touches == 0:
                        arr.append(device_id)
        return arr

def st_light_overlap_pole_message(device_id):
        longitude = 0
        latitude = 0
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + device_id + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query)) 
        for f in feat:
                geom = f.geometry()
                point = geom.asPoint()
                longitude = point.x()
                latitude = point.y()
        e_msg = st_light_overlap_pole_code + ',' + device_id + ',' + layer_name + ': ' + device_id + ' Street Light MUST overlap Pole ' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg
        


# **********************************
# ******* End of Validation  *******
# **********************************
