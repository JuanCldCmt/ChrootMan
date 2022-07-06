import argparse
import os
import logging
import yaml
from .actions import *
from os import environ
from .helpers import cliAskChoice
from shutil import copy

# read args and set up debugger based on flags
def parse_args():
    parser = argparse.ArgumentParser(description="Manage chroot instances")
    parser.set_defaults(func=help)

    parser.add_argument(
        "-d",
        "--debug",
        help="Increase output verbosity to display dibugging messages",
        action="store_true",
    )

    subparsers = parser.add_subparsers(title="available subcommands")

    # add parsers for subcommands
    info_parser = subparsers.add_parser(
        "info", help="Display information on specified chroot"
    )
    info_parser.add_argument("chroot-name", type=str, help="specify the name of chroot")
    info_parser.set_defaults(func=showinfo)

    mount_parser = subparsers.add_parser(
        "mount", help="Mount filesystem of specified chroot"
    )
    mount_parser.add_argument(
        "chroot-name", type=str, help="specify name of chroot to mount"
    )
    mount_parser.set_defaults(func=mount)

    unmount_parser = subparsers.add_parser(
        "unmount", help="unmount filesystem of specified chroot"
    )
    unmount_parser.add_argument(
        "chroot-name", type=str, help="specify name of chroot to unmount"
    )
    unmount_parser.set_defaults(func=unmount)

    login_parser = subparsers.add_parser(
        "login", help="login to specified chroot"
    )
    login_parser.add_argument(
        "chroot-name", type=str, help="specify name of chroot to login"
    )
    login_parser.set_defaults(func=login)

    # argument
    args = parser.parse_args()

    # set up debugger
    if args.debug:
        logging.basicConfig(level="DEBUG", format="%(levelname)s: %(message)s")
    else:
        logging.basicConfig(level="ERROR", format="%(levelname)s: %(message)s")

    logging.debug("Successfully parsed arguments")

    return args


def parse_conf():

    # Set config location based on Env vars
    config_location = environ.get("XDG_CONFIG_HOME")
    if not config_location:
        config_location = "~/.chrootman.yaml"
    else:
        config_location = config_location + "/chrootman/config.yaml"

    logging.debug(f"config_location is set to {config_location}")

    # Open file, otherwise return None
    try:
        f = open(config_location, mode="r")
        logging.debug("Reading file")
        config_data = yaml.load(f, Loader=yaml.CLoader)
        f.close()
        return config_data
    except:
        logging.warning("Config file not found!")
        logging.error(
            "Config file not found! Do you want to install a default configuration file?"
        )
        if cliAskChoice() == True:
            # path of the directory of script
            if not __file__:
                path = __path__
            else :
                path = os.path.dirname(os.path.abspath(__file__))

            copy(f"{path}/files/config.yaml", config_location)

            logging.debug("Installed default config file.")
            return parse_conf()
        else:
            logging.error("A configuration file is required.")
            logging.debug("Exitting...")
            exit()
