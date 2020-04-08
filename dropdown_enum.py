# check dropdown values for all objects
from qgis.core import *

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

def dropdown_call_me():
	print('dropdown enum is called')
        

          
	
