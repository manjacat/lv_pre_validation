# -*- coding: utf-8 -*-
"""
/***************************************************************************
 seperating main button with GUI code
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QFileDialog

# Added by Khairil
from qgis.core import QgsProject, Qgis

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .lv_pre_validation_dialog import lv_pre_validationDialog
import os.path
# TODO: import own custom python file
from .lvoh_conductor import *
from .lvug_conductor import *
from .lv_fuse import *
from .lv_cable_joint import *
from .lvdb_fp import *
from .pole import *
from .demand_point import *
from .street_light import *
from .manhole import *
from .st_duct import *
from .feature_count import count_lv_features

def exec_validation(self):

    # test calling from new python file
    # print('Hello from new python file')
    
    # count features
    count_lv_features(self)
    
    #*****************************************************
    #***********     INITIALIZE VARIABLE    **************
    #*****************************************************

    #start total_error count
    lv_ug_error = 0
    lv_oh_error = 0
    lv_fuse_error = 0
    lv_cj_error = 0
    lvdb_fp_error = 0
    pole_error = 0
    dmd_pt_error = 0
    st_light_error = 0
    manhole_error = 0
    st_duct_error = 0
    total_error = 0
    # error message
    e_msg = ''

    #***************************************************************
    #***********     CHECK HOW MANY FEATURES SELECTED    ***********
    #***************************************************************

    # init flags
    lv_ug_flag = self.dlg.checkBox_lvug.isChecked()        
    lv_oh_flag = self.dlg.checkBox_lvoh.isChecked()
    lv_fuse_flag = self.dlg.checkBox_lv_fuse.isChecked()
    lv_cj_flag = self.dlg.checkBox_lv_cj.isChecked()
    lvdb_fp_flag = self.dlg.checkBox_lvdb_fp.isChecked()
    pole_flag = self.dlg.checkBox_pole.isChecked()
    dmd_pt_flag = self.dlg.checkBox_dmd_pt.isChecked()
    st_light_flag = self.dlg.checkBox_st_light.isChecked()
    manhole_flag = self.dlg.checkBox_manhole.isChecked()
    st_duct_flag = self.dlg.checkBox_st_duct.isChecked()

    feat_count = 0
    arr_feat_count = []
    if self.dlg.checkBox_lvug.isChecked():
        arr_feat_count.append('LV_UG_Conductor')
        feat_count += 1
    if self.dlg.checkBox_lvoh.isChecked():
        arr_feat_count.append('LV_OH_Conductor')
        feat_count += 1
    if self.dlg.checkBox_lv_fuse.isChecked():
        arr_feat_count.append('LV_Fuse')
        feat_count += 1
    if self.dlg.checkBox_lv_cj.isChecked():
        arr_feat_count.append('LV_Cable_Joint')
        feat_count += 1
    if self.dlg.checkBox_lvdb_fp.isChecked():
        arr_feat_count.append('LVDB-FP')
        feat_count += 1
    if self.dlg.checkBox_pole.isChecked():
        arr_feat_count.append('Pole')
        feat_count += 1
    if self.dlg.checkBox_dmd_pt.isChecked():
        arr_feat_count.append('Demand_Point')
        feat_count += 1
    if self.dlg.checkBox_st_light.isChecked():
        arr_feat_count.append('Street_Light')
        feat_count += 1
    if self.dlg.checkBox_manhole.isChecked():
        arr_feat_count.append('Manhole')
        feat_count += 1
    if self.dlg.checkBox_st_duct.isChecked():
        arr_feat_count.append('Structure_Duct')
        feat_count += 1

    qa_qc_msg = 'No features selected fo QA/QC validation.'
    if feat_count > 0:
        qa_qc_msg = ' ' .join(['running QA/QC now on ',str(feat_count),'features:'])
    print(qa_qc_msg)
    if len(arr_feat_count) > 0:
        print(arr_feat_count)

    #****************************************************************
    #***************     LV UG COND VALIDATION    *******************
    #****************************************************************

    arr_lv_ug = []

    # check z-m shapefile
    if lv_ug_flag:
        arr_lv_ug = lv_ug_z_m_shapefile()
        for device_id in arr_lv_ug:
            e_msg += lv_ug_z_m_shapefile_message(device_id)
            lv_ug_error += 1
            total_error += 1

    # check for duplicates
    if lv_ug_flag:
        arr_lv_ug = lv_ug_duplicate()
        for device_id in arr_lv_ug:
            e_msg += lv_ug_duplicate_message(device_id)
            lv_ug_error += 1
            total_error += 1

    # check for device_id format
    if lv_ug_flag:
        arr_lv_ug = lv_ug_device_id_format()
        for device_id in arr_lv_ug:
            e_msg += lv_ug_device_id_format_message(device_id)
            lv_ug_error += 1
            total_error += 1

    # check for mandatory not null
    field_name_arr = [
        'status'
        ,'phasing'
        ,'usage'
        ,'length'
        ,'label'
        ,'dat_qty_cl'
        ,'device_id'
        ,'db_oper'
        ]
    
    for field_name in field_name_arr: 
        if lv_ug_flag:
            arr_lv_ug = lv_ug_field_not_null(field_name)
            for device_id in arr_lv_ug:
                e_msg += lv_ug_field_not_null_message(device_id, field_name)
                lv_ug_error += 1
                total_error += 1

    # check for ENUM values
    field_name_arr = [
        'status'
        ,'phasing'
        ,'usage'
        ,'label'
        ,'dat_qty_cl'
        ,'db_oper'
        ]
    
    for field_name in field_name_arr:           
        if lv_ug_flag:
            arr_lv_ug = lv_ug_field_enum(field_name)
            for device_id in arr_lv_ug:
                e_msg += lv_ug_field_enum_message(device_id, field_name)
                lv_ug_error += 1
                total_error += 1

    # check for incoming lv ug vs in_lvdb_id
    if lv_ug_flag:
        arr_lv_ug = lv_ug_lv_db_in()
        for device_id in arr_lv_ug:
            e_msg += lv_ug_lv_db_in_message(device_id)
            lv_ug_error += 1
            total_error += 1

    # check for outgoing lv ug vs out_lvdb_id
    if lv_ug_flag:
        arr_lv_ug = lv_ug_lv_db_out()
        for device_id in arr_lv_ug:
            e_msg += lvug_lvdb_out_message(device_id)
            total_error += 1

    # check for LVDB in out VS LVDB no
    if lv_ug_flag:
        arr_lv_ug = lv_ug_lvdb_id_in_check()
        for device_id in arr_lv_ug:
            e_msg += lv_ug_lvdb_id_check_message(device_id)
            lv_ug_error += 1
            total_error += 1

    if lv_ug_flag:
        arr_lv_ug = lv_ug_lvdb_id_out_check()
        for device_id in arr_lv_ug:
            e_msg += lv_ug_lvdb_id_check_message(device_id)
            total_error += 1

    if lv_ug_flag:
        arr_lv_ug = lv_ug_lvdb_no_in_check()
        for device_id in arr_lv_ug:
            e_msg += lv_ug_lvdb_no_check_message(device_id)
            lv_ug_error += 1
            total_error += 1

    if lv_ug_flag:
        arr_lv_ug = lv_ug_lvdb_no_out_check()
        for device_id in arr_lv_ug:
            e_msg += lv_ug_lvdb_no_check_message(device_id)
            lv_ug_error += 1
            total_error += 1

    # check for LV UG length
    if lv_ug_flag:
        arr_lv_ug = lv_ug_length_check()
        for device_id in arr_lv_ug:
            e_msg += lv_ug_length_check_message(device_id)
            lv_ug_error += 1
            total_error += 1

    # check for self intersect geometry
    if lv_ug_flag:
        arr_lv_ug = lv_ug_self_intersect()
        for device_id in arr_lv_ug:
            e_msg += lv_ug_self_intersect_message(device_id)
            lv_ug_error += 1
            total_error += 1

    # check for distance between 2nd vertex to LVDB-FP
    if lv_ug_flag:
        arr_lv_ug = lv_ug_1_2_incoming()
        for device_id in arr_lv_ug:
            e_msg += lv_ug_1_2_incoming_message(device_id)
            lv_ug_error += 1
            total_error += 1

    if lv_ug_flag:
        arr_lv_ug = lv_ug_1_2_outgoing()
        for device_id in arr_lv_ug:
            e_msg += lv_ug_1_2_outgoing_message(device_id)
            lv_ug_error += 1
            total_error += 1

    # check for LV UG hanging
    if lv_ug_flag:
        arr_lv_ug = lv_ug_hanging()
        for device_id in arr_lv_ug:
            e_msg += lv_ug_hanging_message(device_id)
            lv_ug_error += 1
            total_error += 1

    # check for coincidence geometry
    if lv_ug_flag:
        arr_lv_ug = lv_ug_coin()
        for device_id in arr_lv_ug:
            e_msg += lv_ug_self_intersect_message(device_id)
            lv_ug_error += 1
            total_error += 1

    #****************************************************************
    #***************     LV OH COND VALIDATION     ******************
    #****************************************************************

    arr_lv_oh = []
    
    # check z-m shapefile
    if lv_oh_flag:
        arr_lv_oh = lv_oh_z_m_shapefile()
        for device_id in arr_lv_oh:
            e_msg += lv_oh_z_m_shapefile_message(device_id)
            lv_oh_error += 1
            total_error += 1

    # check for duplicates
    if lv_oh_flag:
        arr_lv_oh = lv_oh_duplicate()
        for device_id in arr_lv_oh:
            e_msg += lv_oh_duplicate_message(device_id)
            lv_oh_error += 1
            total_error += 1

    # check for device_id format
    if lv_oh_flag:
        arr_lv_oh = lv_oh_device_id_format()
        for device_id in arr_lv_oh:
            e_msg += lv_oh_device_id_format_message(device_id)
            lv_oh_error += 1
            total_error += 1

    # check for mandatory not null
    field_name_arr = [
        'status'
        ,'phasing'
        ,'usage'
        ,'label'
        ,'length'
        ,'device_id'
        ,'db_oper'
        ]
    
    for field_name in field_name_arr: 
        if lv_oh_flag:
            arr_lv_oh = lv_oh_field_not_null(field_name)
            for device_id in arr_lv_oh:
                e_msg += lv_oh_field_not_null_message(device_id, field_name)
                lv_oh_error += 1
                total_error += 1

    # check for ENUM values
    field_name_arr = [
        'status'
        ,'phasing'
        ,'usage'
        ,'label'
        ,'db_oper'
        ]
    
    for field_name in field_name_arr: 
        if lv_oh_flag:
            arr_lv_oh = lv_oh_field_enum(field_name)
            for device_id in arr_lv_oh:
                e_msg += lv_oh_field_enum_message(device_id, field_name)
                lv_oh_error += 1
                total_error += 1

    
    # check for LV OH length
    if lv_oh_flag:
        arr_lv_oh = lv_oh_length_check()
        for device_id in arr_lv_oh:
            e_msg += lv_oh_length_check_message(device_id)
            lv_oh_error += 1
            total_error += 1

    # check LV OH self intersect
    if lv_oh_flag:
        arr_lv_oh = lv_oh_self_intersect()
        for device_id in arr_lv_oh:
            e_msg += lv_oh_self_intersect_message(device_id)
            lv_oh_error += 1
            total_error += 1

    # check LV OH hanging
    if lv_oh_flag:
        arr_lv_oh = lv_oh_hanging()
        for device_id in arr_lv_oh:
            e_msg += lv_oh_hanging_message(device_id)
            lv_oh_error += 1
            total_error += 1

    #*************************************************************
    #***************     LV Fuse VALIDATION     ******************
    #*************************************************************

    arr_lv_fuse = []

    # check for z-m value
    if lv_fuse_flag:
        arr_lv_fuse = lv_fuse_z_m_shapefile()
        for device_id in arr_lv_fuse:
            e_msg += lv_fuse_z_m_shapefile_message(device_id)
            lv_fuse_error += 1
            total_error += 1

    # check for duplicates
    if lv_fuse_flag:
        arr_lv_fuse = lv_fuse_duplicate()
        for device_id in arr_lv_fuse:
            e_msg += lv_fuse_duplicate_message(device_id)
            lv_fuse_error += 1
            total_error += 1

    # check for device_id format
    if lv_fuse_flag:
        arr_lv_fuse = lv_fuse_device_id_format()
        for device_id in arr_lv_fuse:
            e_msg += lv_fuse_device_id_format_message(device_id)
            lv_fuse_error += 1
            total_error += 1

    # check for mandatory not null
    field_name_arr = [
        'status'
        ,'phasing'
        ,'class'
        ,'normal_sta'
        ,'device_id'            
        ,'db_oper'
        ]

    if lv_fuse_flag:
        for field_name in field_name_arr:             
            arr_lv_fuse = lv_fuse_field_not_null(field_name)
            for device_id in arr_lv_fuse:
                e_msg += lv_fuse_field_not_null_message(device_id, field_name)
                lv_fuse_error += 1
                total_error += 1
                
    # check for ENUM values
    field_name_arr = [
        'status'
        ,'phasing'
        ,'class'
        ,'normal_sta'
        ,'db_oper'
        ]
     
    if lv_fuse_flag:
        for field_name in field_name_arr:            
            arr_lv_fuse = lv_fuse_field_enum(field_name)
            for device_id in arr_lv_fuse:
                e_msg += lv_fuse_field_enum_message(device_id, field_name)
                lv_fuse_error += 1
                total_error += 1

    # check for nearby Pole
    if lv_fuse_flag:
        arr_lv_fuse = lv_fuse_pole_distance()
        for device_id in arr_lv_fuse:
            e_msg += lv_fuse_pole_distance_message(device_id)
            lv_fuse_error += 1
            total_error += 1

    # check for LV Fuse(Blackbox) Snapping Error
    if lv_fuse_flag:
        arr_lv_fuse = lv_fuse_snapping()
        for device_id in arr_lv_fuse:
            e_msg += lv_fuse_snapping_message(device_id)
            lv_fuse_error += 1
            total_error += 1

    #***************************************************************
    #**************    LV Cable Joint VALIDATION     ***************
    #***************************************************************

    arr_lv_cj = []

    # check for z-m value
    if lv_cj_flag:
        arr_lv_cj = lv_cj_z_m_shapefile()
        for device_id in arr_lv_cj:
            e_msg += lv_cj_z_m_shapefile_message(device_id)
            lv_cj_error += 1
            total_error += 1

    # check for duplicates
    if lv_cj_flag:
        arr_lv_cj = lv_cj_duplicate()
        for device_id in arr_lv_cj:
            e_msg += lv_cj_duplicate_message(device_id)
            lv_cj_error += 1
            total_error += 1

    # check for device_id format
    if lv_cj_flag:
        arr_cj_oh = lv_cj_device_id_format()
        for device_id in arr_lv_cj:
            e_msg += lv_cj_device_id_format_message(device_id)
            lv_oh_error += 1
            total_error += 1

    # check for mandatory not null
    field_name_arr = [
        'status'
        ,'class'
        ,'type'
        ,'db_oper'
        ,'device_id'
        ]
    
    if lv_cj_flag:
        for field_name in field_name_arr:             
            arr_lv_cj = lv_cj_field_not_null(field_name)
            for device_id in arr_lv_cj:
                e_msg += lv_cj_field_not_null_message(device_id, field_name)
                lv_cj_error += 1
                total_error += 1

    # check for ENUM values
    field_name_arr = [
        'status'
        ,'class'
        ,'type'
        ,'db_oper'
        ]

    if lv_cj_flag:
        for field_name in field_name_arr:             
            arr_lv_cj = lv_cj_field_enum(field_name)
            for device_id in arr_lv_cj:
                e_msg += lv_cj_field_enum_message(device_id, field_name)
                lv_cj_error += 1
                total_error += 1

    # check for snapping with LV OH/LV UG
    if lv_cj_flag:
        arr_lv_cj = lv_cj_snapping()
        for device_id in arr_lv_cj:
            e_msg += lv_cj_snapping_message(device_id)
            lv_cj_error += 1
            total_error += 1
    

    #***************************************************************
    #******************    LVDB-FP VALIDATION     ******************
    #***************************************************************

    arr_lvdb_fp = []

    # check for z-m value
    if lvdb_fp_flag:
        arr_lvdb_fp = lvdb_fp_z_m_shapefile()
        for device_id in arr_lvdb_fp:
            e_msg += lvdb_fp_z_m_shapefile_message(device_id)
            lvdb_fp_error += 1
            total_error += 1

    # check for duplicates
    if lvdb_fp_flag:
        arr_lvdb_fp = lvdb_fp_duplicate()
        for device_id in arr_lvdb_fp:
            e_msg += lvdb_fp_duplicate_message(device_id)
            lvdb_fp_error += 1
            total_error += 1

    # check for device_id format
    if lvdb_fp_flag:
        arr_lvdb_fp = lvdb_fp_device_id_format()
        for device_id in arr_lvdb_fp:
            e_msg += lvdb_fp_device_id_format_message(device_id)
            lvdb_fp_error += 1
            total_error += 1

    # check for mandatory not null
    field_name_arr = [
        'status'
        ,'lvdb_loc'
        ,'design'
        ,'device_id'
        ,'db_oper'
        ,'lvdb_angle'
        ]

    for field_name in field_name_arr: 
        if lvdb_fp_flag:
            arr_lvdb_fp = lvdb_fp_field_not_null(field_name)
            for device_id in arr_lvdb_fp:
                e_msg += lvdb_fp_field_not_null_message(device_id, field_name)
                lvdb_fp_error += 1
                total_error += 1

    # check for ENUM values
    field_name_arr = [
        'status'
        ,'lvdb_loc'
        ,'design'
        ,'db_oper'
        ]
        
    for field_name in field_name_arr:    
        if lvdb_fp_flag:
            arr_lvdb_fp = lvdb_fp_field_enum(field_name)
            for device_id in arr_lvdb_fp:
                e_msg += lvdb_fp_field_enum_message(device_id, field_name)
                lvdb_fp_error += 1
                total_error += 1

    # check for remarks/db_oper mismatch
    if lvdb_fp_flag:
        arr_lvdb_fp = lvdb_fp_remarks_db_oper()
        for device_id in arr_lvdb_fp:
            e_msg += lvdb_fp_remarks_db_oper_message(device_id)
            lvdb_fp_error += 1
            total_error += 1

    # check for lvf/design mismatch
    if lvdb_fp_flag:
        arr_lvdb_fp = lvdb_fp_lvf_design()
        for device_id in arr_lvdb_fp:
            e_msg += lvdb_fp_lvf_design_message(device_id)
            lvdb_fp_error += 1
            total_error += 1

    # check for lvdb-fp hanging/snapping
    if lvdb_fp_flag:
        arr_lvdb_fp = lvdb_fp_snapping()
        for device_id in arr_lvdb_fp:
            e_msg += lvdb_fp_snapping_message(device_id)
            lvdb_fp_error += 1
            total_error += 1

    #***************************************************************
    #********************    POLE VALIDATION     *******************
    #***************************************************************

    arr_pole = []

    # check for z-m value
    if pole_flag:
        arr_pole = pole_z_m_shapefile()
        for device_id in arr_pole:
            e_msg += pole_z_m_shapefile_message(device_id)
            pole_error += 1
            total_error += 1

    # check for duplicates
    if pole_flag:
        arr_pole = pole_duplicate()
        for device_id in arr_pole:
            e_msg += pole_duplicate_message(device_id)
            pole_error += 1
            total_error += 1

    # check for device_id format
    if pole_flag:
        arr_pole = pole_device_id_format()
        for device_id in arr_pole:
            e_msg += pole_device_id_format_message(device_id)
            pole_error += 1
            total_error += 1

    # check for mandatory not null
    field_name_arr = [
        'status'
        ,'light_ares'
        ,'struc_type'
        ,'pole_no'
        ,'device_id'
        ,'db_oper'
        ,'lv_ptc'
        ]

    for field_name in field_name_arr: 
        if pole_flag:
            arr_pole = pole_field_not_null(field_name)
        for device_id in arr_pole:
            e_msg += pole_field_not_null_message(device_id, field_name)
            pole_error += 1
            total_error += 1

    # check for ENUM values
    field_name_arr = [
        'status'
        ,'light_ares'
        ,'struc_type'
        ,'db_oper'
        ,'lv_ptc'
        ]
        
    for field_name in field_name_arr:    
        if pole_flag:
            arr_pole = pole_field_enum(field_name)
            for device_id in arr_pole:
                e_msg += pole_field_enum_message(device_id, field_name)
                pole_error += 1
                total_error += 1

    # check for Pole/LV OH vertex
    if pole_flag:
        arr_pole = pole_lv_oh_vertex()
        for device_id in arr_pole:
            e_msg += pole_lv_oh_vertex_message(device_id)
            pole_error += 1
            total_error += 1

    #***************************************************************
    #***************    DEMAND POINT VALIDATION     ****************
    #***************************************************************

    arr_dmd_pt = []

    # check z-m shapefile
    if dmd_pt_flag:
        arr_dmd_pt = dmd_pt_z_m_shapefile()
        for device_id in arr_dmd_pt:
            e_msg += dmd_pt_z_m_shapefile_message(device_id)
            dmd_pt_error += 1
            total_error += 1

    # check for duplicates
    if dmd_pt_flag:
        arr_dmd_pt = dmd_pt_duplicate()
        for device_id in arr_dmd_pt:
            e_msg += dmd_pt_duplicate_message(device_id)
            dmd_pt_error += 1
            total_error += 1

    # check for device_id format
    if dmd_pt_flag:
        arr_dmd_pt = dmd_pt_device_id_format()
        for device_id in arr_dmd_pt:
            e_msg += dmd_pt_device_id_format_message(device_id)
            dmd_pt_error += 1
            total_error += 1

    # check for mandatory not null
    field_name_arr = [
        'status'
        ,'device_id'
        ,'db_oper'
        ,'dist_tranx'
        ,'house_no'
        ,'str_name'
        ]

    for field_name in field_name_arr: 
        if dmd_pt_flag:
            arr_dmd_pt = dmd_pt_field_not_null(field_name)
            for device_id in arr_dmd_pt:
                e_msg += dmd_pt_field_not_null_message(device_id, field_name)
                dmd_pt_error += 1
                total_error += 1

    # check for ENUM values
    field_name_arr = [
        'status'         
        ,'db_oper'
        ]
        
    for field_name in field_name_arr:    
        if dmd_pt_flag:
            arr_dmd_pt = dmd_pt_field_enum(field_name)
            for device_id in arr_dmd_pt:
                e_msg += dmd_pt_field_enum_message(device_id, field_name)
                dmd_pt_error += 1
                total_error += 1

    # check for Remarks
    if dmd_pt_flag:
        arr_dmd_pt = dmd_pt_remarks()
        for device_id in arr_dmd_pt:
            e_msg += dmd_pt_remarks_message(device_id)
            dmd_pt_error += 1
            total_error += 1

    # check for demand point snapping
    if dmd_pt_flag:
        arr_dmd_pt = dmd_pt_snapping()
        for device_id in arr_dmd_pt:
            e_msg += dmd_pt_snapping_message(device_id)
            dmd_pt_error += 1
            total_error += 1

    #***************************************************************
    #***************    STREET LIGHT VALIDATION     ****************
    #***************************************************************

    arr_st_light = []

    # check for duplicates
    if st_light_flag:
        arr_st_light = st_light_z_m_shapefile()
        for device_id in arr_st_light:
            e_msg += st_light_z_m_shapefile_message(device_id)
            st_light_error += 1
            total_error += 1

    # check for duplicates
    if st_light_flag:
        arr_st_light = st_light_duplicate()
        for device_id in arr_st_light:
            e_msg += st_light_duplicate_message(device_id)
            st_light_error += 1
            total_error += 1

    # check for device_id format
    if st_light_flag:
        arr_st_light = st_light_device_id_format()
        for device_id in arr_st_light:
            e_msg += st_light_device_id_format_message(device_id)
            st_light_error += 1
            total_error += 1

    # check for mandatory not null
    field_name_arr = [
        'status'
        ,'phasing'
        ,'db_oper'
        ,'stl_angle'
        ,'cont_dev'
        ,'device_id'
        ]

    for field_name in field_name_arr: 
        if st_light_flag:
            arr_st_light = st_light_field_not_null(field_name)
            for device_id in arr_st_light:
                e_msg += st_light_field_not_null_message(device_id, field_name)
                st_light_error += 1
                total_error += 1

    
    # check for ENUM values
    field_name_arr = [
        'status'
        ,'db_oper'
        ,'cont_dev'
        ]
        
    for field_name in field_name_arr:    
        if st_light_flag:
            arr_st_light = st_light_field_enum(field_name)
            for device_id in arr_st_light:
                e_msg += st_light_field_enum_message(device_id, field_name)
                st_light_error += 1
                total_error += 1

    # check for phasing must be 'R'   
    if st_light_flag:
        arr_st_light = st_light_phasing()
        for device_id in arr_st_light:
            e_msg += st_light_phasing_message(device_id)
            st_light_error += 1
            total_error += 1

    # check for Control Device
    if st_light_flag:
        arr_st_light = st_light_cont_dev()
        for device_id in arr_st_light:
            e_msg += st_light_cont_dev_message(device_id)
            st_light_error += 1
            total_error += 1

    # Geom check: Street Light overlap Pole
    if st_light_flag:
        arr_st_light = st_light_overlap_pole()
        for device_id in arr_st_light:
            e_msg += st_light_overlap_pole_message(device_id)
            st_light_error += 1
            total_error += 1

    #***************************************************************
    #******************    MANHOLE VALIDATION     ******************
    #***************************************************************

    arr_manhole = []

    #check for z-m value
    if manhole_flag:
        arr_manhole = manhole_z_m_shapefile()
        for device_id in arr_manhole:
            e_msg += manhole_z_m_shapefile_message(device_id)
            manhole_error += 1
            total_error += 1

    #check for duplicate
    if manhole_flag:
        arr_manhole = manhole_duplicate()
        for device_id in arr_manhole:
            e_msg += manhole_duplicate_message(device_id)
            manhole_error += 1
            total_error += 1

    # check for device_id format
    if manhole_flag:
        arr_manhole = manhole_device_id_format()
        for device_id in arr_manhole:
            e_msg += manhole_device_id_format_message(device_id)
            manhole_error += 1
            total_error += 1

    # check for mandatory not null
    field_name_arr = [
        'status'
        ,'phasing'
        ,'db_oper'
        ,'stl_angle'
        ,'cont_dev'
        ,'device_id'
        ]

    for field_name in field_name_arr: 
        if manhole_flag:
            arr_manhole = manhole_field_not_null(field_name)
            for device_id in arr_manhole:
                e_msg += manhole_field_not_null_message(device_id, field_name)
                manhole_error += 1
                total_error += 1

    # check for ENUM values
    field_name_arr = [
        'status'
        ,'phasing'
        ,'db_oper'
        ,'cont_dev'
        ]
        
    for field_name in field_name_arr:    
        if manhole_flag:
            arr_manhole = manhole_field_enum(field_name)
            for device_id in arr_manhole:
                e_msg += manhole_field_enum_message(device_id, field_name)
                manhole_error += 1
                total_error += 1

    #***************************************************************
    #***************     STRUCTURE DUCT VALIDATION     *************
    #***************************************************************

    arr_st_duct = []
    
    # check for duplicates
    if st_duct_flag:
        arr_st_duct = st_duct_duplicate()
        for device_id in arr_st_duct:
            e_msg += st_duct_duplicate_message(device_id)
            st_duct_error += 1
            total_error += 1

    # check for device_id format
    if st_duct_flag:
        arr_st_duct = st_duct_device_id_format()
        for device_id in arr_st_duct:
            e_msg += st_duct_device_id_format_message(device_id)
            st_duct_error += 1
            total_error += 1

    # check for mandatory not null
    field_name_arr = [
        'status'
        ,'size'
        ,'method'
        ,'way'
        ,'device_id'
        ,'db_oper'
        ]

    for field_name in field_name_arr: 
        if st_duct_flag:
            arr_st_duct = st_duct_field_not_null(field_name)
            for device_id in arr_st_duct:
                e_msg += st_duct_field_not_null_message(device_id, field_name)
                arr_st_duct_error += 1
                total_error += 1

    # check for ENUM values
    field_name_arr = [
        'status'
        ,'size'
        ,'method'
        ,'way'
        ,'db_oper'
        ]
        
    for field_name in field_name_arr:    
        if st_duct_flag:
            arr_st_duct = st_light_field_enum(field_name)
        for device_id in arr_st_duct:
            e_msg += st_duct_field_enum_message(device_id, field_name)
            st_duct_error += 1
            total_error += 1
    
    #****************************************************************
    #******************     END OF VALIDATION     *******************
    #****************************************************************
            
    #change label in GUI
    if lv_ug_flag == False:
        lv_ug_error = 'Skipped'
    if lv_oh_flag == False:
        lv_oh_error = 'Skipped'
    if lv_fuse_flag == False:
        lv_fuse_error = 'Skipped'
    if lv_cj_flag == False:
        lv_cj_error = 'Skipped'
    if lvdb_fp_flag == False:
        lvdb_fp_error = 'Skipped'
    if pole_flag == False:
        pole_error = 'Skipped'
    if dmd_pt_flag == False:
        dmd_pt_error = 'Skipped'
    if st_light_flag == False:
        st_light_error = 'Skipped'
    if manhole_flag == False:
        manhole_error = 'Skipped'
    if st_duct_flag == False:
        st_duct_error = 'Skipped'
        
    self.dlg.label_message.setText(' ')

    # update error count label
    self.dlg.err_lvug.setText(str(lv_ug_error))
    self.dlg.err_lvoh.setText(str(lv_oh_error))
    self.dlg.err_lv_fuse.setText(str(lv_fuse_error))
    self.dlg.err_lv_cj.setText(str(lv_cj_error))
    self.dlg.err_lvdb_fp.setText(str(lvdb_fp_error))
    self.dlg.err_pole.setText(str(pole_error))
    self.dlg.err_dmd_pt.setText(str(dmd_pt_error))
    self.dlg.err_st_light.setText(str(st_light_error))
    self.dlg.err_manhole.setText(str(manhole_error))
    self.dlg.err_st_duct.setText(str(st_duct_error))
    # update total
    self.dlg.err_total.setText(str(total_error))

    #****************************************************************
    #******************     WRITE TO CSV FILE     *******************
    #****************************************************************

    # write to csv file
    filename = self.dlg.lineEdit_csv.text()
    # if output to csv file, will not print to console.
    # print to console only if no csv filename is specified
    if len(filename) > 4:
        with open(filename, 'w') as output_file:
            output_file.write(e_msg)
        self.iface.messageBar().pushMessage(
              "Success", "Output file written at " + filename,
              level=Qgis.Success, duration=3)
    else:
        print(e_msg)
        print('total Error(s):', str(total_error))
        self.iface.messageBar().pushMessage(
              "Success", "Validation completed. " + str(total_error) + " ERROR(s) found.",
              level=Qgis.Success, duration=3)
    return 0

def exec_clear_errors(self):
    #start total_error count
    lv_ug_error = 0
    lv_oh_error = 0
    lv_fuse_error = 0
    lv_cj_error = 0
    lvdb_fp_error = 0
    pole_error = 0
    dmd_pt_error = 0
    st_light_error = 0
    manhole_error = 0
    st_duct_error = 0
    total_error = 0
    
    # update error count label
    self.dlg.err_lvug.setText(str(lv_ug_error))
    self.dlg.err_lvoh.setText(str(lv_oh_error))
    self.dlg.err_lv_fuse.setText(str(lv_fuse_error))
    self.dlg.err_lv_cj.setText(str(lv_cj_error))
    self.dlg.err_lvdb_fp.setText(str(lvdb_fp_error))
    self.dlg.err_pole.setText(str(pole_error))
    self.dlg.err_dmd_pt.setText(str(dmd_pt_error))
    self.dlg.err_st_light.setText(str(st_light_error))
    self.dlg.err_manhole.setText(str(manhole_error))
    self.dlg.err_st_duct.setText(str(st_duct_error))
    # update total
    self.dlg.err_total.setText(str(total_error))
    return 0

