import json
from typing import Optional
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
            # print(f"Loaded role: {role.name} ({role.id_slug})")

            # store the role in our dict
            self.roles[role.id_slug] = role
