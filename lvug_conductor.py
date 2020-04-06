# Test import python file
# TODO: tukar return type kepada array
from qgis.core import *

def lvug_callMe():
	print('lvug_conductor is called')


lvug_error1 = 'ERR_LVUGCOND_01'
def lvug_fieldNotNull(fieldName):
        layer_lvug = QgsProject.instance().mapLayersByName('LV_UG_Conductor')[0]
        query = '"' + fieldName + '" is null'
        feat_lvug = layer_lvug.getFeatures(QgsFeatureRequest().setFilterExpression(query))
        return(feat_lvug)

def lvug_fieldNotNullMessage(device_id, fieldName):
        eMsg = 'LV_UG_Conductor:' + device_id + ' Mandatory field NOT NULL at: ' + fieldName
        return(eMsg)

def lvug_duplicate():
        layer_lvug = QgsProject.instance().mapLayersByName('LV_UG_Conductor')[0]
        feat_lvug = layer_lvug.getFeatures()
        for f in feat_lvug:
                device_id = f.attribute('device_id')
                
                
        

def TestGeom3Apr():
        # LVDB layer
        print('This is LVDB-FP:')
        layer = QgsProject.instance().mapLayersByName('LVDB-FP')[0]
        query = '"device_id" = \'R6142lvdb01\''
        featLVDB = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))

        # now loop through the features, perform geometry computation and print the results
        for f in featLVDB:
                geom = f.geometry()
                device_id = f.attribute('device_id')
                lvdb_loc = f.attribute('lvdb_loc')
                status = f.attribute('status')
                print('Device ID: ', device_id)
                x = geom.asPoint()
                print("Point: ", x)

        # LVUG conductor layer
        print('This is LV UG Conductor:')
        layer = QgsProject.instance().mapLayersByName('LV_UG_Conductor')[0]
        query = '"device_id" = \'R6142ugc004\''
        featLVUG = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))

        # now loop through the features, perform geometry computation and print the results
        for f in featLVUG:
                gLine = f.geometry()
                device_id = f.attribute('device_id')
                label = f.attribute('label')
                status = f.attribute('status')
                print('Device ID: ', device_id)
                print('this geometry is', QgsWkbTypes.displayString(gLine.wkbType()))
                #convert MultiLineString to LineString
                y = gLine.mergeLines()
                print('converted to', QgsWkbTypes.displayString(y.wkbType()))
                print("LineString: ", y)

          
	
