# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class CostCenterDigestCostCenterDigestActualMonthlyResponseDTOResultsDTO(Model):
    """CostCenterDigestCostCenterDigestActualMonthlyResponseDTOResultsDTO.

    :param period_name: Calendar Period Name
    :type period_name: str
    :param calendar_period: Calendar Period
    :type calendar_period: int
    :param calendar_year: Calendar Year
    :type calendar_year: int
    :param fiscal_period: Fiscal Period
    :type fiscal_period: int
    :param fiscal_year: Fiscal Year
    :type fiscal_year: int
    :param total_cost: Total Cost
    :type total_cost: float
    :param global_use: Global Use
    :type global_use: float
    :param global_use_unit_cost: Global Use Unit Cost
    :type global_use_unit_cost: float
    """

    _attribute_map = {
        'period_name': {'key': 'periodName', 'type': 'str'},
        'calendar_period': {'key': 'calendarPeriod', 'type': 'int'},
        'calendar_year': {'key': 'calendarYear', 'type': 'int'},
        'fiscal_period': {'key': 'fiscalPeriod', 'type': 'int'},
        'fiscal_year': {'key': 'fiscalYear', 'type': 'int'},
        'total_cost': {'key': 'totalCost', 'type': 'float'},
        'global_use': {'key': 'globalUse', 'type': 'float'},
        'global_use_unit_cost': {'key': 'globalUseUnitCost', 'type': 'float'},
    }

    def __init__(self, period_name=None, calendar_period=None, calendar_year=None, fiscal_period=None, fiscal_year=None, total_cost=None, global_use=None, global_use_unit_cost=None):
        super(CostCenterDigestCostCenterDigestActualMonthlyResponseDTOResultsDTO, self).__init__()
        self.period_name = period_name
        self.calendar_period = calendar_period
        self.calendar_year = calendar_year
        self.fiscal_period = fiscal_period
        self.fiscal_year = fiscal_year
        self.total_cost = total_cost
        self.global_use = global_use
        self.global_use_unit_cost = global_use_unit_cost
