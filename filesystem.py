import tarfile
import os

class VirtualFileSystem:
    def __init__(self, fs_path):
        self.fs_path = fs_path
        self.current_path = "/"
        self.tar = tarfile.open(fs_path, 'r')

    def list_dir(self, path=None):
        path = path or self.current_path
        members = [m.name for m in self.tar.getmembers() if m.name.startswith(path) and m.name != path]
        return set(os.path.relpath(m, path).split('/')[0] for m in members)

    def change_dir(self, path):
        new_path = os.path.normpath(os.path.join(self.current_path, path))
        if not any(m.name == new_path + '/' for m in self.tar.getmembers()):
            raise FileNotFoundError(f"Directory {new_path} not found.")
        self.current_path = new_path

    def disk_usage(self, path=None):
        path = path or self.current_path
        members = [m for m in self.tar.getmembers() if m.name.startswith(path)]
        return sum(m.size for m in members)

    def move(self, src, dst):
        raise NotImplementedError("Move operation not supported in read-only tar.")