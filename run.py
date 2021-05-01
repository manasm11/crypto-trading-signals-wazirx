#!/usr/bin/python3
import pretty_errors
from sys import argv
import os


def test():
    os.system(f"python3 -m pytest tests " + " ".join(argv[2:]))


def help_():
    print(
        f"""
    USAGE: {argv[0]} [test|help]
    """
    )


if __name__ == "__main__":
    if len(argv) > 1:
        {"test": test, "help": help_}.get(argv[1], help_)()
    else:
        help_()
