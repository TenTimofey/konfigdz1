def cmd_ls(vfs, args, logger):
    items = vfs.list_dir()
    logger.log(f"ls executed, items: {items}")
    return "\n".join(items)

def cmd_cd(vfs, args, logger):
    if len(args) < 1:
        return "cd: missing argument"
    try:
        vfs.change_dir(args[0])
        logger.log(f"cd executed, new path: {vfs.current_path}")
    except FileNotFoundError as e:
        return str(e)
    return ""

def cmd_du(vfs, args, logger):
    size = vfs.disk_usage()
    logger.log(f"du executed, size: {size} bytes")
    return f"{size} bytes"

def cmd_exit(vfs, args, logger):
    logger.log("exit executed")
    return "exit"