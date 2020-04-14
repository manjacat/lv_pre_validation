# Test import python file
from qgis.core import *
	
def count_lv_features(self):
    # print('counting LV UG conductor')
    try:
        layer_lv_ug = QgsProject.instance().mapLayersByName('LV_UG_Conductor')[0]
        feat_lv_ug = layer_lv_ug.getFeatures()
        count_lv_ug = 0
        for f1 in feat_lv_ug:
                count_lv_ug += 1
        self.dlg.count_lvug.setText(str(count_lv_ug))
    except:
        self.dlg.count_lvug.setText('E')
    
    # print('counting LV OH conductor')
    try:
        layer_lv_oh = QgsProject.instance().mapLayersByName('LV_OH_Conductor')[0]
        feat_lv_oh = layer_lv_oh.getFeatures()
        count_lv_oh = 0
        for f1 in feat_lv_oh:
            count_lv_oh += 1
        self.dlg.count_lvoh.setText(str(count_lv_oh))
    except:
        self.dlg.count_lvoh.setText('E')

    # print('counting LV Fuse')
    try:
        layer_lv_fuse = QgsProject.instance().mapLayersByName('LV_Fuse')[0]
        feat_lv_fuse = layer_lv_fuse.getFeatures()
        count_lv_fuse = 0
        for f1 in feat_lv_fuse:
            count_lv_fuse += 1
        self.dlg.count_lv_fuse.setText(str(count_lv_fuse))
    except:
        self.dlg.count_lv_fuse.setText('E')

    # print('counting LV Cable Joint')
    try:
        layer_lv_cj = QgsProject.instance().mapLayersByName('LV_Cable_Joint')[0]
        feat_lv_cj = layer_lv_cj.getFeatures()
        count_lv_cj = 0
        for f1 in feat_lv_cj:
                count_lv_cj += 1
        self.dlg.count_lv_cj.setText(str(count_lv_cj))
    except:
        self.dlg.count_lv_cj.setText('E')

    # print('counting LVDB-FP')
    try:
        layer_lvdb_fp = QgsProject.instance().mapLayersByName('LVDB-FP')[0]
        feat_lvdb_fp = layer_lvdb_fp.getFeatures()
        count_lvdb_fp = 0
        for f1 in feat_lvdb_fp:
                count_lvdb_fp += 1
        self.dlg.count_lvdb_fp.setText(str(count_lvdb_fp))
    except:
        self.dlg.count_lvdb_fp.setText('E')

    # print('counting Pole')
    try:
        layer_pole = QgsProject.instance().mapLayersByName('Pole')[0]
        feat_pole = layer_pole.getFeatures()
        count_pole = 0
        for f1 in feat_pole:
                count_pole += 1
        self.dlg.count_pole.setText(str(count_pole))
    except:
        self.dlg.count_pole.setText('E')

    # print('counting Demand Point')
    try:
        layer_dmd_pt = QgsProject.instance().mapLayersByName('Demand_Point')[0]
        feat_dmd_pt = layer_dmd_pt.getFeatures()
        count_dmd_pt = 0
        for f1 in feat_dmd_pt:
                count_dmd_pt += 1
        self.dlg.count_dmd_pt.setText(str(count_dmd_pt))
    except:
        self.dlg.count_dmd_pt.setText('E')

    # print('counting Street Light')
    try:
        layer_st_light = QgsProject.instance().mapLayersByName('Street_Light')[0]
        feat_st_light = layer_st_light.getFeatures()
        count_st_light = 0
        for f1 in feat_st_light:
                count_st_light += 1
        self.dlg.count_st_light.setText(str(count_st_light))
    except:
        self.dlg.count_st_light.setText('E')

    # print('counting Manhole')
    try:
        layer_manhole = QgsProject.instance().mapLayersByName('Manhole')[0]
        feat_manhole = layer_manhole.getFeatures()
        count_manhole = 0
        for f1 in feat_manhole:
                count_manhole += 1
        self.dlg.count_manhole.setText(str(count_manhole))
    except:
        self.dlg.count_manhole.setText('Skipped')

    # print('counting Structure Duct')
    try:
        layer_st_duct = QgsProject.instance().mapLayersByName('Structure_Duct')[0]
        feat_st_duct = layer_st_duct.getFeatures()
        count_st_duct = 0
        for f1 in feat_st_duct:
                count_st_duct += 1
        self.dlg.count_st_duct.setText(str(count_st_duct))
    except:
        self.dlg.count_st_duct.setText('Skipped')
        
    # end the function
    return 0



          
	
