# Test import python file
# tukar return type kepada array
from qgis.core import *

def lvug_call_me():
	print('lv ug_conductor is called')


lv_ug_field_null = 'ERR_LVUGCOND_01'
lv_ug_lv_db_in_out = 'ERR_LVUGCOND_04'

def lv_ug_field_not_null(fieldName):
	arr = []
	layer_lv_ug = QgsProject.instance().mapLayersByName('LV_UG_Conductor')[0]
	query = '"' + fieldName + '" is null OR ' + '"' + fieldName + '" =  \'N/A\''
	feat_lv_ug = layer_lv_ug.getFeatures(QgsFeatureRequest().setFilterExpression(query))
	for f in feat_lv_ug:
		device_id = f.attribute('device_id')
		arr.append(device_id)
	return arr

def lv_ug_field_not_null_message(device_id, field_name):
	e_msg = lv_ug_field_null +',' + device_id + ',' + 'LV_UG_Conductor:' + device_id + ' Mandatory field NOT NULL at: ' + field_name + '\n'
	return e_msg

def lvug_duplicate():
	#TODO
	layer_lvug = QgsProject.instance().mapLayersByName('LV_UG_Conductor')[0]
	feat_lvug = layer_lvug.getFeatures()
	for f in feat_lvug:
		device_id = f.attribute('device_id')

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
                                if distance_xy > 0:
                                        print("WARNING: incoming distance > 0")
                                        print("Point1 (LVUG):", y.asPolyline()[len(y.asPolyline())-1])
                                        print("Point2 (LVDB):", geom_x)
                                        print("difference:", format(distance_xy,'.9f'))
                                if distance_xy > 0.001:
                                        arr.append(device_id)
	return arr

def lv_ug_lv_db_in_message(device_id):
	e_msg = lv_ug_lv_db_in_out + ',' + device_id + ',' + 'LV_UG_Conductor:' + device_id + ' column in_lvdb_id mismtach ' + '\n'
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
				if distance_xy > 0:
                                        print("WARNING: outgoing distance > 0:")
                                        print("Point1 (LVUG):",y.asPolyline()[0])
                                        print("Point2 (LVDB):",geom_x)
                                        print("difference:", format(distance_xy, '.9f'))
                                        if distance_xy > 0.001:
                                                arr.append(device_id)

	return arr

def lvug_lvdb_out_message(device_id):
	e_msg = lv_ug_lv_db_in_out + ',' + device_id + ',' + 'LV_UG_Conductor:' + device_id + ' column out_lvdb_id mismatch' + '\n'
	return e_msg

				


	
