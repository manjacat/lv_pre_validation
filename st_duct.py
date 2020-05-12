# -*- coding: utf-8 -*-
"""
/***************************************************************************
All checkings related to Structure Duct
 ***************************************************************************/
"""
from qgis.core import *
# import own custom file
from .dropdown_enum import *
from .rps_utility import *

layer_name = 'Structure_Duct'	
st_duct_field_null = 'ERR_STDUCT_01'
st_duct_enum_valid = 'ERR_STDUCT_02'
st_duct_duplicate_code = 'ERR_DUPLICATE_ID'
st_duct_device_id_format_code = 'ERR_DEVICE_ID'
st_duct_z_m_shapefile_code = 'ERR_Z_M_VALUE'

# *****************************************
# ****** Check Z-M Value in shapefile *****
# *****************************************

def st_duct_z_m_shapefile():
        arr = []
        arr = rps_z_m_shapefile(layer_name)
        return arr

def st_duct_z_m_shapefile_message(geom_name):
        longitude = 0
        latitude = 0

        e_msg = st_duct_z_m_shapefile_code + ',' + layer_name + ',' + 'Z M Value for ' + layer_name + ' is ' + geom_name + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg

# ****************************************
# ****** Check for Device_Id Format ******
# ****************************************

def st_duct_device_id_format():
        arr = []
        arr = rps_device_id_format(layer_name)
        return arr

def st_duct_device_id_format_message(device_id):
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
        
        e_msg = st_duct_device_id_format_code +',' + device_id + ',' + layer_name + ': ' + device_id + ' device_id format error ' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg

# **********************************
# ****** Check for Duplicates ******
# **********************************

def st_duct_duplicate():
        arr = []
        arr = rps_device_id_format(layer_name)

        return arr

def st_duct_duplicate_message(device_id):
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
        
        e_msg = st_duct_duplicate_code +',' + device_id + ',' + layer_name + ': ' + device_id + ' duplicated device_id: ' + device_id + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg

# **********************************
# ****** Check for Enum Value ******
# **********************************

def st_duct_field_enum(field_name):
        arr = []
        arr_dropdown = []
        if field_name == 'status':
                arr_dropdown = arr_status
        elif field_name == 'db_oper':
                arr_dropdown = arr_db_oper
        elif field_name == 'size':
                arr_dropdown = arr_size_st_duct
        elif field_name == 'method':
                arr_dropdown = arr_method_st_duct
        elif field_name == 'way':
                arr_dropdown = arr_way_st_duct
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

def st_duct_field_enum_message(device_id, field_name):
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
        
        e_msg = st_duct_enum_valid +',' + device_id + ',' + layer_name + ': ' + device_id + ' Invalid Enumerator at: ' + field_name + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg

# **********************************
# ****** Check for Not Null   ******
# **********************************

def st_duct_field_not_null(field_name):
	arr = []
	layer = QgsProject.instance().mapLayersByName(layer_name)[0]
	query = '"' + field_name + '" is null OR ' + '"' + field_name + '" =  \'N/A\''
	feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
	for f in feat:
		device_id = f.attribute('device_id')
		arr.append(device_id)
	return arr

def st_duct_field_not_null_message(device_id, field_name):
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

        e_msg = st_duct_field_null +',' + device_id + ',' + layer_name + ': ' + device_id + ' Mandatory field NOT NULL at: ' + field_name + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg

# **********************************
# ********* TODO  **********
# **********************************


# **********************************
# ******* End of Validation  *******
# **********************************
