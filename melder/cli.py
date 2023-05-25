""" Turn all the JSON data into One-JSON-To-Rule-Them-All"""

import json
import os
from melder.botc.roledata import BuilderRole

from melder.util import fetch_remote_data, load_data


class RoleIdNotFoundException(Exception):
    """Exception for when a role id is not found in the role data"""

    pass


# fetch the remote data and save in data/external/
def _fetch_remote_data():
    remote_data = {
        "bra1n-roles": "https://raw.githubusercontent.com/bra1n/townsquare/develop/src/roles.json",
        "bra1n-fabled": "https://raw.githubusercontent.com/bra1n/townsquare/develop/src/fabled.json",
        "script-nightorder": "https://script.bloodontheclocktower.com/data/nightsheet.json",
        "script-jinx": "https://script.bloodontheclocktower.com/data/jinx.json",
    }

    for name, url in remote_data.items():
        # if we already have the file, skip it
        if os.path.exists(f"data/external/{name}.json"):
            print(f"Skipping {name} as it already exists")
            continue

        print(f"Fetching {name} from {url} …")
        data = fetch_remote_data(url)

        # make sure the directory exists
        os.makedirs("data/external", exist_ok=True)

        # write the data to a file
        with open(f"data/external/{name}.json", "w", encoding="utf-8") as fhandle:
            json.dump(data, fhandle, indent=4, sort_keys=True)


def _get_role_files() -> list[str]:
    # these are the main files with ROLE information in them
    role_files = [
        "data/external/bra1n-roles.json",
        "data/external/bra1n-fabled.json",
        "data/roles-nightmeta.json",
    ]
    # add anything in the extra-characters directory
    for filename in os.listdir("data/extra-characters"):
        if filename.endswith(".json"):
            role_files.append(f"data/extra-characters/{filename}")

    return role_files


def _combined_role_info():
    role_info = []
    for filename in _get_role_files():
        role_info.extend(load_data(filename))
    return role_info


def combiner():
    print("Combining JSON data into one file...")

    _fetch_remote_data()

    role_data = BuilderRole(_combined_role_info())

    # load our local role-edition mapping
    role_edition = load_data("data/role-edition.json")

    # loop through all the roles in the main json
    for role in role_data.incoming_data:
        role["firstNight"] = 0
        role["otherNight"] = 0

        # get the role data from our RoleData object
        role_info = role_data.roles.get(role["id"], None)

        # freak out if we don't have role data; throw an exception
        if not role_info:
            raise RoleIdNotFoundException(
                f"Role with id '{role['id']}' not found in role data"
            )

        # if we have role data, we'll use it to populate the night order data
        if role_data:
            role["firstNight"] = role_info.first_night_position
            role["otherNight"] = role_info.other_night_position
        else:
            print(f"Warning: role with id '{role['id']}' not found in role data")

        # get the edition for this role
        edition = role_edition.get(role["id"], "Unknown Edition")
        # if we already have an edition for this role, we'll warn and preserve the existing data
        if "edition" in role:
            # only warn if the edition is different, and not an empty string
            if role["edition"] != edition and role["edition"] != "":
                print(
                    f"role with id '{role['id']}' has edition '{role['edition']}' [role data], which is different to '{edition}' [manual file]"
                )
        # add the edition to the role
        role["edition"] = edition

        # get jinx information
        jinx_info = load_data("data/external/script-jinx.json")

    # we write the data out to a file with a couple of sections for options on
    # finding roles/information
    # - roles: a list of all the roles, as we're used to seeing them; this
    #   should include all the travelers, etc.
    character_data = {}
    edition_data = {}
    team_data = {}
    # loop through the roles, sorted by id
    for role in sorted(role_data.incoming_data, key=lambda x: x["id"]):
        # - characters: a way to get character info by "slug" (usually just lowercase name)
        character_data[role["id"]] = role

        # by edition: we don't need the full role data here, just the id and name
        # if it's None or empty, we'll add it to the "Unknown Edition" section
        if role["edition"] is None or role["edition"] == "":
            role["edition"] = "Unknown Edition"
        if role["edition"] not in edition_data:
            edition_data[role["edition"]] = []
        edition_data[role["edition"]].append({"id": role["id"], "name": role["name"]})

        # by team: we don't need the full role data here, just the id and name
        # if it's None or empty, we'll print a warning and add it to the "Unknown Team" section
        if role["team"] is None or role["team"] == "":
            print(f"Warning: role with id '{role['id']}' has no team")
            role["team"] = "Unknown Team"
        if role["team"] not in team_data:
            team_data[role["team"]] = []
        team_data[role["team"]].append({"id": role["id"], "name": role["name"]})

    file_data = {
        "role_list": role_data.incoming_data,
        "character_by_id": character_data,
        "editions": edition_data,
        "teams": team_data,
        "jinxes": jinx_info,
    }

    print("Writing combined JSON data to roles-combined.json …")
    # make sure the directory exists
    os.makedirs("data/generated", exist_ok=True)
    with open("data/generated/roles-combined.json", "w", encoding="utf-8") as fhandle:
        json.dump(file_data, fhandle, indent=4, sort_keys=True)


if __name__ == "__main__":
    combiner()
