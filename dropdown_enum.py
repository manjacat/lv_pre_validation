# check dropdown values for all objects
from qgis.core import *

def dropdown_call_me():
	print('dropdown enum is called')
	return 0

# **************************
# *****   LV UG Enum   *****
# **************************
arr_status = [
        'Abandoned'
        ,'Existing'
        ,'Inactive'
        ,'Proposed'
        ,'Proposed Abandon'
        ,'Proposed Remove'
        ,'Proposed Replace'
        ,'Removed'
        ,'Temporary'
        ]

arr_phasing = [
        'Y'
        ,'Neutral'
        ,'RY'
        ,'Unknown'
        ,'YB'
        ,'BR'
        ,'R'
        ,'B'
        ,'RYB'
        ]

arr_usage = [
        '5 FOOT WAYS'
        ,'LV LINE'
        ,'PRIVATE LIGHT'
        ,'PUBLIC LIGHT'
        ,'SERVICE LINE'
        ,'Unknown'
        ]

arr_label_lv_ug = [
        '120_4C_AL_PILC'
        ,'120_4C_AL_XLPE'
        ,'185_4C_AL_PILC'
        ,'185_4C_AL_XLPE'
        ,'25_4C_AL_PILC'
        ,'25_4C_AL_XLPE'
        ,'35_4C_AL_XLPE'
        ,'300_4C_AL_PILC'
        ,'300_4C_AL_XLPE'
        ,'70_4C_AL_PILC'
        ,'70_4C_AL_XLPE'
        ,'240_4C_AL_XLPE'
        ,'240_4C_QUADRAPLEX'
        ,'300_4C_AL_TRIPLEX'
        ,'ARMOURED_16MM'
        ,'4X_300_1C_AL_PVC/PVC'
        ,'4X_500_1C_AL_PVC/PVC'
        ,'7X_300_1C_AL_PVC/PVC'
        ,'7X_500_1C_AL_PVC/PVC'
        ]

arr_dat_qty_cl = [
        'Class A'
        ,'Class B'
        ,'Class C'
        ,'Class D'
        ]

arr_db_oper = [
        'Insert'
        ,'Update'
        ,'Delete'
        ]

# **************************
# *****   LV OH Enum   *****
# **************************

# status - as lv ug
# phasing - as lv ug
# usage - as lv ug
# db_oper - as lv ug

arr_label_lv_oh = [
        '3X_185+120+16_ABC_INS'
        ,'3X_95+70+16_ABC_INS'
        ,'3X_95+70_ABC_INS'
        ,'3X_16+25_ABC_INS'
        ,'1X_16+25_ABC_INS'
        ,'4X_19/0.064"_PVC_AL'
        ,'4X_19/0.083"_PVC_AL'
        ,'3X_19/0.064"_PVC_AL'
        ,'2X_19/0.064"_PVC_AL'
        ,'2X_19/0.083"_PVC_AL'
        ,'2X_7/0.044"_PVC_AL'
        ,'4X_7/0.173"_BARE_AL'
        ,'4X_7/0.122"_BARE_AL'
        ,'2X_7/0.173"_BARE_AL'
        ,'2X_7/0.122"_BARE_AL'
        ,'2X_3/0.132"_BARE_AL'
        ]

# ****************************
# *****   LV Fuse Enum   *****
# ****************************

# status - as lv ug
# phasing - as lv ug
# db_oper - as lv ug

arr_class_lv_fuse = [
        'LV FUSE SWITCH'
        ,'BLACK BOX DOUBLE'
        ,'BLACK BOX'
        ,'Unknown'
        ,'POLE FUSE'
        ,'CUT OUT'
        ,'BLACK BOX SINGLE'
        ,'BLACK BOX TRIPLE'
        ,'GREEN BOX'
        ]

arr_normal_sta = [
        'CLOSED'
        ,'OPEN'
        ]

# ***********************************
# *****   LV Cable Joint Enum   *****
# ***********************************

# status - as lv ug
# db_oper - as lv ug

arr_class_lv_cj = [
        'END POINT'
        ,'LV JOINT'
        ,'LV POT END'
        ,'LV TERMINAL'
        ,'SL CABLE TERMINAL'
        ,'SL POT END'
        ,'Unknown'
        ]

