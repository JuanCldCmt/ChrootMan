import subprocess
from os import environ
from logging import debug, error
from termcolor import colored


def cliAskChoice():
    yes = {"yes", "yep", "y", "ye", ""}
    no = {"no", "nope", "n"}

    choice = input(f"{colored('Input', 'blue')}: ({colored('y','green')}/{colored('n', 'red')}) > ").lower()
    debug("input is:" + choice)
    if choice in yes:
        debug("Choice is yes")
        return True
    elif choice in no:
        debug("Choice is no")
        return False
    else:
        print(f" Please respond with '{colored('y', 'green')}' or '{colored('n', 'red')}'")
        return cliAskChoice()


def findLocation(config_data, chroot_name):
    if not validChrootName(config_data, chroot_name):
        exit(1)

    if "custom-location" not in config_data["chroots"][chroot_name]:
        return (
            config_data["general"]["unified-location"]
            + config_data["chroots"][chroot_name]["location"]
        )
    else:
        return config_data["chroots"][chroot_name]["custom-location"]


def validChrootName(config_data, chroot_name):
    if chroot_name not in config_data["chroots"]:
        error(f"{chroot_name} is not in the configuration file!")
        error(f"Available options are: {list(config_data['chroots'])}")
        return False
    else:
        return True


def getChrootCommand(config_data, command_name, distro = None, chroot_name = None):
    # chroots-settings -> distro-settings -> default-distro-settings
    debug(f"distro: {distro}, chroot_name: {chroot_name}, command_name: {command_name}")
    try:
        command = config_data["chroots"][chroot_name][command_name]
    except KeyError:
        try:
            command = config_data["general"]["distro-settings"][distro][command_name]
        except KeyError:
            try:
                debug("distro is not in configured list, using default")
                command = config_data["general"]["distro-settings"]["default"][command_name]
            except KeyError:
                error("KeyError: Make sure you have properly configured the chroots")
                exit(1)

    command = command.replace(
        "$rootfs_location", findLocation(config_data, chroot_name)
    )
    command = command.replace("~", environ["HOME"])
    debug(f"Command loaded:\n{command}")
    return command


def ensureMount(config_data, chroot_name, args, mount_func, command_func):
    if not chkMountStatus(config_data, chroot_name):
        error("Filesystem is not mounted! Do you want to mount it first?")
        if cliAskChoice():
            mount_func(config_data, args)
            command_func(config_data, args)
            return True
    return False


def chkMountStatus(config_data, chroot_name):
    chrootPath = findLocation(config_data, chroot_name).replace("~", environ["HOME"])
    output = subprocess.run(["mount"], capture_output=True).stdout
    if chrootPath in str(output):
        return True
    else:
        return False


def suRunCommand(config_data, chroot_name, su_provider, command, command_type):
    if validChrootName(config_data, chroot_name):
        print(f"→ {colored('Executing', 'green')} {colored(command_type, 'yellow')}")
        child = subprocess.run([su_provider, "sh", "-c", command])
        print(f"⏎ {colored(command_type, 'yellow')} executed and returned {colored(str(child.returncode), 'magenta')}")
