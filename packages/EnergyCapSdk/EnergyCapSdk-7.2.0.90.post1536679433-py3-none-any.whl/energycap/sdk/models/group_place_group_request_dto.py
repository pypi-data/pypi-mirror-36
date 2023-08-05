# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class GroupPlaceGroupRequestDTO(Model):
    """<span class='property-internal'>Only one of AutomaticGroupFilters,
    ManualGroupMembers is required</span>.

    :param place_group_info: The place group info <span
     class='property-internal'>Must be between 0 and 255 characters</span>
     <span class='property-internal'>Required</span>
    :type place_group_info: str
    :param place_group_category_id: The place group category <span
     class='property-internal'>Required</span>
    :type place_group_category_id: int
    :param limit_members_by_topmost: Should this group only return members
     within the current user's topmost <span
     class='property-internal'>Required</span>
    :type limit_members_by_topmost: bool
    :param automatic_group_filters: List of filters to add members to an
     automic place group
     Either AutomaticGroupFilters or ManualGroupMembers, but not both, must be
     passed in <span class='property-internal'>Cannot be Empty</span> <span
     class='property-internal'>NULL Valid</span>
    :type automatic_group_filters:
     list[~energycap.sdk.models.CommonFilterEditDTO]
    :param manual_group_members: List of members to add to the group
     Either AutomaticGroupFilters or ManualGroupMembers, but not both, must be
     passed in
     Members but be within the current user's topmost
     You can create an empty group by passing in an empty array
    :type manual_group_members: list[int]
    """

    _validation = {
        'place_group_info': {'required': True, 'max_length': 255, 'min_length': 0},
        'place_group_category_id': {'required': True},
        'limit_members_by_topmost': {'required': True},
    }

    _attribute_map = {
        'place_group_info': {'key': 'placeGroupInfo', 'type': 'str'},
        'place_group_category_id': {'key': 'placeGroupCategoryId', 'type': 'int'},
        'limit_members_by_topmost': {'key': 'limitMembersByTopmost', 'type': 'bool'},
        'automatic_group_filters': {'key': 'automaticGroupFilters', 'type': '[CommonFilterEditDTO]'},
        'manual_group_members': {'key': 'manualGroupMembers', 'type': '[int]'},
    }

    def __init__(self, place_group_info, place_group_category_id, limit_members_by_topmost, automatic_group_filters=None, manual_group_members=None):
        super(GroupPlaceGroupRequestDTO, self).__init__()
        self.place_group_info = place_group_info
        self.place_group_category_id = place_group_category_id
        self.limit_members_by_topmost = limit_members_by_topmost
        self.automatic_group_filters = automatic_group_filters
        self.manual_group_members = manual_group_members
