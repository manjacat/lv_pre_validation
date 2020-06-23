"""
/***************************************************************************
All checkings related to Customer

error to check:
 DEMAND_PT_ID_MISSING
 METER_NO_EMPTY_OR_CONTAIN_NA
 CSV_NAME_AND_FORMAT_MISMATCH
 ***************************************************************************/
"""

# Test import python file
from qgis.core import *
# import own custom file
from .dropdown_enum import *
from .rps_utility import *

layer_name = 'Customer'
customer_dmd_pt_id_missing_code = 'ERR_CUSTOMER_01'
customer_field_not_null_code = 'ERR_CUSTOMER_02'

"""
The customer should be associated with the captured demand point.
the device id should contain the device id of the associated demand point.
"""
def customer_dmd_pt_id_missing():

    # get list of demand point ids
    arr_dmd = []
    layer_dmd = QgsProject.instance().mapLayersByName('Demand_Point')[0]
    feat_dmd = layer_dmd.getFeatures()
    for f in feat_dmd:
        device_id = f.attribute('device_id')
        if device_id:
            # strip string to remove /r/n
            arr_dmd.append(device_id.strip())
        # print(arr_dmd)

    # get list of customer and check if demand point id is null or is not in the list
    arr = []
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    feat = layer.getFeatures()
    for f in feat:
        device_id = f.attribute('device_id')
        if device_id:
            device_id = device_id.strip()
            # check if device id is in array
            if device_id not in arr_dmd:
                arr.append(device_id)
        else:
            arr.append(str(device_id))

    return arr

def customer_dmd_pt_id_missing_message(device_id):
    longitude = 0
    latitude = 0
    error_desc = 'Customer device_id: ' + str(device_id) + '. No Demand Point has this device_id. '
    e_msg = customer_dmd_pt_id_missing_code + ', ' + str(device_id) + ', ' + error_desc + ', ' + str(longitude) + ',' + str(latitude) + ' \n'
    return e_msg

"""
    meter_no should not be empty and should not provide “N/A”
"""
def customer_field_not_null(field_name):
    arr = rps_field_not_null(layer_name, field_name)
    return arr

def customer_field_not_null_message(device_id, field_name):
    e_msg = rps_field_not_null_message(device_id, field_name, layer_name, customer_field_not_null_code)
    return e_msg