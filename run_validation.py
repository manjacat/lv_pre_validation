# -*- coding: utf-8 -*-
"""
/***************************************************************************
 seperating main button with GUI code

 Changelog
 ---------
 18/5/2020: require geometry checks for LV OH/LV UG to prevent it throws error in other checks (demand point, lvdb, pole etc)
 27/5/2020: allow 'N/A' for [pole number] column
 4/6/2020: seperate device id error as seperate checks
 11/6/2020: added device_id.strip() to remove carriage return (/r/n) in device_id
 11/6/2020: added try/catch for all object when checking for device id format error
 18/6/2020: added param to lv_ug_self_intersect_message and lv_oh_self_intersect_message
            changed try-except clause to try-except Exception as e
 22/6/2020: added customer.py validation
 
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
# import own custom python file
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
from .customer import *
from .feature_count import count_lv_features


def exec_validation(self):
    # test calling from new python file
    # print('Hello from new python file')

    # count features
    count_lv_features(self)

    # *****************************************************
    # ***********     INITIALIZE VARIABLE    **************
    # *****************************************************

    # start total_error count
    device_id_error = 0
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
    customer_error = 0
    total_error = 0

    # error message
    e_msg = ''

    # col flag
    lv_ug_check_flag = False
    lv_oh_check_flag = False
    lv_fuse_check_flag = False
    lv_cj_check_flag = False
    lvdb_fp_check_flag = False
    pole_check_flag = False
    dmd_pt_check_flag = False
    st_light_check_flag = False
    manhole_check_flag = False
    st_duct_check_flag = False
    customer_check_flag = False

    # error geom
    arr_lv_ug_exclude_geom = []
    arr_lv_oh_exclude_geom = []

    # ****************************************************
    # ***********     KHAIRIL TESTING STUFF    ***********
    # ****************************************************

    # future testing area

    # ***************************************************************
    # ***********     CHECK HOW MANY FEATURES SELECTED    ***********
    # ***************************************************************

    # init flags
    device_id_flag = self.dlg.checkBox_device_id.isChecked()
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
    customer_flag = self.dlg.checkBox_customer.isChecked()

    feat_count = 0
    arr_feat_count = []
    if self.dlg.checkBox_device_id.isChecked():
        arr_feat_count.append('Device_Id')
        feat_count += 1
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
    if self.dlg.checkBox_customer.isChecked():
        arr_feat_count.append('Customer')
        feat_count += 1

    qa_qc_msg = 'No features selected fo QA/QC validation.'
    if feat_count > 0:
        qa_qc_msg = ' '.join(['running QA/QC now on ', str(feat_count), 'features:'])
    print(qa_qc_msg)
    if len(arr_feat_count) > 0:
        print(arr_feat_count)

    # ******************************************************
    # ******     MANDATORY COLUMN/FIELD CHECKING    ********
    # ******************************************************

    if lv_ug_flag:
        arr_lv_ug = rps_column_name_check('LV_UG_Conductor')
        # check missing layers
        lv_ug_layer_name = 'LV_UG_Conductor'
        arr_layers = rps_get_arr_layers(lv_ug_layer_name)
        arr_missing_layer = rps_check_layer_name(arr_layers)

        if len(arr_missing_layer) > 0:
            for missing_layer in arr_missing_layer:
                e_msg += rps_check_layer_name_message(lv_ug_layer_name, missing_layer)
                lv_ug_error += 1
                total_error += 1
        else:
            # check missing columns
            arr_missing_columns = rps_column_name_check(lv_ug_layer_name)
            if len(arr_missing_columns) > 0:
                for col_miss in arr_missing_columns:
                    e_msg += rps_column_name_check_message(lv_ug_layer_name, col_miss)
                    lv_ug_error += 1
                    total_error += 1
            else:
                lv_ug_check_flag = True
                # lv_oh_check_flag = True

    if lv_oh_flag:
        # check missing layers
        lv_oh_layer_name = 'LV_OH_Conductor'
        arr_layers = rps_get_arr_layers(lv_oh_layer_name)
        arr_missing_layer = rps_check_layer_name(arr_layers)

        if len(arr_missing_layer) > 0:
            for missing_layer in arr_missing_layer:
                e_msg += rps_check_layer_name_message(lv_oh_layer_name, missing_layer)
                lv_oh_error += 1
                total_error += 1
        else:
            # check missing columns
            arr_missing_columns = rps_column_name_check(lv_oh_layer_name)
            if len(arr_missing_columns) > 0:
                for col_miss in arr_missing_columns:
                    e_msg += rps_column_name_check_message(lv_oh_layer_name, col_miss)
                    lv_oh_error += 1
                    total_error += 1
            else:
                # lv_ug_check_flag = True
                lv_oh_check_flag = True

    if lv_fuse_flag:
        # check missing layers
        lv_fuse_layer_name = 'LV_Fuse'
        arr_layers = rps_get_arr_layers(lv_fuse_layer_name)
        arr_missing_layer = rps_check_layer_name(arr_layers)

        if len(arr_missing_layer) > 0:
            for missing_layer in arr_missing_layer:
                e_msg += rps_check_layer_name_message(lv_fuse_layer_name, missing_layer)
                lv_fuse_error += 1
                total_error += 1
        else:
            # check missing columns
            arr_missing_columns = rps_column_name_check(lv_fuse_layer_name)
            if len(arr_missing_columns) > 0:
                for col_miss in arr_missing_columns:
                    e_msg += rps_column_name_check_message(lv_fuse_layer_name, col_miss)
                    lv_fuse_error += 1
                    total_error += 1
            else:
                lv_fuse_check_flag = True
                # lv_oh_check_flag = True

    if lv_cj_flag:
        # check missing layers
        lv_cj_layer_name = 'LV_Fuse'
        arr_layers = rps_get_arr_layers(lv_cj_layer_name)
        arr_missing_layer = rps_check_layer_name(arr_layers)

        if len(arr_missing_layer) > 0:
            for missing_layer in arr_missing_layer:
                e_msg += rps_check_layer_name_message(lv_cj_layer_name, missing_layer)
                lv_cj_error += 1
                total_error += 1
        else:
            # check missing columns
            arr_missing_columns = rps_column_name_check(lv_cj_layer_name)
            if len(arr_missing_columns) > 0:
                for col_miss in arr_missing_columns:
                    e_msg += rps_column_name_check_message(lv_cj_layer_name, col_miss)
                    lv_cj_error += 1
                    total_error += 1
            else:
                lv_cj_check_flag = True
                # lv_ug_check_flag = True
                # lv_oh_check_flag = True

    if lvdb_fp_flag:
        # check missing layers
        lvdb_fp_layer_name = 'LVDB-FP'
        arr_layers = rps_get_arr_layers(lvdb_fp_layer_name)
        arr_missing_layer = rps_check_layer_name(arr_layers)

        if len(arr_missing_layer) > 0:
            for missing_layer in arr_missing_layer:
                e_msg += rps_check_layer_name_message(lvdb_fp_layer_name, missing_layer)
                lvdb_fp_error += 1
                total_error += 1
        else:
            # check missing columns
            arr_missing_columns = rps_column_name_check(lvdb_fp_layer_name)
            if len(arr_missing_columns) > 0:
                for col_miss in arr_missing_columns:
                    e_msg += rps_column_name_check_message(lvdb_fp_layer_name, col_miss)
                    lvdb_fp_error += 1
                    total_error += 1
            else:
                lvdb_fp_check_flag = True
                # lv_ug_check_flag = True
                # lv_oh_check_flag = True

    if pole_flag:
        # check missing layers
        pole_layer_name = 'Pole'
        arr_layers = rps_get_arr_layers(pole_layer_name)
        arr_missing_layer = rps_check_layer_name(arr_layers)

        if len(arr_missing_layer) > 0:
            for missing_layer in arr_missing_layer:
                e_msg += rps_check_layer_name_message(pole_layer_name, missing_layer)
                pole_error += 1
                total_error += 1
        else:
            # check missing columns
            arr_missing_columns = rps_column_name_check(pole_layer_name)
            if len(arr_missing_columns) > 0:
                for col_miss in arr_missing_columns:
                    e_msg += rps_column_name_check_message(pole_layer_name, col_miss)
                    pole_error += 1
                    total_error += 1
            else:
                pole_check_flag = True
                # lv_oh_check_flag = True

    if dmd_pt_flag:
        # check missing layers
        dmd_pt_layer_name = 'Demand_Point'
        arr_layers = rps_get_arr_layers(dmd_pt_layer_name)
        arr_missing_layer = rps_check_layer_name(arr_layers)

        if len(arr_missing_layer) > 0:
            for missing_layer in arr_missing_layer:
                e_msg += rps_check_layer_name_message(dmd_pt_layer_name, missing_layer)
                dmd_pt_error += 1
                total_error += 1
        else:
            # check missing columns
            arr_missing_columns = rps_column_name_check(dmd_pt_layer_name)
            if len(arr_missing_columns) > 0:
                for col_miss in arr_missing_columns:
                    e_msg += rps_column_name_check_message(dmd_pt_layer_name, col_miss)
                    dmd_pt_error += 1
                    total_error += 1
            else:
                dmd_pt_check_flag = True
                # lv_ug_check_flag = True
                # lv_oh_check_flag = True

    if st_light_flag:
        # check missing layers
        st_light_layer_name = 'Street_Light'
        arr_layers = rps_get_arr_layers(st_light_layer_name)
        arr_missing_layer = rps_check_layer_name(arr_layers)

        if len(arr_missing_layer) > 0:
            for missing_layer in arr_missing_layer:
                e_msg += rps_check_layer_name_message(st_light_layer_name, missing_layer)
                st_light_error += 1
                total_error += 1
        else:
            # check missing columns
            arr_missing_columns = rps_column_name_check(st_light_layer_name)
            if len(arr_missing_columns) > 0:
                for col_miss in arr_missing_columns:
                    e_msg += rps_column_name_check_message(st_light_layer_name, col_miss)
                    st_light_error += 1
                    total_error += 1
            else:
                st_light_check_flag = True
                # pole_check_flag = True

    if customer_flag:
        # check missing layer
        customer_layer_name = 'Customer'
        arr_layers = rps_get_arr_layers(customer_layer_name)
        arr_missing_layer = rps_check_layer_name(arr_layers)

        if len(arr_missing_layer) > 0:
            for missing_layer in arr_missing_layer:
                e_msg += rps_check_layer_name_message(customer_layer_name, missing_layer)
                customer_error += 1
                total_error += 1
        else:
            # check missing columns
            arr_missing_columns = rps_column_name_check(customer_layer_name)
            if len(arr_missing_columns) > 0:
                for col_miss in arr_missing_columns:
                    e_msg += rps_column_name_check_message(customer_layer_name, col_miss)
                    customer_error += 1
                    total_error += 1
            else:
                customer_check_flag = True
                # dmd_pt_check_flag = True

    # ******************************************************
    # **********     DEVICE ID CHECKING    *****************
    # ******************************************************

    # print('current total (device_id): ' + str(total_error))

    arr_device_id_err = []

    # check for device_id format
    if device_id_flag:
        try:
            arr_device_id_err = lv_ug_device_id_format()
            for device_id in arr_device_id_err:
                if device_id:
                    device_id = device_id.strip()
                e_msg += lv_ug_device_id_format_message(device_id)
                device_id_error += 1
                total_error += 1
        except Exception as e:
            print('lv ug device_id skipped')

    # check for device_id format
    if device_id_flag:
        try:
            arr_device_id_err = lv_oh_device_id_format()
            for device_id in arr_device_id_err:
                e_msg += lv_oh_device_id_format_message(device_id)
                device_id_error += 1
                total_error += 1
        except Exception as e:
            print('lv oh device id skipped:' + str(e))

    # check for device_id format
    if device_id_flag:
        try:
            arr_device_id_err = lv_fuse_device_id_format()
            for device_id in arr_device_id_err:
                if device_id:
                    device_id = device_id.strip()
                e_msg += lv_fuse_device_id_format_message(device_id)
                device_id_error += 1
                total_error += 1
        except Exception as e:
            print('lv fuse device id skipped:' + str(e))

    # check for device_id format
    if device_id_flag:
        try:
            arr_device_id_err = lv_cj_device_id_format()
            for device_id in arr_device_id_err:
                if device_id:
                    device_id = device_id.strip()
                e_msg += lv_cj_device_id_format_message(device_id)
                device_id_error += 1
                total_error += 1
        except Exception as e:
            print('lv cable joint device id skipped:' + str(e))

    # check for device_id format
    if device_id_flag:
        try:
            arr_device_id_err = lvdb_fp_device_id_format()
            for device_id in arr_device_id_err:
                if device_id:
                    device_id = device_id.strip()
                e_msg += lvdb_fp_device_id_format_message(device_id)
                device_id_error += 1
                total_error += 1
        except Exception as e:
            print('lvdb-fp device id skipped:' + str(e))

    # check for device_id format
    if device_id_flag:
        try:
            arr_device_id_err = pole_device_id_format()
            for device_id in arr_device_id_err:
                if device_id:
                    device_id = device_id.strip()
                e_msg += pole_device_id_format_message(device_id)
                device_id_error += 1
                total_error += 1
        except Exception as e:
            print('pole device_id skipped:' + str(e))

    # check for device_id format
    if device_id_flag:
        try:
            arr_device_id_err = dmd_pt_device_id_format()
            for device_id in arr_device_id_err:
                if device_id:
                    device_id = device_id.strip()
                e_msg += dmd_pt_device_id_format_message(device_id)
                device_id_error += 1
                total_error += 1
        except Exception as e:
            print('pole device_id skipped:' + str(e))

    # check for device_id format
    if device_id_flag:
        try:
            arr_device_id_err = st_light_device_id_format()
            for device_id in arr_device_id_err:
                if device_id:
                    device_id = device_id.strip()
                e_msg += st_light_device_id_format_message(device_id)
                device_id_error += 1
                total_error += 1
        except Exception as e:
            print('street light device id skipped: ' + str(e))

    # check for device_id format
    if device_id_flag:
        try:
            arr_device_id_err = manhole_device_id_format()
            for device_id in arr_device_id_err:
                if device_id:
                    device_id = device_id.strip()
                e_msg += manhole_device_id_format_message(device_id)
                device_id_error += 1
                total_error += 1
        except Exception as e:
            print('manhole device id skipped: ' + str(e))

    # check for device_id format
    if device_id_flag:
        try:
            arr_device_id_err = st_duct_device_id_format()
            for device_id in arr_device_id_err:
                if device_id:
                    device_id = device_id.strip()
                e_msg += st_duct_device_id_format_message(device_id)
                device_id_error += 1
                total_error += 1
        except Exception as e:
            print('structure duct device id skipped')

    # print('current total (end of device id): ' + str(total_error))

    # *******************************************************
    # ***************     Z M CHECKING    *******************
    # *******************************************************

    arr_lv_ug = []
    testing_flag = True

    # check z-m shapefile
    if lv_ug_check_flag or testing_flag:
        arr_lv_ug = lv_ug_z_m_shapefile()
        arr_lv_ug_exclude_geom = arr_lv_ug
        # print(len(arr_lv_ug_exclude_geom))
        for device_id in arr_lv_ug:
            if device_id:
                device_id = device_id.strip()
            e_msg += lv_ug_z_m_shapefile_message(device_id)
            lv_ug_error += 1
            total_error += 1

    arr_lv_oh = []

    # check z-m shapefile
    if lv_oh_check_flag or testing_flag:
        arr_lv_oh = lv_oh_z_m_shapefile()
        arr_lv_oh_exclude_geom = arr_lv_oh
        # print(len(arr_lv_oh_exclude_geom))
        for device_id in arr_lv_oh:
            if device_id:
                device_id = device_id.strip()
            e_msg += lv_oh_z_m_shapefile_message(device_id)
            lv_oh_error += 1
            total_error += 1

    # print('current total error is (zm check):' + str(total_error))

    # ****************************************************************
    # ***************   KHAIRIL TESTING CODE AREA    *****************
    # ****************************************************************

    # check LV OH hanging
    # if lv_oh_flag and lv_oh_check_flag:
    # arr_lv_oh = lv_oh_hanging(arr_lv_ug_exclude_geom, arr_lv_oh_exclude_geom)
    # for device_id in arr_lv_oh:
    #    if device_id:
    #        device_id = device_id.strip()
    #    e_msg += lv_oh_hanging_message(device_id)
    #    lv_oh_error += 1
    #    total_error += 1

    # ****************************************************************
    # ***************     LV UG COND VALIDATION    *******************
    # ****************************************************************

    # check for duplicates
    if lv_ug_flag and lv_ug_check_flag:
        arr_lv_ug = lv_ug_duplicate()
        for device_id in arr_lv_ug:
            if device_id:
                device_id = device_id.strip()
            e_msg += lv_ug_duplicate_message(device_id)
            lv_ug_error += 1
            total_error += 1

    # check for mandatory not null
    field_name_arr = [
        'status'
        , 'phasing'
        , 'usage'
        , 'length'
        , 'label'
        , 'dat_qty_cl'
        , 'device_id'
        , 'db_oper'
    ]

    if lv_ug_flag and lv_ug_check_flag:
        for field_name in field_name_arr:
            arr_lv_ug = lv_ug_field_not_null(field_name)
            for device_id in arr_lv_ug:
                if device_id:
                    device_id = device_id.strip()
                e_msg += lv_ug_field_not_null_message(device_id, field_name)
                lv_ug_error += 1
                total_error += 1

    # check for ENUM values
    field_name_arr = [
        'status'
        , 'phasing'
        , 'usage'
        , 'label'
        , 'dat_qty_cl'
        , 'db_oper'
    ]

    if lv_ug_flag and lv_ug_check_flag:
        for field_name in field_name_arr:
            arr_lv_ug = lv_ug_field_enum(field_name)
            for device_id in arr_lv_ug:
                if device_id:
                    device_id = device_id.strip()
                e_msg += lv_ug_field_enum_message(device_id, field_name)
                lv_ug_error += 1
                total_error += 1

    # check for incoming lv ug vs in_lvdb_id
    if lv_ug_flag and lv_ug_check_flag:
        arr_lv_ug = lv_ug_lv_db_in(arr_lv_ug_exclude_geom)
        for device_id in arr_lv_ug:
            if device_id:
                device_id = device_id.strip()
            e_msg += lv_ug_lv_db_in_message(device_id)
            lv_ug_error += 1
            total_error += 1

    # check for outgoing lv ug vs out_lvdb_id
    if lv_ug_flag and lv_ug_check_flag:
        arr_lv_ug = lv_ug_lv_db_out(arr_lv_ug_exclude_geom)
        for device_id in arr_lv_ug:
            if device_id:
                device_id = device_id.strip()
            e_msg += lvug_lvdb_out_message(device_id)
            total_error += 1

    # check for LVDB in out VS LVDB no
    if lv_ug_flag and lv_ug_check_flag:
        arr_lv_ug = lv_ug_lvdb_id_in_check()
        for device_id in arr_lv_ug:
            if device_id:
                device_id = device_id.strip()
            e_msg += lv_ug_lvdb_id_check_message(device_id)
            lv_ug_error += 1
            total_error += 1

    if lv_ug_flag and lv_ug_check_flag:
        arr_lv_ug = lv_ug_lvdb_id_out_check()
        for device_id in arr_lv_ug:
            if device_id:
                device_id = device_id.strip()
            e_msg += lv_ug_lvdb_id_check_message(device_id)
            total_error += 1

    if lv_ug_flag and lv_ug_check_flag:
        arr_lv_ug = lv_ug_lvdb_no_in_check()
        for device_id in arr_lv_ug:
            if device_id:
                device_id = device_id.strip()
            e_msg += lv_ug_lvdb_no_check_message(device_id)
            lv_ug_error += 1
            total_error += 1

    if lv_ug_flag and lv_ug_check_flag:
        arr_lv_ug = lv_ug_lvdb_no_out_check()
        for device_id in arr_lv_ug:
            if device_id:
                device_id = device_id.strip()
            e_msg += lv_ug_lvdb_no_check_message(device_id)
            lv_ug_error += 1
            total_error += 1

    # check for LV UG length
    if lv_ug_flag and lv_ug_check_flag:
        arr_lv_ug = lv_ug_length_check()
        for device_id in arr_lv_ug:
            if device_id:
                device_id = device_id.strip()
            e_msg += lv_ug_length_check_message(device_id)
            lv_ug_error += 1
            total_error += 1

    # check for self intersect geometry
    if lv_ug_flag and lv_ug_check_flag:
        arr_lv_ug = lv_ug_self_intersect(arr_lv_ug_exclude_geom)
        for device_id in arr_lv_ug:
            if device_id:
                device_id = device_id.strip()
            e_msg += lv_ug_self_intersect_message(device_id)
            lv_ug_error += 1
            total_error += 1

    # check for distance between 2nd vertex to LVDB-FP
    if lv_ug_flag and lv_ug_check_flag:
        arr_lv_ug = lv_ug_1_2_incoming(arr_lv_ug_exclude_geom)
        for device_id in arr_lv_ug:
            if device_id:
                device_id = device_id.strip()
            e_msg += lv_ug_1_2_incoming_message(device_id)
            lv_ug_error += 1
            total_error += 1

    if lv_ug_flag and lv_ug_check_flag:
        arr_lv_ug = lv_ug_1_2_outgoing(arr_lv_ug_exclude_geom)
        for device_id in arr_lv_ug:
            if device_id:
                device_id = device_id.strip()
            e_msg += lv_ug_1_2_outgoing_message(device_id)
            lv_ug_error += 1
            total_error += 1

    # check for LV UG hanging
    if lv_ug_flag and lv_ug_check_flag:
        arr_lv_ug = lv_ug_hanging(arr_lv_ug_exclude_geom, arr_lv_oh_exclude_geom)
        for device_id in arr_lv_ug:
            if device_id:
                device_id = device_id.strip()
            e_msg += lv_ug_hanging_message(device_id)
            lv_ug_error += 1
            total_error += 1

    # check for LV UG buffer
    if lv_ug_flag and lv_ug_check_flag:
        arr_lv_ug = lv_ug_buffer(arr_lv_ug_exclude_geom)
        for device_id in arr_lv_ug:
            if device_id:
                device_id = device_id.strip()
            e_msg += lv_ug_buffer_message(device_id)
            lv_ug_error += 1
            total_error += 1

    if lv_ug_flag and lv_ug_check_flag:
        arr_lv_ug = lv_ug_angle_mismatch()
        for device_id in arr_lv_ug:
            if device_id:
                device_id = device_id.strip()
            e_msg += lv_ug_angle_mismatch_message(device_id)
            lv_ug_error += 1
            total_error += 1

    #  # check for coincidence geometry
    #  if lv_ug_flag:
    #        arr_lv_ug = lv_ug_coin()
    #        for device_id in arr_lv_ug:
    #            e_msg += lv_ug_self_intersect_message(device_id)
    #            lv_ug_error += 1
    #            total_error += 1

    # ****************************************************************
    # ***************     LV OH COND VALIDATION     ******************
    # ****************************************************************

    # moved z_m checking to top

    # check for duplicates
    if lv_oh_flag and lv_oh_check_flag:
        arr_lv_oh = lv_oh_duplicate()
        for device_id in arr_lv_oh:
            if device_id:
                device_id = device_id.strip()
            e_msg += lv_oh_duplicate_message(device_id)
            lv_oh_error += 1
            total_error += 1

    # check for mandatory not null
    field_name_arr = [
        'status'
        , 'phasing'
        , 'usage'
        , 'label'
        , 'length'
        , 'device_id'
        , 'db_oper'
    ]

    if lv_oh_flag and lv_oh_check_flag:
        for field_name in field_name_arr:
            arr_lv_oh = lv_oh_field_not_null(field_name)
            for device_id in arr_lv_oh:
                if device_id:
                    device_id = device_id.strip()
                e_msg += lv_oh_field_not_null_message(device_id, field_name)
                lv_oh_error += 1
                total_error += 1

    # check for ENUM values
    field_name_arr = [
        'status'
        , 'phasing'
        , 'usage'
        , 'label'
        , 'db_oper'
    ]

    if lv_oh_flag and lv_oh_check_flag:
        for field_name in field_name_arr:
            arr_lv_oh = lv_oh_field_enum(field_name)
            for device_id in arr_lv_oh:
                if device_id:
                    device_id = device_id.strip()
                e_msg += lv_oh_field_enum_message(device_id, field_name)
                lv_oh_error += 1
                total_error += 1

    # check for LV OH length
    if lv_oh_flag and lv_oh_check_flag:
        arr_lv_oh = lv_oh_length_check()
        for device_id in arr_lv_oh:
            if device_id:
                device_id = device_id.strip()
            e_msg += lv_oh_length_check_message(device_id)
            lv_oh_error += 1
            total_error += 1

    # check LV OH self intersect
    if lv_oh_flag and lv_oh_check_flag:
        arr_lv_oh = lv_oh_self_intersect(arr_lv_oh_exclude_geom)
        for device_id in arr_lv_oh:
            if device_id:
                device_id = device_id.strip()
            e_msg += lv_oh_self_intersect_message(device_id)
            lv_oh_error += 1
            total_error += 1

    # check LV OH hanging
    if lv_oh_flag and lv_oh_check_flag:
        arr_lv_oh = lv_oh_hanging(arr_lv_ug_exclude_geom, arr_lv_oh_exclude_geom)
        print('arr_lv_oh is..')
        print(arr_lv_oh)
        for device_id in arr_lv_oh:
            if device_id:
                device_id = device_id.strip()
            e_msg += lv_oh_hanging_message(device_id)
            lv_oh_error += 1
            total_error += 1

    # check for LV OH buffer
    if lv_oh_flag and lv_oh_check_flag:
        arr_lv_oh = lv_oh_buffer(arr_lv_oh_exclude_geom)
        for device_id in arr_lv_oh:
            if device_id:
                device_id = device_id.strip()
            e_msg += lv_oh_buffer_message(device_id)
            lv_oh_error += 1
            total_error += 1

    # check for wrong flow direction
    # if lv_oh_flag and lv_oh_check_flag:
    #     arr_lv_oh = lv_oh_wrong_flow(arr_lv_oh_exclude_geom)
    #     for device_id in arr_lv_oh:
    #         if device_id:
    #             device_id = device_id.strip()
    #         e_msg += lv_oh_wrong_flow_message(device_id)
    #         lv_oh_error += 1
    #         total_error += 1

    if lv_oh_flag and lv_oh_check_flag:
        arr_lv_oh = lv_oh_wrong_direction(arr_lv_oh_exclude_geom)
        for device_id in arr_lv_oh:
            if device_id:
                device_id = device_id.strip()
            e_msg += lv_oh_wrong_direction_message(device_id)
            lv_oh_error += 1
            total_error += 1

    # *************************************************************
    # ***************     LV Fuse VALIDATION     ******************
    # *************************************************************

    arr_lv_fuse = []

    # check for z-m value
    if lv_fuse_flag and lv_fuse_check_flag:
        arr_lv_fuse = lv_fuse_z_m_shapefile()
        for device_id in arr_lv_fuse:
            if device_id:
                device_id = device_id.strip()
            e_msg += lv_fuse_z_m_shapefile_message(device_id)
            lv_fuse_error += 1
            total_error += 1

    # check for duplicates
    if lv_fuse_flag and lv_fuse_check_flag:
        arr_lv_fuse = lv_fuse_duplicate()
        for device_id in arr_lv_fuse:
            if device_id:
                device_id = device_id.strip()
            e_msg += lv_fuse_duplicate_message(device_id)
            lv_fuse_error += 1
            total_error += 1

    # check for mandatory not null
    field_name_arr = [
        'status'
        , 'phasing'
        , 'class'
        , 'normal_sta'
        , 'device_id'
        , 'db_oper'
    ]

    if lv_fuse_flag and lv_fuse_check_flag:
        for field_name in field_name_arr:
            arr_lv_fuse = lv_fuse_field_not_null(field_name)
            for device_id in arr_lv_fuse:
                if device_id:
                    device_id = device_id.strip()
                e_msg += lv_fuse_field_not_null_message(device_id, field_name)
                lv_fuse_error += 1
                total_error += 1

    # check for ENUM values
    field_name_arr = [
        'status'
        , 'phasing'
        , 'class'
        , 'normal_sta'
        , 'db_oper'
    ]

    if lv_fuse_flag and lv_fuse_check_flag:
        for field_name in field_name_arr:
            arr_lv_fuse = lv_fuse_field_enum(field_name)
            for device_id in arr_lv_fuse:
                if device_id:
                    device_id = device_id.strip()
                e_msg += lv_fuse_field_enum_message(device_id, field_name)
                lv_fuse_error += 1
                total_error += 1

    # check for nearby Pole
    if lv_fuse_flag and lv_fuse_check_flag:
        arr_lv_fuse = lv_fuse_pole_distance()
        for device_id in arr_lv_fuse:
            if device_id:
                device_id = device_id.strip()
            e_msg += lv_fuse_pole_distance_message(device_id)
            lv_fuse_error += 1
            total_error += 1

    # check for LV Fuse(Blackbox) Snapping Error
    if lv_fuse_flag and lv_fuse_check_flag:
        arr_lv_fuse = lv_fuse_snapping(arr_lv_oh_exclude_geom)
        for device_id in arr_lv_fuse:
            if device_id:
                device_id = device_id.strip()
            e_msg += lv_fuse_snapping_message(device_id)
            lv_fuse_error += 1
            total_error += 1

    # ***************************************************************
    # **************    LV Cable Joint VALIDATION     ***************
    # ***************************************************************

    # print('current total (lv cj): ' + str(total_error))

    arr_lv_cj = []

    # check for z-m value
    if lv_cj_flag and lv_cj_check_flag:
        arr_lv_cj = lv_cj_z_m_shapefile()
        for device_id in arr_lv_cj:
            if device_id:
                device_id = device_id.strip()
            e_msg += lv_cj_z_m_shapefile_message(device_id)
            lv_cj_error += 1
            total_error += 1

    # check for duplicates
    if lv_cj_flag and lv_cj_check_flag:
        arr_lv_cj = lv_cj_duplicate()
        for device_id in arr_lv_cj:
            if device_id:
                device_id = device_id.strip()
            e_msg += lv_cj_duplicate_message(device_id)
            lv_cj_error += 1
            total_error += 1

    # check for mandatory not null
    field_name_arr = [
        'status'
        , 'class'
        , 'type'
        , 'db_oper'
        , 'device_id'
    ]

    if lv_cj_flag and lv_cj_check_flag:
        for field_name in field_name_arr:
            arr_lv_cj = lv_cj_field_not_null(field_name)
            for device_id in arr_lv_cj:
                if device_id:
                    device_id = device_id.strip()
                e_msg += lv_cj_field_not_null_message(device_id, field_name)
                lv_cj_error += 1
                total_error += 1

    # check for ENUM values
    field_name_arr = [
        'status'
        , 'class'
        , 'type'
        , 'db_oper'
    ]

    if lv_cj_flag and lv_cj_check_flag:
        for field_name in field_name_arr:
            arr_lv_cj = lv_cj_field_enum(field_name)
            for device_id in arr_lv_cj:
                if device_id:
                    device_id = device_id.strip()
                e_msg += lv_cj_field_enum_message(device_id, field_name)
                lv_cj_error += 1
                total_error += 1

    # check for snapping with LV OH/LV UG
    if lv_cj_flag and lv_cj_check_flag:
        arr_lv_cj = lv_cj_snapping(arr_lv_ug_exclude_geom, arr_lv_oh_exclude_geom)
        for device_id in arr_lv_cj:
            if device_id:
                device_id = device_id.strip()
            e_msg += lv_cj_snapping_message(device_id)
            lv_cj_error += 1
            total_error += 1
    
    if lv_cj_flag and lv_cj_check_flag:
        arr_lv_cj = lv_cj_class_mismatch(arr_lv_ug_exclude_geom, arr_lv_oh_exclude_geom)
        for device_id in arr_lv_cj:
            if device_id:
                device_id = device_id.strip()
            e_msg += lv_cj_class_mismatch_message(device_id)
            lv_cj_error += 1
            total_error += 1

    # ***************************************************************
    # ******************    LVDB-FP VALIDATION     ******************
    # ***************************************************************

    # print('current total (lvdb-fp): ' + str(total_error))

    arr_lvdb_fp = []

    # check for z-m value
    if lvdb_fp_flag and lvdb_fp_check_flag:
        arr_lvdb_fp = lvdb_fp_z_m_shapefile()
        for device_id in arr_lvdb_fp:
            if device_id:
                device_id = device_id.strip()
            e_msg += lvdb_fp_z_m_shapefile_message(device_id)
            lvdb_fp_error += 1
            total_error += 1

    # check for duplicates
    if lvdb_fp_flag and lvdb_fp_check_flag:
        arr_lvdb_fp = lvdb_fp_duplicate()
        for device_id in arr_lvdb_fp:
            if device_id:
                device_id = device_id.strip()
            e_msg += lvdb_fp_duplicate_message(device_id)
            lvdb_fp_error += 1
            total_error += 1

    # check for mandatory not null
    field_name_arr = [
        'status'
        , 'lvdb_loc'
        , 'design'
        , 'device_id'
        , 'db_oper'
        , 'lvdb_angle'
    ]

    if lvdb_fp_flag and lvdb_fp_check_flag:
        for field_name in field_name_arr:
            arr_lvdb_fp = lvdb_fp_field_not_null(field_name)
            for device_id in arr_lvdb_fp:
                if device_id:
                    device_id = device_id.strip()
                e_msg += lvdb_fp_field_not_null_message(device_id, field_name)
                lvdb_fp_error += 1
                total_error += 1

    # check for ENUM values
    field_name_arr = [
        'status'
        , 'lvdb_loc'
        , 'design'
        , 'db_oper'
    ]

    if lvdb_fp_flag and lvdb_fp_check_flag:
        for field_name in field_name_arr:
            arr_lvdb_fp = lvdb_fp_field_enum(field_name)
            for device_id in arr_lvdb_fp:
                if device_id:
                    device_id = device_id.strip()
                e_msg += lvdb_fp_field_enum_message(device_id, field_name)
                lvdb_fp_error += 1
                total_error += 1

    # check for remarks/db_oper mismatch
    if lvdb_fp_flag and lvdb_fp_check_flag:
        arr_lvdb_fp = lvdb_fp_remarks_db_oper()
        for device_id in arr_lvdb_fp:
            if device_id:
                device_id = device_id.strip()
            e_msg += lvdb_fp_remarks_db_oper_message(device_id)
            lvdb_fp_error += 1
            total_error += 1

    # check for lvf/design mismatch
    if lvdb_fp_flag and lvdb_fp_check_flag:
        arr_lvdb_fp = lvdb_fp_lvf_design()
        for device_id in arr_lvdb_fp:
            if device_id:
                device_id = device_id.strip()
            e_msg += lvdb_fp_lvf_design_message(device_id)
            lvdb_fp_error += 1
            total_error += 1

    # check for lvdb-fp hanging/snapping
    if lvdb_fp_flag and lvdb_fp_check_flag:
        arr_lvdb_fp = lvdb_fp_snapping(arr_lv_ug_exclude_geom, arr_lv_oh_exclude_geom)
        for device_id in arr_lvdb_fp:
            if device_id:
                device_id = device_id.strip()
            e_msg += lvdb_fp_snapping_message(device_id)
            lvdb_fp_error += 1
            total_error += 1

    print('end of total: ' + str(total_error))

    # ***************************************************************
    # ********************    POLE VALIDATION     *******************
    # ***************************************************************

    arr_pole = []

    # check for z-m value
    if pole_flag and pole_check_flag:
        arr_pole = pole_z_m_shapefile()
        for device_id in arr_pole:
            if device_id:
                device_id = device_id.strip()
            e_msg += pole_z_m_shapefile_message(device_id)
            pole_error += 1
            total_error += 1

    # check for duplicates
    if pole_flag and pole_check_flag:
        arr_pole = pole_duplicate()
        for device_id in arr_pole:
            if device_id:
                device_id = device_id.strip()
            e_msg += pole_duplicate_message(device_id)
            pole_error += 1
            total_error += 1

    # check for mandatory not null
    field_name_arr = [
        'status'
        , 'light_ares'
        , 'struc_type'
        , 'pole_no'
        , 'device_id'
        , 'db_oper'
        , 'lv_ptc'
    ]

    if pole_flag and pole_check_flag:
        for field_name in field_name_arr:
            arr_pole = pole_field_not_null(field_name)
        for device_id in arr_pole:
            if device_id:
                device_id = device_id.strip()
            e_msg += pole_field_not_null_message(device_id, field_name)
            pole_error += 1
            total_error += 1

    # check for ENUM values
    field_name_arr = [
        'status'
        , 'light_ares'
        , 'struc_type'
        , 'db_oper'
        , 'lv_ptc'
    ]

    if pole_flag and pole_check_flag:
        for field_name in field_name_arr:
            arr_pole = pole_field_enum(field_name)
            for device_id in arr_pole:
                if device_id:
                    device_id = device_id.strip()
                e_msg += pole_field_enum_message(device_id, field_name)
                pole_error += 1
                total_error += 1

    # check for Pole/LV OH vertex
    if pole_flag and pole_check_flag:
        arr_pole = pole_lv_oh_vertex(arr_lv_oh_exclude_geom)
        for device_id in arr_pole:
            if device_id:
                device_id = device_id.strip()
            e_msg += pole_lv_oh_vertex_message(device_id)
            pole_error += 1
            total_error += 1

    # ***************************************************************
    # ***************    DEMAND POINT VALIDATION     ****************
    # ***************************************************************

    arr_dmd_pt = []

    # check z-m shapefile
    if dmd_pt_flag and dmd_pt_check_flag:
        arr_dmd_pt = dmd_pt_z_m_shapefile()
        for device_id in arr_dmd_pt:
            if device_id:
                device_id = device_id.strip()
            e_msg += dmd_pt_z_m_shapefile_message(device_id)
            dmd_pt_error += 1
            total_error += 1

    # check for duplicates
    if dmd_pt_flag and dmd_pt_check_flag:
        arr_dmd_pt = dmd_pt_duplicate()
        for device_id in arr_dmd_pt:
            if device_id:
                device_id = device_id.strip()
            e_msg += dmd_pt_duplicate_message(device_id)
            dmd_pt_error += 1
            total_error += 1

    # check for mandatory not null
    field_name_arr = [
        'status'
        , 'device_id'
        , 'db_oper'
        , 'dist_tranx'
        , 'house_no'
        , 'str_name'
    ]

    if dmd_pt_flag and dmd_pt_check_flag:
        for field_name in field_name_arr:
            arr_dmd_pt = dmd_pt_field_not_null(field_name)
            for device_id in arr_dmd_pt:
                if device_id:
                    device_id = device_id.strip()
                e_msg += dmd_pt_field_not_null_message(device_id, field_name)
                dmd_pt_error += 1
                total_error += 1

    # check for ENUM values
    field_name_arr = [
        'status'
        , 'db_oper'
    ]

    if dmd_pt_flag and dmd_pt_check_flag:
        for field_name in field_name_arr:
            arr_dmd_pt = dmd_pt_field_enum(field_name)
            for device_id in arr_dmd_pt:
                if device_id:
                    device_id = device_id.strip()
                e_msg += dmd_pt_field_enum_message(device_id, field_name)
                dmd_pt_error += 1
                total_error += 1

    # check for Remarks
    if dmd_pt_flag and dmd_pt_check_flag:
        arr_dmd_pt = dmd_pt_remarks()
        for device_id in arr_dmd_pt:
            if device_id:
                device_id = device_id.strip()
            e_msg += dmd_pt_remarks_message(device_id)
            dmd_pt_error += 1
            total_error += 1

    # check for demand point snapping
    if dmd_pt_flag and dmd_pt_check_flag:
        arr_dmd_pt = dmd_pt_snapping()
        for device_id in arr_dmd_pt:
            if device_id:
                device_id = device_id.strip()
            e_msg += dmd_pt_snapping_message(device_id)
            dmd_pt_error += 1
            total_error += 1

    # ***************************************************************
    # ***************    STREET LIGHT VALIDATION     ****************
    # ***************************************************************

    arr_st_light = []

    # check for duplicates
    if st_light_flag and st_light_check_flag:
        arr_st_light = st_light_z_m_shapefile()
        for device_id in arr_st_light:
            if device_id:
                device_id = device_id.strip()
            e_msg += st_light_z_m_shapefile_message(device_id)
            st_light_error += 1
            total_error += 1

    # check for duplicates
    if st_light_flag and st_light_check_flag:
        arr_st_light = st_light_duplicate()
        for device_id in arr_st_light:
            if device_id:
                device_id = device_id.strip()
            e_msg += st_light_duplicate_message(device_id)
            st_light_error += 1
            total_error += 1

    # check for mandatory not null
    field_name_arr = [
        'status'
        , 'phasing'
        , 'db_oper'
        , 'stl_angle'
        , 'cont_dev'
        , 'device_id'
    ]

    if st_light_flag and st_light_check_flag:
        for field_name in field_name_arr:
            arr_st_light = st_light_field_not_null(field_name)
            for device_id in arr_st_light:
                if device_id:
                    device_id = device_id.strip()
                e_msg += st_light_field_not_null_message(device_id, field_name)
                st_light_error += 1
                total_error += 1

    # check for ENUM values
    field_name_arr = [
        'status'
        , 'db_oper'
        , 'cont_dev'
    ]

    if st_light_flag and st_light_check_flag:
        for field_name in field_name_arr:
            arr_st_light = st_light_field_enum(field_name)
            for device_id in arr_st_light:
                if device_id:
                    device_id = device_id.strip()
                e_msg += st_light_field_enum_message(device_id, field_name)
                st_light_error += 1
                total_error += 1

    # check for phasing must be 'R'   
    if st_light_flag and st_light_check_flag:
        arr_st_light = st_light_phasing()
        for device_id in arr_st_light:
            if device_id:
                device_id = device_id.strip()
            e_msg += st_light_phasing_message(device_id)
            st_light_error += 1
            total_error += 1

    # check for Control Device
    if st_light_flag and st_light_check_flag:
        arr_st_light = st_light_cont_dev()
        for device_id in arr_st_light:
            if device_id:
                device_id = device_id.strip()
            e_msg += st_light_cont_dev_message(device_id)
            st_light_error += 1
            total_error += 1

    # Geom check: Street Light overlap Pole
    if st_light_flag and st_light_check_flag:
        arr_st_light = st_light_overlap_pole()
        for device_id in arr_st_light:
            if device_id:
                device_id = device_id.strip()
            e_msg += st_light_overlap_pole_message(device_id)
            st_light_error += 1
            total_error += 1

    # ***************************************************************
    # ******************    MANHOLE VALIDATION     ******************
    # ***************************************************************

    arr_manhole = []

    # check for z-m value
    if manhole_flag and manhole_check_flag:
        arr_manhole = manhole_z_m_shapefile()
        for device_id in arr_manhole:
            if device_id:
                device_id = device_id.strip()
            e_msg += manhole_z_m_shapefile_message(device_id)
            manhole_error += 1
            total_error += 1

    # check for duplicate
    if manhole_flag and manhole_check_flag:
        arr_manhole = manhole_duplicate()
        for device_id in arr_manhole:
            if device_id:
                device_id = device_id.strip()
            e_msg += manhole_duplicate_message(device_id)
            manhole_error += 1
            total_error += 1

    # check for mandatory not null
    field_name_arr = [
        'status'
        , 'phasing'
        , 'db_oper'
        , 'stl_angle'
        , 'cont_dev'
        , 'device_id'
    ]

    if manhole_flag and manhole_check_flag:
        for field_name in field_name_arr:
            arr_manhole = manhole_field_not_null(field_name)
            for device_id in arr_manhole:
                if device_id:
                    device_id = device_id.strip()
                e_msg += manhole_field_not_null_message(device_id, field_name)
                manhole_error += 1
                total_error += 1

    # check for ENUM values
    field_name_arr = [
        'status'
        , 'phasing'
        , 'db_oper'
        , 'cont_dev'
    ]

    if manhole_flag and manhole_check_flag:
        for field_name in field_name_arr:
            arr_manhole = manhole_field_enum(field_name)
            for device_id in arr_manhole:
                if device_id:
                    device_id = device_id.strip()
                e_msg += manhole_field_enum_message(device_id, field_name)
                manhole_error += 1
                total_error += 1

    # ***************************************************************
    # ***************     STRUCTURE DUCT VALIDATION     *************
    # ***************************************************************

    arr_st_duct = []

    # check for duplicates
    if st_duct_flag and st_duct_check_flag:
        arr_st_duct = st_duct_duplicate()
        for device_id in arr_st_duct:
            if device_id:
                device_id = device_id.strip()
            e_msg += st_duct_duplicate_message(device_id)
            st_duct_error += 1
            total_error += 1

    # check for mandatory not null
    field_name_arr = [
        'status'
        , 'size'
        , 'method'
        , 'way'
        , 'device_id'
        , 'db_oper'
    ]

    if st_duct_flag and st_duct_check_flag:
        for field_name in field_name_arr:
            arr_st_duct = st_duct_field_not_null(field_name)
            for device_id in arr_st_duct:
                if device_id:
                    device_id = device_id.strip()
                e_msg += st_duct_field_not_null_message(device_id, field_name)
                arr_st_duct_error += 1
                total_error += 1

    # check for ENUM values
    field_name_arr = [
        'status'
        , 'size'
        , 'method'
        , 'way'
        , 'db_oper'
    ]

    if st_duct_flag and st_duct_check_flag:
        for field_name in field_name_arr:
            arr_st_duct = st_duct_field_enum(field_name)
            for device_id in arr_st_duct:
                if device_id:
                    device_id = device_id.strip()
                e_msg += st_duct_field_enum_message(device_id, field_name)
                st_duct_error += 1
                total_error += 1

    # *************************************************************
    # ***************     CUSTOMER VALIDATION     ******************
    # *************************************************************

    # customer_meter_empty_code
    field_name_arr = [
        'device_id'
        , 'meter_no'
    ]
    if customer_flag and customer_check_flag:
        for field_name in field_name_arr:
            arr_customer = customer_field_not_null(field_name)
            for device_id in arr_customer:
                if device_id:
                    device_id = device_id.strip()
                e_msg += customer_field_not_null_message(device_id, field_name)
                customer_error += 1
                total_error += 1

    # check device id vs demand point device id
    if customer_flag and customer_check_flag:
        arr_customer = customer_dmd_pt_id_missing()
        for device_id in arr_customer:
            if device_id:
                device_id = device_id.strip()
            e_msg += customer_dmd_pt_id_missing_message(device_id)
            customer_error += 1
            total_error += 1

    # ****************************************************************
    # ******************     END OF VALIDATION     *******************
    # ****************************************************************

    # print('after end of validation, total error is ' + str(total_error))

    # change label in GUI
    if not device_id_flag:
        device_id_error = 'Skipped'
    if lv_ug_flag == False and lv_ug_error == 0:
        lv_ug_error = 'Skipped'
    if lv_oh_flag == False and lv_oh_error == 0:
        lv_oh_error = 'Skipped'
    if not lv_fuse_flag:
        lv_fuse_error = 'Skipped'
    if not lv_cj_flag:
        lv_cj_error = 'Skipped'
    if not lvdb_fp_flag:
        lvdb_fp_error = 'Skipped'
    if not pole_flag:
        pole_error = 'Skipped'
    if not dmd_pt_flag:
        dmd_pt_error = 'Skipped'
    if not st_light_flag:
        st_light_error = 'Skipped'
    if not manhole_flag:
        manhole_error = 'Skipped'
    if not st_duct_flag:
        st_duct_error = 'Skipped'

    self.dlg.label_message.setText(' ')

    # update error count label
    self.dlg.err_device_id.setText(str(device_id_error))
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

    # ****************************************************************
    # ******************     WRITE TO CSV FILE     *******************
    # ****************************************************************

    # write to csv file
    filename = self.dlg.lineEdit_csv.text()
    # if output to csv file, will not print to console.
    # print to console only if no csv filename is specified
    if len(filename) > 4:
        with open(filename, 'w') as output_file:
            # Add header to e_msg
            header = 'Error Code, Device Id, Error Message, Longitude, Latitude \n'
            e_msg = header + e_msg
            output_file.write(e_msg)
        self.iface.messageBar().pushMessage(
            "Success", "Output file written at " + filename,
            level=Qgis.Success, duration=3)
    else:
        # print(e_msg)
        print('total Error(s):', str(total_error))
        self.iface.messageBar().pushMessage(
            "Success", "Validation completed. " + str(total_error) + " ERROR(s) found.",
            level=Qgis.Success, duration=3)
    return 0


def exec_clear_errors(self):
    # start total_error count
    device_id_error = 0
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
    self.dlg.err_device_id.setText(str(device_id_error))
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

    # clear csv file
    self.dlg.lineEdit_csv.setText('')

    return 0
