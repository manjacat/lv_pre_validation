# Test import python file
# tukar return type kepada array
from qgis.core import *

def lvug_callMe():
	print('lvug_conductor is called')


lvug_fieldNull = 'ERR_LVUGCOND_01'
lvug_lvdbInOut = 'ERR_LVUGCOND_04'

def lvug_fieldNotNull(fieldName):
        arr = []
        layer_lvug = QgsProject.instance().mapLayersByName('LV_UG_Conductor')[0]
        query = '"' + fieldName + '" is null OR ' + '"' + fieldName + '" =  \'N/A\''
        feat_lvug = layer_lvug.getFeatures(QgsFeatureRequest().setFilterExpression(query))
        for f in feat_lvug:
                device_id = f.attribute('device_id')
                arr.append(device_id)
        return(arr)

def lvug_fieldNotNullMessage(device_id, fieldName):
        eMsg = lvug_fieldNull +',' + device_id + ',' + 'LV_UG_Conductor:' + device_id + ' Mandatory field NOT NULL at: ' + fieldName + '\n'
        return(eMsg)

def lvug_duplicate():
	#TODO
        layer_lvug = QgsProject.instance().mapLayersByName('LV_UG_Conductor')[0]
        feat_lvug = layer_lvug.getFeatures()
        for f in feat_lvug:
                device_id = f.attribute('device_id')

def lvug_lvdb_in():
        #TODO
        arr = []
        layer_lvug = QgsProject.instance().mapLayersByName('LV_UG_Conductor')[0]
        feat_lvug = layer_lvug.getFeatures()
        for f in feat_lvug:
                device_id = f.attribute('device_id')
                in_lvdb_id = f.attribute('in_lvdb_id')
                if in_lvdb_id:
                        layer_lvdb = QgsProject.instance().mapLayersByName('LVDB-FP')[0]
                        query = '"device_id" = \'' + in_lvdb_id + '\''
                        feat_lvdb = layer_lvdb.getFeatures(QgsFeatureRequest().setFilterExpression(query))
                        lvdb_device_id = ''
                        for lvdb in feat_lvdb:
                                lvdb_device_id = lvdb.attribute('device_id')
                                geom = lvdb.geometry()
                                geomx = geom.asPoint()
                                #arr.append(lvdb_device_id)
                        if lvdb_device_id:
                                query = '"in_lvdb_id" = \''+ lvdb_device_id +'\' and "device_id" = \''+ device_id + '\''
                                feat_lvugIncoming = layer_lvug.getFeatures(QgsFeatureRequest().setFilterExpression(query))
                                for h in feat_lvugIncoming:
                                        lvug_device_id = h.attribute('device_id')
                                        #arr.append(lvug_device_id)
                                        gLine = h.geometry()
                                        y = gLine.mergeLines()
                                        lastVertex = y.asPolyline()[0]
                                        distanceXY = y.asPolyline()[0].distance(geomx)
                                        # print('INBOUND CHECK: distance from first vertex:', distanceXY)
                                        # if distance == 0, means its outgoing
                                        # if distance > 0, means its incoming
                                        if(distanceXY == 0):
                                                arr.append(lvug_device_id)
                                        
        return(arr)

def lvug_lvdb_inMessage(device_id):
        eMsg = lvug_lvdbInOut +',' + device_id + ',' + 'LV_UG_Conductor:' + device_id + ' column in_lvdb_id mismtach ' + '\n'
        return(eMsg)

def lvug_lvdb_out():
        #TODO
        arr = []
        layer_lvug = QgsProject.instance().mapLayersByName('LV_UG_Conductor')[0]
        feat_lvug = layer_lvug.getFeatures()
        for f in feat_lvug:
                device_id = f.attribute('device_id')
                gLine = f.geometry()
                y = gLine.mergeLines()
                firstVertex = y.asPolyline()[0]
                out_lvdb_id = f.attribute('out_lvdb_i')
                if out_lvdb_id:
                        layer_lvdb = QgsProject.instance().mapLayersByName('LVDB-FP')[0]
                        query = '"device_id" = \'' + out_lvdb_id + '\''
                        feat_lvdb = layer_lvdb.getFeatures(QgsFeatureRequest().setFilterExpression(query))
                        lvdb_device_id = ''
                        for lvdb in feat_lvdb:
                                lvdb_device_id = lvdb.attribute('device_id')
                                geom = lvdb.geometry()
                                geomx = geom.asPoint()
                                #arr.append(lvdb_device_id)
                        if lvdb_device_id:
                                # qgis distanceArea
                                distance = QgsDistanceArea()
                                distance.setEllipsoid('WGS84')
                                distanceXY = distance.measureLine(y.asPolyline()[0],geomx)
                                myMsg ='OUTGOING CHECK: distance from LVDB:' + lvdb_device_id + ' and LVUG:' + device_id + '[0] = ' + str(distanceXY)
                                #print(myMsg)
                                if(distanceXY > 0):
                                        print("Point1 (LVUG):",y.asPolyline()[0])
                                        print("Point2 (LVDB):",geomx)
                                        print("difference:", distanceXY)
                                # if distance == 0, means its outgoing
                                # if distance > 0, means its incoming
                                if(distanceXY > 0.001):
                                        arr.append(device_id)
                                
                                        
        return(arr)

def lvug_lvdb_outMessage(device_id):
        eMsg = lvug_lvdbInOut +',' + device_id + ',' + 'LV_UG_Conductor:' + device_id + ' column out_lvdb_id mismatch' + '\n'
        return(eMsg)
                        
				

          
	
