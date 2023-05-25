import json
from typing import Any, Optional
from melder.botc.role import Role


# a lazy exception class
class RoleDataException(Exception):
    """Generic exception for RoleData class."""

    pass


class BuilderRole(Role):
    """Access and manage BotC role data."""

    roles: dict[str, Role] = {}

    def __init__(self, json_role_info: list, stylize: bool = True):
        """Initialize the RoleData object."""

        self.incoming_data = json_role_info

        # if we weren't given a list of files we'll throw an error
        if not json_role_info:
            raise RoleDataException("No data files provided")

        # loop through the role data
        for role_data in json_role_info:
            # create a Role object
            role = Role(role_data)

            # store the role in our dict
            self.roles[role.id_slug] = role

        # we need to set first and other night positions for all roles
        self._set_night_positions()

    def _set_night_positions(self) -> None:
        # get the night order data
        night_order = self._get_night_order()

        first_night_order_by_name: dict[str, int] = {}
        other_night_order_by_name: dict[str, int] = {}

        # loop through firstNight, with the index as the position
        for index, role_id in enumerate(night_order["firstNight"]):
            night_position = index + 1
            # store the position in a dict
            first_night_order_by_name[role_id] = night_position

        # loop through otherNight, with the index as the position
        for index, role_id in enumerate(night_order["otherNight"]):
            night_position = index + 1
            # store the position in a dict
            other_night_order_by_name[role_id] = night_position

        # this might not be perfect but we aren't running real time
        # so it's probably fine...
        # loop through the roles
        for role in self.roles.values():
            # if we have a first night position, set it
            if role.name in first_night_order_by_name:
                role.first_night_position = first_night_order_by_name[role.name]
            else:
                # set to None
                role.first_night_position = None

            # if we have an other night position, set it
            if role.name in other_night_order_by_name:
                role.other_night_position = other_night_order_by_name[role.name]
            else:
                # set to None
                role.other_night_position = None

            # we only need DAWN, DUSK, DEMON, MINION as names until we've
            # worked out the night order
            # we should generalise this properly later, but for now
            if role.name == "DEMON":
                role.name = "Demon Night Info"
            elif role.name == "MINION":
                role.name = "Minion Night Info"

            # replace the role in the dict
            self.roles[role.id_slug] = role

    def _get_night_order(self):
        """Get the night order data from the JSON file."""
        with open("data/external/script-nightorder.json", encoding="utf-8") as fhandle:
            night_order = json.load(fhandle)
        return night_order
