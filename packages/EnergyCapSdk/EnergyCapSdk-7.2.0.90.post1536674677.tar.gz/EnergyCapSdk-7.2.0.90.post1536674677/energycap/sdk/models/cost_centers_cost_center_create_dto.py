# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class CostCentersCostCenterCreateDTO(Model):
    """CostCentersCostCenterCreateDTO.

    :param cost_center_code: The cost center code <span
     class='property-internal'>Required</span> <span
     class='property-internal'>Must be between 0 and 32 characters</span>
    :type cost_center_code: str
    :param cost_center_info: The cost center info <span
     class='property-internal'>Required</span> <span
     class='property-internal'>Must be between 0 and 32 characters</span>
    :type cost_center_info: str
    :param parent_cost_center_id: The identifier for the parent of the cost
     center. The parent is the cost center directly above the current cost
     center on the Accounts tree <span
     class='property-internal'>Required</span> <span
     class='property-internal'>Topmost (CostCenter)</span>
    :type parent_cost_center_id: int
    """

    _validation = {
        'cost_center_code': {'required': True, 'max_length': 32, 'min_length': 0},
        'cost_center_info': {'required': True, 'max_length': 32, 'min_length': 0},
        'parent_cost_center_id': {'required': True},
    }

    _attribute_map = {
        'cost_center_code': {'key': 'costCenterCode', 'type': 'str'},
        'cost_center_info': {'key': 'costCenterInfo', 'type': 'str'},
        'parent_cost_center_id': {'key': 'parentCostCenterId', 'type': 'int'},
    }

    def __init__(self, cost_center_code, cost_center_info, parent_cost_center_id):
        super(CostCentersCostCenterCreateDTO, self).__init__()
        self.cost_center_code = cost_center_code
        self.cost_center_info = cost_center_info
        self.parent_cost_center_id = parent_cost_center_id
