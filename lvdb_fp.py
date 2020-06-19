# -*- coding: utf-8 -*-
"""
/***************************************************************************
All checkings related to LVDB-FP

12/6/2020 - Fixed design check missed when user choose 'FP 1600 A - 2 in 8 out (PE)'
(this value was recently changed)

 ***************************************************************************/
"""
from qgis.core import *
# import own custom file
from .dropdown_enum import *
from .rps_utility import *
# regex
import re

layer_name = 'LVDB-FP'	
lvdb_fp_field_null = 'ERR_LVDVFP_01'
lvdb_fp_enum_valid = 'ERR_LVDBFP_02'
lvdb_fp_remarks_db_oper_code = 'ERR_LVDBFP_03'
lvdb_fp_lvf_design_code = 'ERR_LVDBFP_04'
lvdb_fp_snapping_code = 'ERR_LVDBFP_05'
lvdb_fp_duplicate_code = 'ERR_DUPLICATE_ID'
lvdb_fp_device_id_format_code = 'ERR_DEVICE_ID'
lvdb_fp_z_m_shapefile_code = 'ERR_Z_M_VALUE'

# *****************************************
# ****** Check Z-M Value in shapefile *****
# *****************************************

def lvdb_fp_z_m_shapefile():
        arr = []
        arr = rps_z_m_shapefile(layer_name)
        return arr

def lvdb_fp_z_m_shapefile_message(device_id):
        longitude = 0
        latitude = 0
        e_msg = rps_z_m_shapefile_message(layer_name, device_id, lvdb_fp_z_m_shapefile_code)
        return e_msg

# ****************************************
# ****** Check for Device_Id Format ******
# ****************************************

def lvdb_fp_device_id_format():
        arr = []
        arr = rps_device_id_format(layer_name)
        return arr

def lvdb_fp_device_id_format_message(device_id):
        longitude = 0
        latitude = 0
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + str(device_id) + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
        for f in feat:
                geom = f.geometry()
                if geom:
                        geom_type = QgsWkbTypes.displayString(geom.wkbType())
                        if geom_type == 'Point':
                                point = geom.asPoint()
                                longitude = point.x()
                                latitude = point.y()
        
        e_msg = lvdb_fp_device_id_format_code +',' + str(device_id) + ',' + layer_name + ': ' + str(device_id) + ' device_id format error' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg

# **********************************
# ****** Check for Duplicates ******
# **********************************

def lvdb_fp_duplicate():
        arr = []
        arr = rps_duplicate_device_id(layer_name)
        
        return arr

def lvdb_fp_duplicate_message(device_id):
        longitude = 0
        latitude = 0
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + str(device_id) + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
        for f in feat:
                geom = f.geometry()
                if geom:
                        geom_type = QgsWkbTypes.displayString(geom.wkbType())
                        if geom_type == 'Point':
                                point = geom.asPoint()
                                longitude = point.x()
                                latitude = point.y()
        
        e_msg = lvdb_fp_duplicate_code +',' + str(device_id) + ',' + layer_name + ': ' + str(device_id) + ' duplicated device_id: ' + str(device_id) + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg

# **********************************
# ****** Check for Enum Value ******
# **********************************

def lvdb_fp_field_enum(field_name):
        arr = []
        arr_dropdown = []
        if field_name == 'status':
                arr_dropdown = arr_status
        elif field_name == 'lvdb_loc':
                arr_dropdown = arr_lvdb_loc
        elif field_name == 'design':
                arr_dropdown = arr_design_lvdb
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

def lvdb_fp_field_enum_message(device_id, field_name):
        longitude = 0
        latitude = 0
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + str(device_id) + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
        for f in feat:
                geom = f.geometry()
                if geom:
                        geom_type = QgsWkbTypes.displayString(geom.wkbType())
                        if geom_type == 'Point':
                                point = geom.asPoint()
                                longitude = point.x()
                                latitude = point.y()
        
        e_msg = lvdb_fp_enum_valid +',' + str(device_id) + ',' + layer_name + ': ' + str(device_id) + ' Invalid Enumerator at: ' + field_name + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg

# **********************************
# ****** Check for Not Null   ******
# **********************************

def lvdb_fp_field_not_null(field_name):
	arr = []
	layer = QgsProject.instance().mapLayersByName(layer_name)[0]
	query = '"' + field_name + '" is null OR ' + '"' + field_name + '" =  \'N/A\''
	feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
	for f in feat:
		device_id = f.attribute('device_id')
		arr.append(device_id)
	return arr

