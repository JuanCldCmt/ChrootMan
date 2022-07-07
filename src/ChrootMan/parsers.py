import argparse
import os

# logging
import logging
import yaml

# functionality
from .actions import *
from os import environ
from .helpers import cliAskChoice
from shutil import copy


class custom_formatter(logging.Formatter):
    cyan = "\x1b[36m"
    blue = "\x1b[34m"
    yellow = "\x1b[33m"
    red = "\x1b[31m"
    reset = "\x1b[0m"

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.cyan + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.red + self.fmt + self.reset,
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def add_subcommands(subparsers):
    # add parsers for subcommands
    list_parser = subparsers.add_parser("list", help="Display availble chroots")
    list_parser.set_defaults(func=list)

    info_parser = subparsers.add_parser(
        "info", help="Display information on specified chroot"
    )
    info_parser.add_argument("chroot_name", type=str, help="specify the name of chroot")
    info_parser.set_defaults(func=showinfo)

    mount_parser = subparsers.add_parser(
        "mount", help="Mount filesystem of specified chroot"
    )
    mount_parser.add_argument(
        "chroot_name", type=str, help="specify name of chroot to mount"
    )
    mount_parser.set_defaults(func=mount)

    unmount_parser = subparsers.add_parser(
        "unmount", help="unmount filesystem of specified chroot"
    )
    unmount_parser.add_argument(
        "chroot_name", type=str, help="specify name of chroot to unmount"
    )
    unmount_parser.set_defaults(func=unmount)

    login_parser = subparsers.add_parser("login", help="login to specified chroot")
    login_parser.add_argument(
        "chroot_name", type=str, help="specify name of chroot to login"
    )
    login_parser.set_defaults(func=login)

    update_parser = subparsers.add_parser("update", help="update to specified chroot")
    update_parser.add_argument(
        "chroot_name",
        nargs="?",
        type=str,
        help="specify name of chroot to update",
    )
    update_parser.add_argument("--all", "-a", action="store_true")
    update_parser.set_defaults(func=update)


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

    add_subcommands(subparsers)
    # argument
    args = parser.parse_args()

    # set up debugger
    logger = logging.getLogger()
    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.ERROR)

    log = logging.StreamHandler()
    fmt = "%(levelname)s: %(message)s"
    log.setFormatter(custom_formatter(fmt))

    logger.addHandler(log)

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
            else:
                path = os.path.dirname(os.path.abspath(__file__))

            copy(f"{path}/files/config.yaml", config_location)

            logging.debug("Installed default config file.")
            return parse_conf()
        else:
            logging.error("A configuration file is required.")
            logging.debug("Exitting...")
            exit()
