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

        

          
	
