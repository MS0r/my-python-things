import os
import shutil
import sys
import re


def get_dirs(source):
    dirs_path = []
    for root, dirs, files in os.walk(source):
        for directory in dirs:
            dirs_path.append(directory)
        dirs_path.extend(files)
        break

    return dirs_path


def copy_all(source, dest):
    if re.match('[a-zA-Z0-9_%+-]*\.[a-z]{1,3}', os.path.basename(source)) == None:
        if os.path.exists(dest):
            shutil.rmtree(dest)
        shutil.copytree(source, dest)
    else:
        shutil.copyfile(source, dest)


def create_dir(target):
    if not os.path.exists(target):
        os.mkdir(target)


def main(source, target):
    cwd = os.getcwd()
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    source_path = os.path.join(cwd, source)
    target_path = os.path.join(desktop_path, target)

    create_dir(target_path)
    dirs_name = get_dirs(source_path)

    for d in dirs_name:
        copy = os.path.join(source_path, d)
        paste = os.path.join(target_path, d)
        copy_all(copy, paste)


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        raise Exception("You must pass source and target directory - only")
    source, target = args[1:]
    main(source, target)
