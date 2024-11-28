import sys
from config import parse_config
from filesystem import VirtualFileSystem
from logger import Logger
from commands import cmd_ls, cmd_cd, cmd_du, cmd_exit

COMMANDS = {'ls': cmd_ls, 'cd': cmd_cd, 'du': cmd_du, 'exit': cmd_exit}

def main(config_path):
    config = parse_config(config_path)
    vfs = VirtualFileSystem(config['fs_path'])
    logger = Logger(config['log_path'])

    try:
        while True:
            cmd_input = input(f"{config['hostname']}:{vfs.current_path}$ ").strip()
            if not cmd_input:
                continue
            parts = cmd_input.split()
            cmd = parts[0]
            args = parts[1:]

            if cmd in COMMANDS:
                output = COMMANDS[cmd](vfs, args, logger)
                if output == "exit":
                    break
                if output:
                    print(output)
            else:
                print(f"{cmd}: command not found")
    finally:
        logger.save()