def lvdb_fp_field_not_null_message(device_id, field_name):
        longitude = 0
        latitude = 0
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + str(device_id) + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
        for f in feat:
                geom = f.geometry()
                if geom:
                        geom_type = QgsWkbTypes.displayString(geom.wkbType())
                        if geom_type == 'Point':
                                point = geom.asPoint()
                                longitude = point.x()
                                latitude = point.y()
                
        e_msg = lvdb_fp_field_null +',' + str(device_id) + ',' + layer_name + ': ' + str(device_id) + ' Mandatory field NOT NULL at: ' + field_name + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg

# **********************************************
# ********* REMARKS/DB OPER MISMATCH  **********
# **********************************************

'''
# Quote shahid:
# all LVDB are existing, in the remarks column, SW_ID is added.
# all FP are new. in the remarks column, there is no SW_ID information.
# hence, we check if there is SW_ID information in the remarks column.
# if got SW_ID, [db_oper] is Update. otherwise, [db_oper] is Insert.
'''

def lvdb_fp_remarks_db_oper():
        arr = []
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        feat = layer.getFeatures()
        for f in feat:
                device_id = f.attribute('device_id')
                remarks = f.attribute('remarks')
                db_oper = f.attribute('db_oper')
                if remarks:
                        #9 digit pattern: SW ID
                        pattern = "[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]"
                        check = re.search(pattern, remarks)
                        if check and db_oper == 'Insert':
                                arr.append(device_id)
                        elif not check and db_oper == 'Update':
                                arr.append(device_id)
                        else :
                                # do nothing
                                rem2 = f.attribute('remarks')
                                # print('pattern match:' + str(device_id) + ': ' + remarks + ', ' + db_oper)
        return arr

def lvdb_fp_remarks_db_oper_message(device_id):
        longitude = 0
        latitude = 0
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + str(device_id) + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
        for f in feat:
                geom = f.geometry()
                if geom:
                        geom_type = QgsWkbTypes.displayString(geom.wkbType())
                        if geom_type == 'Point':
                                point = geom.asPoint()
                                longitude = point.x()
                                latitude = point.y()
                
        e_msg = lvdb_fp_remarks_db_oper_code +',' + str(device_id) + ',' + layer_name + ': ' + str(device_id) + ' remarks and db_oper MISMATCH ' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg

# ********************************************************************
# ********* Number of LVF columns filled must match Design  **********
# ********************************************************************

'''
# check [design] column. if it says 2 in 8 out,
# then all lv in columns ([lvs_1], [lvs_2]) must not be null
# similarly, all lv out columns ([lvf_1] to [lvs_8]) must not be null
'''

def lvdb_fp_lvf_design():
        arr = []
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        feat = layer.getFeatures()
        for f in feat:
                device_id = f.attribute('device_id')
                design = f.attribute('design')
                lvf_1 = f.attribute('lvf_1')
                lvf_2 = f.attribute('lvf_2')
                lvf_3 = f.attribute('lvf_3')
                lvf_4 = f.attribute('lvf_4')
                lvf_5 = f.attribute('lvf_5')
                lvf_6 = f.attribute('lvf_6')
                lvf_7 = f.attribute('lvf_7')
                lvf_8 = f.attribute('lvf_8')
                lvf_9 = f.attribute('lvf_9')
                lvf_10 = f.attribute('lvf_10')
                lvs_1 = f.attribute('lvs_1')
                lvs_2 = f.attribute('lvs_2')


                arr_lvf = [lvf_1, lvf_2, lvf_3, lvf_4, lvf_5, lvf_6, lvf_7, lvf_8, lvf_9, lvf_10]
                arr_lvs = [lvs_1, lvs_2]
                lv_in = 2
                lv_out = get_lv_out_number(design)
                count_out = 0
                count_in = 0
                # print('checking values for device_id ' + str(device_id) + ', design = ', design)
                # check null values in lvs (in)
                for index_in in range(lv_in):
                        lvs = arr_lvs[index_in]
                        # print('lvs_'+ str(index_in + 1) +' value is = ' + str(lvs))
                        if lvs :
                                count_in += 1
                                
                # check null values in lvf (out)
                for index_out in range(lv_out):
                        lvf = arr_lvf[index_out]
                        # print('lvf_'+ str(index_out + 1) +' value is = ' + str(lvf))
                        if lvf :
                                count_out += 1
                
                
                # print('count_out = ' + str(count_out) + ' lv_out = ' + str(lv_out))
                # print('count_in = ' + str(count_in) + ' lv_in = ' + str(lv_in))
                # if count mismatch with design, add to error list
                if count_out != lv_out or count_in != lv_in :
                        arr.append(device_id)
                
        return arr


