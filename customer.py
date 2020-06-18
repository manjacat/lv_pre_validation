# Test import python file
from qgis.core import *

# for testing purposes
from .analysis import *

"""
/***************************************************************************
All checkings related to Customer 

error to check:
 DEMAND_PT_ID_MISSING 
 METER_NO_EMPTY_OR_CONTAIN_NA 
 CSV_NAME_AND_FORMAT_MISMATCH 
 ***************************************************************************/
"""

layer_name = 'Customer'
st_duct_field_null = 'ERR_CUSTMR_01'
st_duct_enum_valid = 'ERR_CUSTMR_02'

def customer_dmd_pt_id():
    arr = []

    layer = QgsProject.instance().mapLayersByName(layer_name)[0]

    return arr