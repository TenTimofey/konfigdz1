import xml.etree.ElementTree as ET

def parse_config(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    config = {
        'hostname': root.find('hostname').text,
        'fs_path': root.find('filesystem').text,
        'log_path': root.find('log').text,
        'startup_script': root.find('startup_script').text,
    }
    return config