import logging
import sys
from typing import Annotated, Optional, TypeAlias, List

import inquirer
import rich
import typer
from rich import print as rprint

from deploy import deploy_commands
from keepass import KeepassDB, get_all_devices, does_device_exist, remove_device
from device_list import get_device_list
from __init__ import COMMANDER_DIRECTORY, KEEPASS_DB_PATH
from init import is_initialized, init_program, delete_project_files
from recruit_device import recruit_device

logger = logging.Logger("commander")
logging.basicConfig(level=logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel("INFO")
logger.addHandler(handler)

app = typer.Typer(pretty_exceptions_show_locals=False)

device_entry_type: TypeAlias = dict[str, str | dict[str, str]]


def commands_reader(command_file_path):
    with open(command_file_path) as commands_file:
        commands = commands_file.readlines()
        commands = [command.strip("\n ") for command in commands]
        commands = filter(lambda command: is_valid_command(command), commands)
        commands = list(commands)
    return commands


def is_valid_command(command: str):
    if not command:
        return False
    if command[0] == '#':
        return False
    return True


@app.command(help="deploy command to all the devices in your database")
def deploy(
        command_file: Optional[typer.FileText] = None,
        command_list: Annotated[Optional[List[str]], typer.Option()] = None,
        permission_level: str = "user"
):
    if not is_initialized(COMMANDER_DIRECTORY, KEEPASS_DB_PATH):
        logger.error("program is not initialized! please run commander init!")
        return
    all_commands = []
    if command_file:
        striped_command_file = [command.strip("\n ") for command in command_file]
        all_commands += striped_command_file

    if command_list:
        all_commands += command_list

    if not command_list and not command_file:
        rich.print("you cant deploy to devices without any commands. enter a command in the terminal!")
        exit(1)

    valid_commands = filter(is_valid_command, all_commands)
    commands = list(valid_commands)
    rich.print("commands: \n" + '\n'.join(commands))

    with KeepassDB(KEEPASS_DB_PATH) as kp:
        devices = get_all_devices(kp)
    rich.print("devices: \n" + '\n'.join(map(str, devices)))
    typer.confirm(f"are you sure you want to deploy {len(commands)} commands on {len(devices)}?", abort=True)
    deploy_commands(commands, devices, permission_level, logger)


@app.command(name="list", help="list all the devices in your command")
def list_devices():
    if not is_initialized(COMMANDER_DIRECTORY, KEEPASS_DB_PATH):
        logger.error("program is not initialized! please run commander init!")
        return

    device_list = get_device_list(KEEPASS_DB_PATH)
    logger.info(device_list)


@app.command(help="add a device to the list of devices")
def recruit(file: Annotated[Optional[str], typer.Argument()] = None):
    if not is_initialized(COMMANDER_DIRECTORY, KEEPASS_DB_PATH):
        init_program(COMMANDER_DIRECTORY, KEEPASS_DB_PATH)
    recruit_device(file, KEEPASS_DB_PATH, logger)


@app.command(help="remove a device from list")
def remove(devices: Annotated[Optional[List[str]], typer.Option("--device")] = None):
    with KeepassDB(KEEPASS_DB_PATH) as kp:
        if not devices:
            all_devices = get_all_devices(kp)
            all_device_names = [device.name for device in all_devices]
            devices = inquirer.checkbox(message="which devices do you want to remove?", choices=all_device_names)
        # find all the non-existent devices
        non_existing_devices = list(filter(lambda device: not does_device_exist(device, kp), devices))
        if non_existing_devices:
            for device_name in non_existing_devices:
                logger.error(f"device {device_name} doesn't exist so it can't be deleted")
            return
        rprint(devices)
        typer.confirm(f"are you sure you want to delete {len(devices)} devices?", abort=True)
        for device_name in devices:
            remove_device(device_name, kp)


@app.command(help="initialize the project")
def init():
    rich.print("Welcome to commander!")
    if is_initialized(COMMANDER_DIRECTORY, KEEPASS_DB_PATH):
        rich.print("commander is already initialized")
        reinitialize: bool = typer.confirm("do you want to delete everything and start over?")
        if reinitialize:
            rich.print(f"deleting directory: {COMMANDER_DIRECTORY}")
            delete_project_files(COMMANDER_DIRECTORY)
    if not is_initialized(COMMANDER_DIRECTORY, KEEPASS_DB_PATH):
        rich.print(f"creating new database in {COMMANDER_DIRECTORY}")
        init_program(COMMANDER_DIRECTORY, KEEPASS_DB_PATH)

    rich.print("finished the initialization process, have a great day")


def main():
    app()


if __name__ == '__main__':
    main()
