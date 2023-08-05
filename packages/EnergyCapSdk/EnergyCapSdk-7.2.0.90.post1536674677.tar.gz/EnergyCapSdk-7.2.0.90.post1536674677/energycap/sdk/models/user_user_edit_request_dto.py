# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class UserUserEditRequestDTO(Model):
    """UserUserEditRequestDTO.

    :param user_code:  <span class='property-internal'>Required</span> <span
     class='property-internal'>Must be between 0 and 32 characters</span>
    :type user_code: str
    :param full_name:  <span class='property-internal'>Required</span> <span
     class='property-internal'>Must be between 0 and 32 characters</span>
    :type full_name: str
    :param password:  <span class='property-internal'>Must be between 0 and
     128 characters</span>
    :type password: str
    :param email:  <span class='property-internal'>Required</span> <span
     class='property-internal'>Must be between 0 and 128 characters</span>
    :type email: str
    :param cost_center_id:  <span class='property-internal'>Required</span>
     <span class='property-internal'>Topmost (CostCenter)</span>
    :type cost_center_id: int
    :param place_id:  <span class='property-internal'>Required</span> <span
     class='property-internal'>Topmost (Place)</span>
    :type place_id: int
    :param active_directory:  <span class='property-internal'>Required</span>
    :type active_directory: bool
    :param active:  <span class='property-internal'>Required</span>
    :type active: bool
    :param password_expiration_interval:  <span
     class='property-internal'>Required</span>
    :type password_expiration_interval: int
    :param strong_password:  <span class='property-internal'>Required</span>
    :type strong_password: bool
    :param force_password_change:  <span
     class='property-internal'>Required</span>
    :type force_password_change: bool
    :param user_role_id:  <span class='property-internal'>Required</span>
    :type user_role_id: int
    :param max_approval_amount:
    :type max_approval_amount: int
    :param report_group_id:  <span class='property-internal'>Required</span>
    :type report_group_id: int
    """

    _validation = {
        'user_code': {'required': True, 'max_length': 32, 'min_length': 0},
        'full_name': {'required': True, 'max_length': 32, 'min_length': 0},
        'password': {'max_length': 128, 'min_length': 0},
        'email': {'required': True, 'max_length': 128, 'min_length': 0},
        'cost_center_id': {'required': True},
        'place_id': {'required': True},
        'active_directory': {'required': True},
        'active': {'required': True},
        'password_expiration_interval': {'required': True},
        'strong_password': {'required': True},
        'force_password_change': {'required': True},
        'user_role_id': {'required': True},
        'max_approval_amount': {'required': True},
        'report_group_id': {'required': True},
    }

    _attribute_map = {
        'user_code': {'key': 'userCode', 'type': 'str'},
        'full_name': {'key': 'fullName', 'type': 'str'},
        'password': {'key': 'password', 'type': 'str'},
        'email': {'key': 'email', 'type': 'str'},
        'cost_center_id': {'key': 'costCenterId', 'type': 'int'},
        'place_id': {'key': 'placeId', 'type': 'int'},
        'active_directory': {'key': 'activeDirectory', 'type': 'bool'},
        'active': {'key': 'active', 'type': 'bool'},
        'password_expiration_interval': {'key': 'passwordExpirationInterval', 'type': 'int'},
        'strong_password': {'key': 'strongPassword', 'type': 'bool'},
        'force_password_change': {'key': 'forcePasswordChange', 'type': 'bool'},
        'user_role_id': {'key': 'userRoleId', 'type': 'int'},
        'max_approval_amount': {'key': 'maxApprovalAmount', 'type': 'int'},
        'report_group_id': {'key': 'reportGroupId', 'type': 'int'},
    }

    def __init__(self, user_code, full_name, email, cost_center_id, place_id, active_directory, active, password_expiration_interval, strong_password, force_password_change, user_role_id, max_approval_amount, report_group_id, password=None):
        super(UserUserEditRequestDTO, self).__init__()
        self.user_code = user_code
        self.full_name = full_name
        self.password = password
        self.email = email
        self.cost_center_id = cost_center_id
        self.place_id = place_id
        self.active_directory = active_directory
        self.active = active
        self.password_expiration_interval = password_expiration_interval
        self.strong_password = strong_password
        self.force_password_change = force_password_change
        self.user_role_id = user_role_id
        self.max_approval_amount = max_approval_amount
        self.report_group_id = report_group_id