def get_lv_out_number(design):
        lv_out = 0
        #total design dropdown value = 8
        if design == 'FP 1600 A - 2 in 8 out' or design == 'FP 1600 A - 2 in 8 out (PE)' or design == 'LVDB 1600 A - 2 in 8 out':
                lv_out = 8
        elif design == 'FP 800 A - 2 in 5 out' or design == 'LVDB 800 A - 2 in 5 out (CS)':
                lv_out = 5
        elif design == 'LVDB 1600 A - 2 in 10 out (CS)':
                lv_out = 10
        elif design == 'LVDB 800 A - 2 in 6 out (CS)' or design == 'MINI FP 400 A - 2 in 6 out':
                lv_out = 6
        else :
                lv_out = 0
        return lv_out
        

def lvdb_fp_lvf_design_message(device_id):
        longitude = 0
        latitude = 0
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + str(device_id) + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
        for f in feat:
                geom = f.geometry()
                if geom:
                        geom_type = QgsWkbTypes.displayString(geom.wkbType())
                        if geom_type == 'Point':
                                point = geom.asPoint()
                                longitude = point.x()
                                latitude = point.y()

        e_msg = lvdb_fp_lvf_design_code +',' + str(device_id) + ',' + layer_name + ': ' + str(device_id) + ' number of lvf/lvs columns does not match IN/OUT design ' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg

# **************************************
# ********* LVDB-FP Snapping  **********
# **************************************
'''
# The newly inserted LVDB-FP should be connected to at least one Conductor.
# Step 1: list all vectors of LV OH/LV UG
# Step 2: list all geom of LVDB-FP where db_oper = 'Insert'
# Step 3: at least ONE LVDB-FP must have distance between it and LV OH/LV UG == 0
# Step 4: if LVDB-FP is not nearby LV UG/LV OH Vectors, then error.
'''

def lvdb_fp_snapping(arr_lv_ug_exclude_geom, arr_lv_oh_exclude_geom):
        arr = []
        arr_lv = []
        # qgis distanceArea
        distance = QgsDistanceArea()
        distance.setEllipsoid('WGS84')

        layerLV_01 = QgsProject.instance().mapLayersByName('LV_OH_Conductor')[0]
        feat_01 = layerLV_01.getFeatures()
        for f in feat_01:
                device_temp = f.attribute('device_id')
                if device_temp not in arr_lv_oh_exclude_geom:
                        geom = f.geometry()
                        y = geom.mergeLines()
                        polyline_y = y.asPolyline()
                        # loop all vertex in this line
                        for geom_01 in polyline_y:
                               arr_lv.append(geom_01)

        layerLV_02 = QgsProject.instance().mapLayersByName('LV_UG_Conductor')[0]
        feat_02 = layerLV_02.getFeatures()
        for f in feat_02:
                device_temp = f.attribute('device_id')
                if device_temp not in arr_lv_ug_exclude_geom:
                        geom = f.geometry()
                        y = geom.mergeLines()
                        polyline_y = y.asPolyline()
                        #loop all vertex in this line
                        for geom_02 in polyline_y:
                                arr_lv.append(geom_02)
        # print(arr_lv)

        # get geom of lvdb-fp layer
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"db_oper" =  \'Insert\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
        for f in feat:
                device_id = f.attribute('device_id')
                # print('device_id insert:', device_id)
                geom = f.geometry()
                if geom:
                        geom_type = QgsWkbTypes.displayString(geom.wkbType())
                        if geom_type == 'Point':
                                geom_x = geom.asPoint()
                                # new arr_snapping each loop
                                arr_snapping = []
                                for geom_lv in arr_lv:
                                        m = distance.measureLine(geom_lv, geom_x)
                                        if m < 0.001:
                                                arr_snapping.append(device_id)
                                if len(arr_snapping) == 0:
                                        arr.append(device_id)
        
        return arr

def lvdb_fp_snapping_message(device_id):
        longitude = 0
        latitude = 0
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        query = '"device_id" = \'' + str(device_id) + '\''
        feat = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
        for f in feat:
                geom = f.geometry()
                if geom:
                        geom_type = QgsWkbTypes.displayString(geom.wkbType())
                        if geom_type == 'Point':
                                point = geom.asPoint()
                                longitude = point.x()
                                latitude = point.y()

        e_msg = lvdb_fp_snapping_code + ',' + str(device_id) + ',' + layer_name + ': ' + str(device_id) + ' LVDB-FP is hanging ' + ',' + str(longitude) + ',' + str(latitude) + ' \n'
        return e_msg


# **********************************
# ******* End of Validation  *******
# **********************************
