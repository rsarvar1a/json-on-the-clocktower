""" Calculate the md5 checksum of all files in a directory. """
# a function to calculate the md5 checksum of all files in a directory
# and write to a file in that directory so we can compare later
import os

from hashlib import md5


def calculate_md5(directory: str) -> None:
    """Calculate the md5 checksum of all files in a directory."""

    md5sum_filename = "md5sum"

    # get a list of *.json files in the directory
    files = os.listdir(directory)
    # filter the list to only include *.json files
    files = [f for f in files if f.endswith(".json")]
    # sort the list
    files.sort()

    # create a dict to store the md5 checksums
    checksums = {}

    # loop through the files
    for file in files:
        # skip the md5 file
        if file == md5sum_filename:
            continue

        # get the full path to the file
        path = os.path.join(directory, file)

        # skip directories
        if os.path.isdir(path):
            continue

        # calculate the md5 checksum using hashlib.md5()
        # open the file in binary mode, readonly
        with open(path, "rb") as fhandle:
            # we know we aren't working with huge files, so we can read the
            # whole file, then calculate the checksum
            # read the whole file
            data = fhandle.read()
            # calculate the checksum
            checksum = md5(data).hexdigest()

        # add the checksum to the dict
        checksums[file] = checksum

    # write the checksums to a file
    with open(
        os.path.join(directory, md5sum_filename), "w", encoding="utf-8"
    ) as fhandle:
        # format should be: checksum filename
        for filename, checksum in checksums.items():
            fhandle.write(f"{checksum} {filename}\n")


if __name__ == "__main__":
    calculate_md5("data/external")
