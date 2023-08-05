# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class SavingsSpecialAdjustmentMethodDTO(Model):
    """SavingsSpecialAdjustmentMethodDTO.

    :param label: The description
    :type label: str
    :param special_adjustment_method_id: The special adjustment method id
    :type special_adjustment_method_id: int
    :param electric_only: The flag which determines if this method is for
     electric meter only
    :type electric_only: bool
    :param symbol: The symbol on value
    :type symbol: str
    :param precision: The precision on value
    :type precision: int
    """

    _attribute_map = {
        'label': {'key': 'label', 'type': 'str'},
        'special_adjustment_method_id': {'key': 'specialAdjustmentMethodId', 'type': 'int'},
        'electric_only': {'key': 'electricOnly', 'type': 'bool'},
        'symbol': {'key': 'symbol', 'type': 'str'},
        'precision': {'key': 'precision', 'type': 'int'},
    }

    def __init__(self, label=None, special_adjustment_method_id=None, electric_only=None, symbol=None, precision=None):
        super(SavingsSpecialAdjustmentMethodDTO, self).__init__()
        self.label = label
        self.special_adjustment_method_id = special_adjustment_method_id
        self.electric_only = electric_only
        self.symbol = symbol
        self.precision = precision
