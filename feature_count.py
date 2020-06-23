# Test import python file
from qgis.core import *

# for testing purposes
from .analysis import *
	
def count_lv_features(self):
    # print('counting LV UG conductor')
    try:
        layer_lv_ug = QgsProject.instance().mapLayersByName('LV_UG_Conductor')[0]
        count_lv_ug = layer_lv_ug.featureCount()
        self.dlg.count_lvug.setText(str(count_lv_ug))
    except Exception as e:
        self.dlg.count_lvug.setText('0')
    
    # print('counting LV OH conductor')
    try:
        layer_lv_oh = QgsProject.instance().mapLayersByName('LV_OH_Conductor')[0]
        count_lv_oh = layer_lv_oh.featureCount()
        self.dlg.count_lvoh.setText(str(count_lv_oh))
    except Exception as e:
        self.dlg.count_lvoh.setText('0')

    # print('counting LV Fuse')
    try:
        layer_lv_fuse = QgsProject.instance().mapLayersByName('LV_Fuse')[0]
        count_lv_fuse = layer_lv_fuse.featureCount()
        self.dlg.count_lv_fuse.setText(str(count_lv_fuse))
    except Exception as e:
        self.dlg.count_lv_fuse.setText('0')

    # print('counting LV Cable Joint')
    try:
        layer_lv_cj = QgsProject.instance().mapLayersByName('LV_Cable_Joint')[0]
        count_lv_cj = layer_lv_cj.featureCount()
        self.dlg.count_lv_cj.setText(str(count_lv_cj))
    except Exception as e:
        self.dlg.count_lv_cj.setText('0')

    # print('counting LVDB-FP')
    try:
        layer_lvdb_fp = QgsProject.instance().mapLayersByName('LVDB-FP')[0]
        count_lvdb_fp = layer_lvdb_fp.featureCount()
        self.dlg.count_lvdb_fp.setText(str(count_lvdb_fp))
    except Exception as e:
        self.dlg.count_lvdb_fp.setText('0')

    # print('counting Pole')
    try:
        layer_pole = QgsProject.instance().mapLayersByName('Pole')[0]
        count_pole = layer_pole.featureCount()
        self.dlg.count_pole.setText(str(count_pole))
    except Exception as e:
        self.dlg.count_pole.setText('0')

    # print('counting Demand Point')
    try:
        layer_dmd_pt = QgsProject.instance().mapLayersByName('Demand_Point')[0]
        count_dmd_pt = layer_dmd_pt.featureCount()
        self.dlg.count_dmd_pt.setText(str(count_dmd_pt))
    except Exception as e:
        self.dlg.count_dmd_pt.setText('0')

    # print('counting Street Light')
    try:
        layer_st_light = QgsProject.instance().mapLayersByName('Street_Light')[0]
        count_st_light = layer_st_light.featureCount()
        self.dlg.count_st_light.setText(str(count_st_light))
    except Exception as e:
        self.dlg.count_st_light.setText('0')

    # print('counting Manhole')
    try:
        layer_manhole = QgsProject.instance().mapLayersByName('Manhole')[0]
        count_manhole = layer_manhole.featureCount()
        self.dlg.count_manhole.setText(str(count_manhole))
    except Exception as e:
        self.dlg.count_manhole.setText('0')

    # print('counting Structure Duct')
    try:
        layer_st_duct = QgsProject.instance().mapLayersByName('Structure_Duct')[0]
        count_st_duct = layer_st_duct.featureCount()
        self.dlg.count_st_duct.setText(str(count_st_duct))
    except Exception as e:
        self.dlg.count_st_duct.setText('0')

        # print('counting Customer')
        try:
            layer_customer = QgsProject.instance().mapLayersByName('Customer')[0]
            count_customer = layer_customer.featureCount()
            self.dlg.count_customer.setText(str(count_customer))
        except Exception as e:
            self.dlg.count_customer.setText('0')

    # try_lukis_line()
    # try_lukis_polygon()
    # test_buffer()  
    # end the function
    return 0



          
	
