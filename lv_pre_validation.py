# -*- coding: utf-8 -*-
"""
/***************************************************************************
 lv_pre_validation
                                 A QGIS plugin
 This plugin will check all LV objects and do a QAQC on each element
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-04-06
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Khairil Rizal
        email                : khairil@redplanet.com.my
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
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


def check_filename():
    lvoh_call_me()
    lvug_call_me()
    pole_call_me()
    print('checking filename')


class lv_pre_validation:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'lv_pre_validation_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&LV Pre Validation')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('lv_pre_validation', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/lv_pre_validation/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'LV Pre Validation'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&LV Pre Validation'),
                action)
            self.iface.removeToolBarIcon(action)

    def select_all(self):
        #list all checkbox in plugin
        arr_chkbox = [
            self.dlg.checkBox_lvoh
            ,self.dlg.checkBox_lvug
            ,self.dlg.checkBox_pole
            ,self.dlg.checkBox_lv_fuse
            ,self.dlg.checkBox_lv_cj
            ,self.dlg.checkBox_lvdb_fp
            ,self.dlg.checkBox_dmd_pt
            ,self.dlg.checkBox_st_light
            ,self.dlg.checkBox_manhole
            ,self.dlg.checkBox_st_duct
            ]
        
        if self.dlg.checkBox_all.isChecked():
            print('select all = true')
            for chk in arr_chkbox:
                chk.setChecked(True)
            
        else :
            print('select all = false')
            for chk in arr_chkbox:
                chk.setChecked(False)

            
    def select_output_file(self):
        filename, _filter = QFileDialog.getSaveFileName(
            self.dlg, "Select output file ","untitled.csv",'.csv')
        self.dlg.label_message.setText('Click Run QAQC to generate CSV file')
        if ".csv" in filename:
            self.dlg.lineEdit_csv.setText(filename)
        else:
            self.dlg.lineEdit_csv.setText(filename + '.csv')

    def count_features(self):
        #count features moved to feature_count.py
        count_lv_features(self)
        return 0

    def run_qa_qc(self):
        
        # count features
        count_lv_features(self)
        
        featCount = 0
        if self.dlg.checkBox_lvug.isChecked():
            featCount += 1
        if self.dlg.checkBox_lvoh.isChecked():
            featCount += 1
        if self.dlg.checkBox_lv_fuse.isChecked():
            featCount += 1
        if self.dlg.checkBox_lv_cj.isChecked():
            featCount += 1
        if self.dlg.checkBox_lvdb_fp.isChecked():
            featCount += 1
        if self.dlg.checkBox_pole.isChecked():
            featCount += 1
        if self.dlg.checkBox_dmd_pt.isChecked():
            featCount += 1
        if self.dlg.checkBox_st_light.isChecked():
            featCount += 1
        if self.dlg.checkBox_manhole.isChecked():
            featCount += 1
        if self.dlg.checkBox_st_duct.isChecked():
            featCount += 1
        

        qa_qc_msg = ' ' .join(['running QA/QC now on ',str(featCount),'features'])
        print(qa_qc_msg)

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

        #****************************************************************
        #***************     LV UG COND VALIDATION    *******************
        #****************************************************************

        # check for mandatory not null
        arr_lv_ug = []

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

        #****************************************************************
        #***************     LV OH COND VALIDATION     ******************
        #****************************************************************

        arr_lv_oh = []

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

        
        # check for LV UG length
        if lv_oh_flag:
            arr_lv_oh = lv_oh_length_check()
        for device_id in arr_lv_oh:
            e_msg += lv_oh_length_check_message(device_id)
            lv_oh_error += 1
            total_error += 1

        #*************************************************************
        #***************     LV Fuse VALIDATION     ******************
        #*************************************************************

        arr_lv_fuse = []

        # check for mandatory not null
        field_name_arr = [
            'status'
            ,'phasing'
            ,'class'
            ,'normal_sta'
            ,'device_id'            
            ,'db_oper'
            ]

        for field_name in field_name_arr: 
            if lv_fuse_flag:
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
         
        for field_name in field_name_arr: 
            if lv_fuse_flag:
                arr_lv_fuse = lv_fuse_field_enum(field_name)
            for device_id in arr_lv_fuse:
                e_msg += lv_fuse_field_enum_message(device_id, field_name)
                lv_fuse_error += 1
                total_error += 1

        #***************************************************************
        #**************    LV Cable Joint VALIDATION     ***************
        #***************************************************************

        arr_lv_cj = []

        # check for mandatory not null
        field_name_arr = [
            'status'
            ,'class'
            ,'type'
            ,'db_oper'
            ,'device_id'
            ]
        
        for field_name in field_name_arr: 
            if lv_cj_flag:
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

        for field_name in field_name_arr: 
            if lv_cj_flag:
                arr_lv_cj = lv_cj_field_enum(field_name)
            for device_id in arr_lv_cj:
                e_msg += lv_cj_field_enum_message(device_id, field_name)
                lv_cj_error += 1
                total_error += 1

        #***************************************************************
        #******************    LVDB-FP VALIDATION     ******************
        #***************************************************************

        arr_lvdb_fp = []

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

        

        #***************************************************************
        #********************    POLE VALIDATION     *******************
        #***************************************************************

        arr_pole = []

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

        #***************************************************************
        #***************    DEMAND POINT VALIDATION     ****************
        #***************************************************************

        arr_dmd_pt = []

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

        #***************************************************************
        #***************    STREET LIGHT VALIDATION     ****************
        #***************************************************************

        arr_st_light = []

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
            ,'phasing'
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

        #***************************************************************
        #******************    MANHOLE VALIDATION     ******************
        #***************************************************************

        arr_manhole = []

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
                
        #print to console
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
            
        #e_msg += 'lv_ug Error is ' + str(lv_ug_error) + '\n'
        #e_msg += 'lv_oh Error is ' + str(lv_oh_error) + '\n'
        #e_msg += 'pole Error is ' + str(pole_error) + '\n'
        #e_msg += 'total Error is ' + str(total_error) + '\n'
        print(e_msg)
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

        # write to csv file
        filename = self.dlg.lineEdit_csv.text()
        if len(filename) > 4:
            with open(filename, 'w') as output_file:
                output_file.write(e_msg)
            self.iface.messageBar().pushMessage(
                  "Success", "Output file written at " + filename,
                  level=Qgis.Success, duration=3)
        else:
            self.iface.messageBar().pushMessage(
                  "Success", "Validation completed. " + str(total_error) + " ERROR(s) found.",
                  level=Qgis.Success, duration=3)
            


    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start:
            self.first_start = False
            self.dlg = lv_pre_validationDialog()
            #connect controls to function
            self.dlg.checkBox_all.stateChanged.connect(self.select_all)
            self.dlg.pushButton_csv.clicked.connect(self.select_output_file)
            self.dlg.pushButton_filename.clicked.connect(check_filename)
            self.dlg.pushButton_count.clicked.connect(self.count_features)
            self.dlg.pushButton_qaqc.clicked.connect(self.run_qa_qc)

        # show the dialog
        self.dlg.show()
        # test: count features on load
        count_lv_features(self)
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
