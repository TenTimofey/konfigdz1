import os
import tarfile
import xml.etree.ElementTree as ET
import json
import time
import shutil

class ShellEmulator:
    def __init__(self, config_path):
        self.load_config(config_path)
        self.cwd = self.fs_root  # Текущая директория
        self.log = []
        self.run_startup_script()

    def load_config(self, config_path):
        tree = ET.parse(config_path)
        root = tree.getroot()

        self.hostname = root.find("hostname").text
        self.fs_archive = root.find("fs_archive").text
        self.log_file = root.find("log_file").text
        self.startup_script = root.find("startup_script").text

        # Используем текущую директорию для совместимости с Windows
        self.fs_root = os.path.normpath(os.path.join(os.getcwd(), "virtual_fs"))
        self.extract_fs()

    def extract_fs(self):
        if os.path.exists(self.fs_root):
            shutil.rmtree(self.fs_root)
        os.makedirs(self.fs_root, exist_ok=True)
        with tarfile.open(self.fs_archive, 'r') as tar:
            tar.extractall(self.fs_root)

    def log_action(self, action, result=""):
        entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "action": action,
            "result": result
        }
        self.log.append(entry)
        with open(self.log_file, "w") as log_file:
            json.dump(self.log, log_file, indent=4)

    def run_startup_script(self):
        if os.path.exists(self.startup_script):
            with open(self.startup_script, "r") as script:
                commands = script.readlines()
            for command in commands:
                self.execute_command(command.strip())

    def execute_command(self, command):
        parts = command.split()
        cmd = parts[0]
        args = parts[1:]

        try:
            if cmd == "ls":
                self.ls()
            elif cmd == "cd":
                self.cd(args[0] if args else "/")
            elif cmd == "mv":
                self.mv(args[0], args[1])
            elif cmd == "du":
                self.du()
            elif cmd == "exit":
                self.exit_shell()
            else:
                print(f"Unknown command: {cmd}")
        except Exception as e:
            print(f"Error: {e}")

    def ls(self):
        files = os.listdir(self.cwd)
        print("\n".join(files))
        self.log_action("ls", result="; ".join(files))

    def cd(self, path):
        new_path = os.path.normpath(os.path.abspath(os.path.join(self.cwd, path)))
        if os.path.exists(new_path) and os.path.isdir(new_path):
            self.cwd = new_path
            self.log_action(f"cd {path}", result=new_path)
        else:
            raise FileNotFoundError(f"No such directory: {path}")

    def mv(self, src, dest):
        src_path = os.path.join(self.cwd, src)
        dest_path = os.path.join(self.cwd, dest)
        shutil.move(src_path, dest_path)
        self.log_action(f"mv {src} {dest}")

    def du(self):
        total_size = sum(
            os.path.getsize(os.path.join(root, file))
            for root, _, files in os.walk(self.cwd)
            for file in files
        )
        print(f"Total size: {total_size} bytes")
        self.log_action("du", result=f"{total_size} bytes")

    def exit_shell(self):
        print("Exiting shell.")
        self.log_action("exit")
        exit(0)

    def start(self):
        print(f"Welcome to {self.hostname} shell emulator!")
        while True:
            command = input(f"{self.hostname}:{self.cwd}$ ")
            self.execute_command(command)

# Запуск эмулятора
if __name__ == "__main__":
    emulator = ShellEmulator("files/config.xml")
    emulator.start()
