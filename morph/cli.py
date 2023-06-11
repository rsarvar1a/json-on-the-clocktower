""" Turn all the JSON data into One-JSON-To-Rule-Them-All"""


from morph.json.incoming import JsonIncoming
from morph.json.onetruejson import OneTrueJson


def combiner():
    """Turn all the JSON data into One-JSON-To-Rule-Them-All"""

    # create a new JsonIncoming object
    incoming = JsonIncoming()

    # create a new OneTrueJson object
    one_true_json = OneTrueJson(incoming)

    # write the data to a file
    one_true_json.write("data/generated/roles-combined-v2.json")
    one_true_json.write("data/generated/roles-combined.json")


if __name__ == "__main__":
    combiner()