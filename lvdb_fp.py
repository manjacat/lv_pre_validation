# -*- coding: utf-8 -*-
"""
/***************************************************************************
All checkings related to LVDB-FP
 ***************************************************************************/
"""
from qgis.core import *
# import own custom file
from .dropdown_enum import *
from .rps_utility import rps_device_id_format
# regex
import re

layer_name = 'LVDB-FP'	
lvdb_fp_field_null = 'ERR_LVDVFP_01'
lvdb_fp_enum_valid = 'ERR_LVDBFP_02'
lvdb_fp_remarks_db_oper_code = 'ERR_LVDBFP_03'
lvdb_fp_lvf_design_code = 'ERR_LVDBFP_04'
lvdb_fp_duplicate_code = 'ERR_DUPLICATE_ID'
lvdb_fp_device_id_format_code = 'ERR_DEVICE_ID'

# ****************************************
# ****** Check for Device_Id Format ******
# ****************************************

def lvdb_fp_device_id_format():
        arr = []
        arr = rps_device_id_format(layer_name)
        return arr

def lvdb_fp_device_id_format_message(device_id):
        e_msg = lvdb_fp_device_id_format_code +',' + device_id + ',' + layer_name + ': ' + device_id + ' device_id format error \n'
        return e_msg

# **********************************
# ****** Check for Duplicates ******
# **********************************

def lvdb_fp_duplicate():
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

def lvdb_fp_duplicate_message(device_id):
        e_msg = lvdb_fp_duplicate_code +',' + device_id + ',' + layer_name + ': ' + device_id + ' duplicated device_id: ' + device_id + '\n'
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
        e_msg = lvdb_fp_enum_valid +',' + device_id + ',' + layer_name + ': ' + device_id + ' Invalid Enumerator at: ' + field_name + '\n'
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
	e_msg = lvdb_fp_field_null +',' + device_id + ',' + layer_name + ': ' + device_id + ' Mandatory field NOT NULL at: ' + field_name + '\n'
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
                        # print('pattern match:' + device_id + ': ' + remarks + ', ' + db_oper)
        return arr

def lvdb_fp_remarks_db_oper_message(device_id):
	e_msg = lvdb_fp_remarks_db_oper_code +',' + device_id + ',' + layer_name + ': ' + device_id + ' remarks and db_oper MISMATCH \n'
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
                # print('checking values for device_id ' + device_id + ', design = ', design)
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
        if design == 'FP 1600 A - 2 in 8 out' or design == 'FP 160000 A - 2 in 8 out (PE)' or design == 'LVDB 1600 A - 2 in 8 out':
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
	e_msg = lvdb_fp_lvf_design_code +',' + device_id + ',' + layer_name + ': ' + device_id + ' number of lvf/lvs columns does not match IN/OUT design \n'
	return e_msg

# **********************************
# ******* End of Validation  *******
# **********************************
