#!/usr/bin/env python3
import logging
from .parsers import parse_args, parse_conf
from .helpers import validChrootName


def main():
    args = parse_args()
    config_data = parse_conf()
    logging.debug(f"Initialization complete.")

    # Validate chroot name
    try:
        chroot_name = vars(args)["chroot-name"]
        logging.debug("Validating chroot name")
        if not validChrootName(config_data, chroot_name):
            logging.debug("Chroot name is invalid, exitting")
            exit(2)
    except KeyError:
        # chroot name is not required
        pass

    # run program depending on what the arguments are
    logging.debug(f"Running with args {args}")
    args.func(config_data, vars(args))


if __name__ == "__main__":
    main()
