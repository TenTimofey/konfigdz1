import tarfile
import os

# Создать структуру виртуальной ФС
os.makedirs("virtual_fs/home/user/documents", exist_ok=True)
with open("virtual_fs/home/user/documents/file1.txt", "w") as f:
    f.write("Hello, World!")
with open("virtual_fs/home/user/documents/file2.txt", "w") as f:
    f.write("Sample text")

# Создать tar-архив
with tarfile.open("files/virtual_fs.tar", "w") as tar:
    tar.add("virtual_fs", arcname=".")

# Удалить исходную директорию
import shutil
shutil.rmtree("virtual_fs")