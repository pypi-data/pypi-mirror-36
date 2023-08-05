# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ChargebackNewCalculatedBillSumResponseDTO(Model):
    """ChargebackNewCalculatedBillSumResponseDTO.

    :param sum_meters: Meters in this list will have their use or cost added
     together during the bill calculation
    :type sum_meters: list[~energycap.sdk.models.LogicalDeviceMeterChildDTO]
    :param sum_meter_groups: Distinct meters from these meter groups will have
     their use or cost added together during the bill calculation
    :type sum_meter_groups:
     list[~energycap.sdk.models.GroupMeterGroupChildDTO]
    """

    _attribute_map = {
        'sum_meters': {'key': 'sumMeters', 'type': '[LogicalDeviceMeterChildDTO]'},
        'sum_meter_groups': {'key': 'sumMeterGroups', 'type': '[GroupMeterGroupChildDTO]'},
    }

    def __init__(self, sum_meters=None, sum_meter_groups=None):
        super(ChargebackNewCalculatedBillSumResponseDTO, self).__init__()
        self.sum_meters = sum_meters
        self.sum_meter_groups = sum_meter_groups
