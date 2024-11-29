import shutil
import unittest
import os
import tarfile
import json
from main import ShellEmulator

class TestShellEmulator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Создаем временные файлы для тестов
        os.makedirs("test_fs/home/user", exist_ok=True)
        with open("test_fs/home/user/file1.txt", "w") as f:
            f.write("File 1 content")
        with open("test_fs/home/user/file2.txt", "w") as f:
            f.write("File 2 content")
        with tarfile.open("test_fs.tar", "w") as tar:
            tar.add("test_fs", arcname=".")

        # Создаем конфигурационный файл
        with open("config.xml", "w") as f:
            f.write("""<config>
                <hostname>test_machine</hostname>
                <fs_archive>test_fs.tar</fs_archive>
                <log_file>test_log.json</log_file>
                <startup_script>test_startup.sh</startup_script>
            </config>""")

        # Создаем пустой лог-файл и стартовый скрипт
        with open("test_log.json", "w") as f:
            json.dump([], f)
        with open("test_startup.sh", "w") as f:
            f.write("cd home/user\nls\n")

    @classmethod
    def tearDownClass(cls):
        # Удаляем временные файлы
        os.remove("test_fs.tar")
        os.remove("config.xml")
        os.remove("test_log.json")
        os.remove("test_startup.sh")
        shutil.rmtree("test_fs", ignore_errors=True)
        shutil.rmtree("/tmp/virtual_fs", ignore_errors=True)

    def setUp(self):
        self.emulator = ShellEmulator("config.xml")

    def tearDown(self):
        del self.emulator

    def test_ls_command(self):
        # Тест команды ls
        self.emulator.cwd = os.path.join(self.emulator.fs_root, "home/user")
        self.emulator.ls()
        self.assertIn("file1.txt", os.listdir(self.emulator.cwd))
        self.assertIn("file2.txt", os.listdir(self.emulator.cwd))

    def test_cd_command_valid(self):
        # Тест успешного выполнения cd
        self.emulator.cd("home/user")
        expected_path = os.path.join(self.emulator.fs_root, "home/user")
        self.assertEqual(self.emulator.cwd, expected_path)

    def test_cd_command_invalid(self):
        # Тест cd с несуществующей директорией
        with self.assertRaises(FileNotFoundError):
            self.emulator.cd("invalid_dir")

    def test_mv_command(self):
        # Тест mv
        self.emulator.cd("home/user")
        self.emulator.mv("file1.txt", "file1_moved.txt")
        self.assertTrue(os.path.exists(os.path.join(self.emulator.cwd, "file1_moved.txt")))
        self.assertFalse(os.path.exists(os.path.join(self.emulator.cwd, "file1.txt")))

    def test_du_command(self):
        # Тест du
        self.emulator.cd("home/user")
        self.emulator.du()
        total_size = sum(
            os.path.getsize(os.path.join(root, file))
            for root, _, files in os.walk(self.emulator.cwd)
            for file in files
        )
        self.assertIn(f"Total size: {total_size} bytes", self.emulator.log[-1]["result"])

    def test_exit_command(self):
        # Тест exit
        with self.assertRaises(SystemExit):
            self.emulator.exit_shell()

    def test_startup_script(self):
        # Тест выполнения стартового скрипта
        self.emulator.run_startup_script()
        expected_path = os.path.abspath(os.path.join(self.emulator.fs_root, "home/user"))
        self.assertEqual(self.emulator.cwd, expected_path)

    def test_log_creation(self):
        # Тест создания логов
        self.emulator.ls()
        self.emulator.cd("home/user")
        self.emulator.du()
        with open("test_log.json", "r") as f:
            logs = json.load(f)
        self.assertEqual(len(logs), 3)
        self.assertEqual(logs[0]["action"], "ls")
        self.assertEqual(logs[1]["action"], "cd home/user")
        self.assertTrue("du" in logs[2]["action"])

if __name__ == "__main__":
    unittest.main()
