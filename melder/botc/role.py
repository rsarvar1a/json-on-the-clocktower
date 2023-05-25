from typing import Any, Optional


class Role:
    """Access and manage BotC role data."""

    def __init__(self, role_data: dict, stylize: bool = True):
        """Initialize a role."""

        # we expect these to always exist, so we don't need .get()
        try:
            self.id_slug: str = role_data["id"]
        except:
            print(role_data)
            raise
        self.name: str = role_data["name"]
        self.team: str = role_data["team"]
        self.first_night_reminder: str = role_data["firstNightReminder"]
        self.other_night_reminder = role_data.get("otherNightReminder", "")
        self.reminders = role_data.get("reminders", [])
        self.setup = role_data.get("setup", False)
        self.first_night_position: Optional[int] = role_data.get("firstNight", None)
        self.other_night_position: Optional[int] = role_data.get("otherNight", None)
        self.jinxes = role_data.get("jinxes", [])

        # we need to know if we're stylizing or not before we can store the
        # ability
        self.stylized = stylize
        # store the original ability, and stylize it if we're supposed to
        self.original_ability = role_data["ability"]
        if stylize:
            self.ability_styled = self.stylize(role_data["ability"])

        # optional (e.g. fabled roles don't have an edition)
        # although we do expect to use our own data to fill any gaps
        self.edition = role_data.get("edition", None)

    def as_json(self) -> dict[str, Any]:
        """Return the role as a JSON object."""
        return {
            "id": self.id_slug,
            "name": self.name,
            "team": self.team,
            "firstNightReminder": self.first_night_reminder,
            "otherNightReminder": self.other_night_reminder,
            "reminders": self.reminders,
            "setup": self.setup,
            "firstNight": self.first_night_position,
            "otherNight": self.other_night_position,
            "jinxes": self.jinxes,
            "ability": self.original_ability,
            "edition": self.edition,
        }

    def __str__(self):
        # build up night order info, if we have it
        night_order = ""
        if self.first_night_position is not None and self.first_night_position > 0:
            night_order += f"first_night_position={self.first_night_position}"
        if self.other_night_position is not None and self.other_night_position > 0:
            # if we already have a first night position, we'll add a comma
            if night_order:
                night_order += ", "
            night_order += f"other_night_position={self.other_night_position}"
        # if we have a night order, prefix it with a comma and a space
        if night_order:
            night_order = f", {night_order}"

        # jinxes, if we don't have them (empty list) strigify as 'None'
        if not self.jinxes:
            jinxes = "None"

        # pylint: disable=line-too-long
        return f"Role(name='{self.name}', id_slug='{self.id_slug}', team='{self.team}', edition='{self.edition}', jinxes={jinxes}{night_order})"

    # it's a bit clunkier than we'd like, but it's better than nothing at all
    def stylize(self, text: str) -> str:
        """Stylize a string of text for HTML/PDF rendering"""
        if not self.stylized:
            return text

        # this looks weird to me, and as we fetch this data from the json
        # we modify it here to suit our desired
        text = text.replace(
            "[Most players are Legion]",
            "&nbsp;<strong>[Most players are Legion]</strong>",
        )
        text = text.replace(
            "(Travellers don’t count)",
            "&nbsp;<strong>[Travellers don’t count]</strong>",
        )
        text = text.replace(
            "(not yourself)",
            "&nbsp;<strong>[not yourself]</strong>",
        )
        text = text.replace(
            "[1 Townsfolk is evil]",
            "&nbsp;<strong>[1 Townsfolk is evil]</strong>",
        )

        # replace '[+N Outsider]' with '<strong>[+N Outsider]</strong>'
        text = text.replace("[+", "&nbsp; <strong>[+")
        # the next two likes look visually similar, but are different
        # the json appears to have a unicode minus sign
        text = text.replace("[-", "&nbsp; <strong>[-")
        text = text.replace("[\u2212", "&nbsp; <strong>[-")

        # and close
        text = text.replace("]", "]</strong>")

        return text
