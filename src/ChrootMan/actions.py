from termcolor import colored
from .helpers import (
    chkMountStatus,
    findLocation,
    getChrootCommand,
    ensureMount,
    suRunCommand,
)
import logging


def help(config_data, args):
    print(f"{colored('run', 'yellow')} {colored('chrootman', 'green')} -h for help")
    logging.debug(f"Arg not specified: {config_data}, {args}")


def list(config_data, args):
    logging.debug(f"Arg is not used {args}")
    print(f"{colored('Available','green')} {colored('chroots', 'yellow')}:")
    for item in config_data["chroots"]:
        print(colored(item, "yellow"))


# Show info of specified chroot
def showinfo(config_data, args):
    chroot_name = args["chroot_name"]
    print(f"{colored('Name','green')}: \t\t{colored(chroot_name, 'yellow')}")
    try:
        print(
            f"{colored('Description', 'green')}: \t{colored(config_data['chroots'][chroot_name]['description'], 'yellow')}"
        )
    except:
        logging.warn("Description not found, skipping")
    print(
        f"{colored('Location', 'green')}: \t{colored(findLocation(config_data, chroot_name), 'yellow')}"
    )
    print(
        f"{colored('Distro', 'green')}: \t{colored(config_data['chroots'][chroot_name]['distro'], 'yellow')}"
    )


# Execute mount-command from settings
def mount(config_data, args, chroot_name=None):
    if not chroot_name:
        chroot_name = args["chroot_name"]
    if chkMountStatus(config_data, chroot_name):
        logging.error(f"{chroot_name} is already mounted.")
        exit(1)
    su_provider = config_data["general"]["su-provider"]
    distro = config_data["chroots"][chroot_name]["distro"]

    # check whether to use default or not
    mount_command = getChrootCommand(config_data, "mount-command", distro, chroot_name)
    suRunCommand(config_data, chroot_name, su_provider, mount_command, "mount_command")


def unmount(config_data, args):
    chroot_name = args["chroot_name"]
    su_provider = config_data["general"]["su-provider"]
    distro = config_data["chroots"][chroot_name]["distro"]

    if not chkMountStatus(config_data, chroot_name):
        logging.error(f"{chroot_name} is not mounted.")
        exit(1)

    unmount_command = getChrootCommand(
        config_data,
        "unmount-command",
        distro,
        chroot_name,
    )
    suRunCommand(
        config_data, chroot_name, su_provider, unmount_command, "unmount_command"
    )


def login(config_data, args):
    chroot_name = args["chroot_name"]

    if ensureMount(config_data, chroot_name, args, mount, login):
        return

    su_provider = config_data["general"]["su-provider"]
    distro = config_data["chroots"][chroot_name]["distro"]

    login_command = getChrootCommand(config_data, "login-command", distro, chroot_name)
    suRunCommand(config_data, chroot_name, su_provider, login_command, "login-command")


def launch(config_data, args):
    chroot_name = args["chroot_name"]

    if ensureMount(config_data, chroot_name, args, mount, launch):
        return

    su_provider = config_data["general"]["su-provider"]
    distro = config_data["chroots"][chroot_name]["distro"]
    launch_command = getChrootCommand(
        config_data, "launch-command", distro, chroot_name
    )
    suRunCommand(config_data, chroot_name, su_provider, launch_command, "login-command")

    unmount(config_data, args)


def updateChroot(config_data, args):
    chroot_name = args["chroot_name"]
    su_provider = config_data["general"]["su-provider"]
    distro = config_data["chroots"][chroot_name]["distro"]
    update_command = getChrootCommand(
        config_data, "update-command", distro, chroot_name
    )

    if ensureMount(config_data, chroot_name, args, mount, updateChroot):
        return

    suRunCommand(
        config_data, chroot_name, su_provider, update_command, "update_command"
    )


def update(config_data, args):
    if not args["chroot_name"]:
        logging.debug("chroot_name arg is not found")
        if not args["all"]:
            print(
                f"{colored('chroot_name', 'yellow')} not specified, assuming {colored('--all', 'green')}"
            )

        for chroot in config_data["chroots"]:
            print(f" {colored('Updating', 'green')}: {colored(chroot, 'yellow')}")
            args["chroot_name"] = chroot
            updateChroot(config_data, args)

    else:
        logging.debug(f"Updating {args['chroot_name']}")
        updateChroot(config_data, args)
