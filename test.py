import pytest
from filesystem import VirtualFileSystem

@pytest.fixture
def vfs():
    return VirtualFileSystem("test_fs.tar")

def test_ls(vfs):
    assert "file1.txt" in vfs.list_dir()

def test_cd(vfs):
    vfs.change_dir("subdir")
    assert vfs.current_path == "/subdir"