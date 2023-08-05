# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class BillsBillEntryBodyLineDTO(Model):
    """BillsBillEntryBodyLineDTO.

    :param body_line_id:
    :type body_line_id: int
    :param caption:
    :type caption: str
    :param value:
    :type value: ~energycap.sdk.models.BillsBillEntryBodyLineWithNounChildDTO
    :param cost:
    :type cost: ~energycap.sdk.models.BillsBillEntryBodyLineChildDTO
    :param observation_type:
    :type observation_type:
     ~energycap.sdk.models.BillsBillEntryObservationTypeChildDTO
    """

    _attribute_map = {
        'body_line_id': {'key': 'bodyLineId', 'type': 'int'},
        'caption': {'key': 'caption', 'type': 'str'},
        'value': {'key': 'value', 'type': 'BillsBillEntryBodyLineWithNounChildDTO'},
        'cost': {'key': 'cost', 'type': 'BillsBillEntryBodyLineChildDTO'},
        'observation_type': {'key': 'observationType', 'type': 'BillsBillEntryObservationTypeChildDTO'},
    }

    def __init__(self, body_line_id=None, caption=None, value=None, cost=None, observation_type=None):
        super(BillsBillEntryBodyLineDTO, self).__init__()
        self.body_line_id = body_line_id
        self.caption = caption
        self.value = value
        self.cost = cost
        self.observation_type = observation_type
