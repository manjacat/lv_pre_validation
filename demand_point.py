# -*- coding: utf-8 -*-
"""
/***************************************************************************
All checkings related to Demand Point
 ***************************************************************************/
"""
from qgis.core import *
# import own custom file
from .dropdown_enum import *
from .rps_utility import rps_device_id_format

layer_name = 'Demand_Point'	
dmd_pt_field_null = 'ERR_DEMANDPT_01'
dmd_pt_enum_valid = 'ERR_DEMANDPT_02'
dmd_pt_duplicate_code = 'ERR_DUPLICATE_ID'
dmd_pt_device_id_format_code = 'ERR_DEVICE_ID'
dmd_pt_remarks_code = 'ERR_DEMANDPT_04'
dmd_pt_snapping_code = 'ERR_DEMANDPT_03'

# ****************************************
# ****** Check for Device_Id Format ******
# ****************************************

def dmd_pt_device_id_format():
        arr = []
        arr = rps_device_id_format(layer_name)
        return arr

def dmd_pt_device_id_format_message(device_id):
        e_msg = dmd_pt_device_id_format_code +',' + device_id + ',' + layer_name + ': ' + device_id + ' device_id format error \n'
        return e_msg

# **********************************
# ****** Check for Duplicates ******
# **********************************

def dmd_pt_duplicate():
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

def dmd_pt_duplicate_message(device_id):
        e_msg = dmd_pt_duplicate_code +',' + device_id + ',' + layer_name + ': ' + device_id + ' duplicated device_id: ' + device_id + '\n'
        return e_msg


# **********************************
# ****** Check for Enum Value ******
# **********************************

def dmd_pt_field_enum(field_name):
        arr = []
        arr_dropdown = []
        if field_name == 'status':
                arr_dropdown = arr_status       
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

def dmd_pt_field_enum_message(device_id, field_name):
        e_msg = dmd_pt_enum_valid +',' + device_id + ',' + layer_name + ': ' + device_id + ' Invalid Enumerator at: ' + field_name + '\n'
        return e_msg

# **********************************
# ****** Check for Not Null   ******
# **********************************

def dmd_pt_field_not_null(field_name):
	arr = []
	layer = QgsProject.instance().mapLayersByName(layer_name)[0]
	query = '"' + field_name + '" is null OR ' + '"' + field_name + '" =  \'N/A\''
	feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
	for f in feat:
		device_id = f.attribute('device_id')
		arr.append(device_id)
	return arr

def dmd_pt_field_not_null_message(device_id, field_name):
	e_msg = dmd_pt_field_null +',' + device_id + ',' + layer_name + ': ' + device_id + ' Mandatory field NOT NULL at: ' + field_name + '\n'
	return e_msg

# ***************************************
# ********* Check for Remarks  **********
# ***************************************

'''
# Step 1 : list down all demand point device id from Street Light
# Step 2 : check Demand Point where Device Id in arr_device_id
# Step 3 : check Remarks column. Remarks must be == 'STREET LIGHT PANEL'
'''

def dmd_pt_remarks():
        arr = []
        arr_dmd_pnt_id = get_dmd_pnt_id()
        # print(arr_dmd_pnt_id)
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        feat = layer.getFeatures()
        for f in feat:
                device_id = f.attribute('device_id')
                if device_id in arr_dmd_pnt_id:
                        remarks = f.attribute('remarks')
                        if remarks != 'STREET LIGHT PANEL':
                                arr.append(device_id)
        return arr

def get_dmd_pnt_id():
        arr_dmd_pnt_id = []
        layer = QgsProject.instance().mapLayersByName('Street_Light')[0]
        query = '"dmd_pnt_id" is not null'
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
        for f in feat:
                dmd_pnt_id = f.attribute('dmd_pnt_id')
                arr_dmd_pnt_id.append(dmd_pnt_id)

        return arr_dmd_pnt_id;
        

def dmd_pt_remarks_message(device_id):
	e_msg = dmd_pt_remarks_code +',' + device_id + ',' + layer_name + ': ' + device_id + ' remarks must be STREET LIGHT PANEL \n'
	return e_msg

# **********************************************************************
# ********* Check for Demand Point not in end point/snapping  **********
# **********************************************************************

'''
# Step 1: Get geometry of all conductors (LV UG, LV OH)
# Step 2: Get last vertext of all geometry of Step 1
# Step 3: Get geometry of all demand point
# Step 4: Geometry of demand point must snap to at least one of LV UG/LV OH
# Step 5: if not snap to any cable == error
'''

def dmd_pt_snapping():
        arr = []
        arr_lv_vertex = []
        # qgis distanceArea
        distance = QgsDistanceArea()
        distance.setEllipsoid('WGS84')

        # Get geometry of LV OH, LV UG
        arr_layer_name = ['LV_OH_Conductor','LV_UG_Conductor']
        for lyr in arr_layer_name:
                layer_lv_01 = QgsProject.instance().mapLayersByName(lyr)[0]
                feat_lv_01 = layer_lv_01.getFeatures()
                for f in feat_lv_01:
                        geom = f.geometry()
                        y = geom.mergeLines()
                        # Get last vertex
                        arr_lv_vertex.append(y.asPolyline()[len(y.asPolyline())-1])
        # print('total array:',len(arr_lv_vertex))

        # Get geometry of Demand point and check distance
        # print('layer_name is:',layer_name)
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        feat = layer.getFeatures()
        for f in feat:
                device_id = f.attribute('device_id')
                geom = f.geometry()
                # new arr_snapping each loop
                arr_snapping = []
                # loop through all LV OH & LV UG
                for geom_lv in arr_lv_vertex:
                        geom_x = geom.asPoint()
                        m = distance.measureLine(geom_lv, geom_x)
                        # print('distance in meters',m)
                        if m < 0.001:
                                arr_snapping.append(device_id)
                if len(arr_snapping) == 0:
                        arr.append(device_id)        
        return arr

def dmd_pt_snapping_message(device_id):
	e_msg = dmd_pt_snapping_code +',' + device_id + ',' + layer_name + ': ' + device_id + ' hanging \n'
	return e_msg

# **********************************
# ******* End of Validation  *******
# **********************************