arr_type_lv_cj = [
        'BOLTED'
        ,'COLD SHRINK'
        ,'COMPOUND'
        ,'COMPRESSION'
        ,'HEAT SHRINK'
        ,'MV TERMINAL'
        ,'PIN AND SOCKET'
        ,'POT END'
        ,'PRE-MOULDED'
        ,'RESIN TYPE'
        ,'Unknown'
        ]

# ********************************
# *******   LVDB-FP Enum   *******
# ********************************

# status - as lv ug
# db_oper - as lv ug

arr_lvdb_loc = [
        'INDOOR'
        ,'OUTDOOR'
        ,'Unknown'
        ]

arr_design_lvdb = [
        'FP 1600 A - 2 in 8 out'
        ,'FP 800 A - 2 in 5 out'
        ,'FP 160000 A - 2 in 8 out (PE)'
        ,'LVDB 1600 A - 2 in 10 out (CS)'
        ,'LVDB 1600 A - 2 in 8 out'
        ,'LVDB 800 A - 2 in 6 out (CS)'
        ,'LVDB 800 A - 2 in 5 out (CS)'
        ,'MINI FP 400 A - 2 in 6 out'
        ]


# *************************
# *****   Pole Enum   *****
# *************************

# status - as lv ug
# db_oper - as lv ug

arr_ares = [
        'NO'
        ,'Unknown'
        ,'YES'
        ]

arr_struc_type = [
        'CONCRETE POLE 30\'' 
        ,'GUY STUB' 
        ,'H POLE ANGLE P1, P2, P3, P4' 
        ,'H POLE INTERMEDIATE'
        ,'H POLE TERMINAL'
        ,'MINI TOWER ANGLE' 
        ,'MINI TOWER STRAIGHT' 
        ,'MINI TOWER TERMINAL'
        ,'SINGLE STEEL 35\''
        ,'SINGLE STEEL45\''
        ,'SPUN POLE 10.0M-5.0 KN' 
        ,'SPUN POLE 7.5M-1.1 KN'
        ,'SPUN POLE 7.5M-2.0 KN'
        ,'SPUN POLE 9.0M-2.0 KN'
        ,'UNKNOWN LV POLE'
        ,'UNKNOWN S/L POLE'
        ,'Unknown'
        ,'WOODEN POLE 25\''
        ,'WOODEN POLE 30\''
        ]

arr_lv_ptc = [
        'Yes'
        ,'No'
        ]

# *********************************
# *****   Demand Point Enum   *****
# *********************************

# status - as lv ug
# db_oper - as lv ug

# *********************************
# *****   Street Light Enum   *****
# *********************************

# status - as lv ug
# db_oper - as lv ug

# phasing in st_light should only be 'R', so other values 'Y','B','Unknown' are ignored.        
arr_phasing_st_light = [
        'R'
        ]

arr_cont_dev = [
        'NONE'
        ,'PANEL'
        ,'PHOTO CELL'
        ,'TIME SWITCH'
        ,'Unknown'
        ]

# ****************************
# *****   Manhole Enum   *****
# ****************************

# status - as lv ug
# db_oper - as lv ug

arr_type_manhole = [
        'Corner Manhole'
        ,'Straight Manhole'
        ,'T Manhole'
        ,'Type L'
        ,'Type M'
        ,'Type N'
        ,'Type O'
        ,'Unknown'
        ]

# ***********************************
# *****   Structure Duct Enum   *****
# ***********************************

# status - as lv ug
# db_oper - as lv ug

arr_size_st_duct = [
        '4"'
        ,'6"'
        ,'8"'
        ,'Unknown'
        ]

arr_method_st_duct = [
        'Cable Bridge'
        ,'Common Utility Tunnel'
        ,'HDD'
        ,'Micro Tunnelling'
        ,'Open Cut'
        ,'Pipe Jacking'
        ,'Unknown'
        ]

arr_way_st_duct = [
        '1'
        ,'10'
        ,'11'
        ,'12'
        ,'13'
        ,'14'
        ,'15'
        ,'16'
        ,'17'
        ,'18'
        ,'19'
        ,'2'
        ,'20'
        ,'24'
        ,'3'
        ,'36'
        ,'4'
        ,'5'
        ,'6'
        ,'66'
        ,'7'
        ,'8'
        ,'9'
        ,'HDD'
        ,'Open Cut'
        ]

# *******************************
# *****   END of All Enum   *****
# *******************************
          
	
