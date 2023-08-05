# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class AccountMeterAccountMeterResponseDTO(Model):
    """AccountMeterAccountMeterResponseDTO.

    :param account_meter_id: The account meter identifier
    :type account_meter_id: int
    :param account: The account for this account meter
    :type account: ~energycap.sdk.models.AccountsAccountChildDTO
    :param meter: The meter for this account meter
    :type meter: ~energycap.sdk.models.LogicalDeviceMeterChildDTO
    :param begin_date: The beginning date and time for this account meter
     relationship
    :type begin_date: datetime
    :param end_date: The ending date and time for this account meter
     relationship
    :type end_date: datetime
    :param general_ledger: The general ledger assigned to this account meter
    :type general_ledger: ~energycap.sdk.models.BillsGeneralLedgerChildDTO
    :param vendor_type: The vendor type. Vendors may assume different types on
     different account meters
    :type vendor_type: ~energycap.sdk.models.AccountsVendorTypeChildDTO
    :param deregulated: Indicates if the account meter is deregulated
    :type deregulated: bool
    :param form_templates: The template assigned to this account meter
    :type form_templates:
     list[~energycap.sdk.models.AccountMeterFormTemplateChildDTO]
    :param rates: The rate assigned to this account meter
    :type rates: list[~energycap.sdk.models.AccountMeterAccountRateChildDTO]
    """

    _attribute_map = {
        'account_meter_id': {'key': 'accountMeterId', 'type': 'int'},
        'account': {'key': 'account', 'type': 'AccountsAccountChildDTO'},
        'meter': {'key': 'meter', 'type': 'LogicalDeviceMeterChildDTO'},
        'begin_date': {'key': 'beginDate', 'type': 'iso-8601'},
        'end_date': {'key': 'endDate', 'type': 'iso-8601'},
        'general_ledger': {'key': 'generalLedger', 'type': 'BillsGeneralLedgerChildDTO'},
        'vendor_type': {'key': 'vendorType', 'type': 'AccountsVendorTypeChildDTO'},
        'deregulated': {'key': 'deregulated', 'type': 'bool'},
        'form_templates': {'key': 'formTemplates', 'type': '[AccountMeterFormTemplateChildDTO]'},
        'rates': {'key': 'rates', 'type': '[AccountMeterAccountRateChildDTO]'},
    }

    def __init__(self, account_meter_id=None, account=None, meter=None, begin_date=None, end_date=None, general_ledger=None, vendor_type=None, deregulated=None, form_templates=None, rates=None):
        super(AccountMeterAccountMeterResponseDTO, self).__init__()
        self.account_meter_id = account_meter_id
        self.account = account
        self.meter = meter
        self.begin_date = begin_date
        self.end_date = end_date
        self.general_ledger = general_ledger
        self.vendor_type = vendor_type
        self.deregulated = deregulated
        self.form_templates = form_templates
        self.rates = rates
