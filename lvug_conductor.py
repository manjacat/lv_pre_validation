# Test import python file
# tukar return type kepada array
from qgis.core import *
# import own custom file
from .dropdown_enum import *

def lvug_call_me():
	print('lv ug_conductor is called')


lv_ug_field_null = 'ERR_LVUGCOND_01'
lv_ug_enum_valid = 'ERR_LVUGCOND_02'
lv_ug_lv_db_in_out_geom = 'ERR_LVUGCOND_04'
lv_ug_lvdb_in_out_col = 'ERR_LVUGCOND_03'

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
        
        layer_lv_ug = QgsProject.instance().mapLayersByName('LV_UG_Conductor')[0]
        feat_lv_ug = layer_lv_ug.getFeatures()
        for f in feat_lv_ug:
                device_id = f.attribute('device_id')
                field_value = f.attribute(field_name)
                if field_value not in arr_dropdown:
                        arr.append(device_id)
        return arr

def lv_ug_field_enum_message(device_id, field_name):
        e_msg = lv_ug_enum_valid +',' + device_id + ',' + 'LV_UG_Conductor:' + device_id + ' Invalid Enumerator at: ' + field_name + '\n'
        return e_msg

# **********************************
# ****** Check for Not Null   ******
# **********************************

def lv_ug_field_not_null(field_name):
	arr = []
	layer_lv_ug = QgsProject.instance().mapLayersByName('LV_UG_Conductor')[0]
	query = '"' + field_name + '" is null OR ' + '"' + field_name + '" =  \'N/A\''
	feat_lv_ug = layer_lv_ug.getFeatures(QgsFeatureRequest().setFilterExpression(query))
	for f in feat_lv_ug:
		device_id = f.attribute('device_id')
		arr.append(device_id)
	return arr

def lv_ug_field_not_null_message(device_id, field_name):
	e_msg = lv_ug_field_null +',' + device_id + ',' + 'LV_UG_Conductor:' + device_id + ' Mandatory field NOT NULL at: ' + field_name + '\n'
	return e_msg

# ************************************
# ****** Check for Duplicate ID ******
# ************************************

def lvug_duplicate():
	#TODO
	layer_lvug = QgsProject.instance().mapLayersByName('LV_UG_Conductor')[0]
	feat_lvug = layer_lvug.getFeatures()
	for f in feat_lvug:
		device_id = f.attribute('device_id')

# **********************************
# ****** Check for LVDB Flow  ******
# **********************************

def lv_ug_lv_db_in():
	#TODO
	arr = []
	layer_lvug = QgsProject.instance().mapLayersByName('LV_UG_Conductor')[0]
	feat_lvug = layer_lvug.getFeatures()
	for f in feat_lvug:
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
	e_msg = lv_ug_lv_db_in_out_geom + ',' + device_id + ',' + 'LV_UG_Conductor:' + device_id + ' column in_lvdb_id mismtach ' + '\n'
	return e_msg

def lv_ug_lv_db_out():
	arr = []
	layer_lvug = QgsProject.instance().mapLayersByName('LV_UG_Conductor')[0]
	feat_lvug = layer_lvug.getFeatures()
	for f in feat_lvug:
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
				distance = QgsDistanceArea()
				distance.setEllipsoid('WGS84')
				distance_xy = distance.measureLine(y.asPolyline()[0], geom_x)
				if distance_xy > 0.001:
                                        print("WARNING: outgoing distance > 0:")
                                        print("Point1 (LVUG):",y.asPolyline()[0])
                                        print("Point2 (LVDB):",geom_x)
                                        print("difference:", format(distance_xy, '.9f'))
                                        arr.append(device_id)

	return arr

def lvug_lvdb_out_message(device_id):
	e_msg = lv_ug_lv_db_in_out_geom + ',' + device_id + ',' + 'LV_UG_Conductor:' + device_id + ' column out_lvdb_id mismatch' + '\n'
	return e_msg

# ************************************
# ****** Check for LVDB in/out  ******
# ************************************

def lv_ug_lvdb_id_in_check():
	arr = []
	layer_lv_ug = QgsProject.instance().mapLayersByName('LV_UG_Conductor')[0]
	query = '"in_lvdb_id" is not null OR "out_lvdb_i" is not null'
	feat_lv_ug = layer_lv_ug.getFeatures(QgsFeatureRequest().setFilterExpression(query))
	for f in feat_lv_ug:
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
	layer_lv_ug = QgsProject.instance().mapLayersByName('LV_UG_Conductor')[0]
	query = '"in_lvdb_id" is not null OR "out_lvdb_i" is not null'
	feat_lv_ug = layer_lv_ug.getFeatures(QgsFeatureRequest().setFilterExpression(query))
	for f in feat_lv_ug:
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
	layer_lv_ug = QgsProject.instance().mapLayersByName('LV_UG_Conductor')[0]
	query = '"lvdb_in_no" is not null OR "lvdb_ot_no" is not null'
	feat_lv_ug = layer_lv_ug.getFeatures(QgsFeatureRequest().setFilterExpression(query))
	for f in feat_lv_ug:
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
	layer_lv_ug = QgsProject.instance().mapLayersByName('LV_UG_Conductor')[0]
	query = '"lvdb_in_no" is not null OR "lvdb_ot_no" is not null'
	feat_lv_ug = layer_lv_ug.getFeatures(QgsFeatureRequest().setFilterExpression(query))
	for f in feat_lv_ug:
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
	e_msg = lv_ug_lvdb_in_out_col + ',' + device_id + ',' + 'LV_UG_Conductor:' + device_id + ' lvdb_in_no/lvdb_ot_no MISSING' + '\n'
	return e_msg

def lv_ug_lvdb_no_check_message(device_id):
	e_msg = lv_ug_lvdb_in_out_col + ',' + device_id + ',' + 'LV_UG_Conductor:' + device_id + ' lvdb_in_id/lvdb_out_i MISSING' + '\n'
	return e_msg

				


	
