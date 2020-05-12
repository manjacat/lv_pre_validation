# -*- coding: utf-8 -*-
"""
/***************************************************************************
 seperating main button with GUI code
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QFileDialog

from qgis.core import *

def try_lukis_line():

    points = []

    device_id = 'R6142ohc220'
    layer = QgsProject.instance().mapLayersByName('LV_OH_Conductor')[0]
    query = '"device_id" = \'' +  device_id + '\''
    feat =  layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
    temp_device_id = ''
    for f in feat:
        geom = f.geometry()
        y = geom.mergeLines()
        polyline_y = y.asPolyline()
        for a in polyline_y:
            points.append(a)

    my_layer_name = 'LV_OH_' + device_id

    layer = QgsVectorLayer('LineString', my_layer_name , "memory")
    pr = layer.dataProvider()
    line = QgsFeature()
    line.setGeometry(QgsGeometry.fromPolylineXY(points))
    pr.addFeatures([line])
    layer.updateExtents()
    QgsProject.instance().addMapLayers([layer])

    return 0

def try_lukis_polygon():
    
    points = []

    device_id = 'R6142ugc013'
    layer = QgsProject.instance().mapLayersByName('LV_UG_Conductor')[0]
    query = '"device_id" = \'' +  device_id + '\''
    feat =  layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
    temp_device_id = ''
    for f in feat:
        geom = f.geometry()
        y = geom.mergeLines()
        polyline_y = y.asPolyline()
    point_01 = QgsGeometry.fromPointXY(polyline_y[2])
    bufferGeom_01 = point_01.buffer(0.00000275,5)
    # print(bufferGeom_01)

    point_02 = QgsGeometry.fromPointXY(polyline_y[1])
    bufferGeom_02 = point_02.buffer(0.00000275,5)
    # print(bufferGeom_02)

    layer = QgsVectorLayer('Polygon', 'vector_2', "memory")
    pr = layer.dataProvider()
    poly = QgsFeature()
    poly.setGeometry(bufferGeom_01)
    poly2 = QgsFeature()
    poly2.setGeometry(bufferGeom_02)
    pr.addFeatures([poly])
    pr.addFeatures([poly2])
    layer.updateExtents()

    # print(poly)
    QgsProject.instance().addMapLayers([layer])
    print('printed')
    return 0

'''
# get array of LV OH vectors
# get all vectors in LV OH - device id
# for each vector, compare with array of LV OH
'''
def test_buffer():    
    arr = []
    arr_lv_ug = []

    # qgis distanceArea
    distance = QgsDistanceArea()
    distance.setEllipsoid('WGS84')

    # get vectors of all LV OH
    layer = QgsProject.instance().mapLayersByName('LV_UG_Conductor')[0]
    feat =  layer.getFeatures()
    for f in feat:
        geom = f.geometry()
        y = geom.mergeLines()
        polyline_y = y.asPolyline()
        for geom_y in polyline_y:
            arr_lv_ug.append(geom_y)

    # print(len(arr_lv_ug))
        

    layer = QgsProject.instance().mapLayersByName('LV_UG_Conductor')[0]    
    feat =  layer.getFeatures()
    for f in feat:
        # reset array values
        arr_temp = []
        arr_temp.extend(arr_lv_ug)
        arr_cur_lv_ug = []

        # get arr_cur_lv_ug value
        device_id = f.attribute('device_id')
        geom = f.geometry()
        y = geom.mergeLines()
        polyline_y = y.asPolyline()
        for geom_y in polyline_y:
            arr_cur_lv_ug.append(geom_y)

        # remove own vector from arr_temp.
        for cur_lv_ug in arr_cur_lv_ug:
            arr_temp.remove(cur_lv_ug)

        arr_too_close = []
        arr_too_far = []
        for i in range(len(arr_cur_lv_ug)):
            # remove first and last vertex from checking
            if i > 0 and i < len(arr_cur_lv_ug) - 1:
                for vector_all in arr_temp:
                    vector = arr_cur_lv_ug[i]
                    m = distance.measureLine(vector, vector_all)
                
                    if m < 0.29 and m > 0.005:
                        print(device_id + '[' + str(i + 1) + '/' + str(len(arr_cur_lv_ug)) + ']' + ' is too close to another conductor')
                        arr_too_close.append(device_id)
                    elif m > 0.31 and m < 0.5:
                        # print(device_id + ' is too far from another conductor')
                        arr_too_far.append(device_id)
        if(len(arr_too_close) > 0):
            print(device_id + ' is too close to another conductor')

    return 0
    
