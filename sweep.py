# -*- coding: utf-8 -*-
__author__ = 'Denis Vesnin, https://github.com/Aeromg'

import os, argparse, time, datetime, stat, re

def walk_path(path, func, recursive=False, follow=False, allow_head=True):
    for step in os.listdir(path):
        cur_path = os.path.join(path, step)
        if not follow and os.path.islink(cur_path):
            continue

        if recursive and os.path.isdir(cur_path):
            walk_path(cur_path, func, recursive=recursive, follow=follow, allow_head=False)

        if os.path.exists(cur_path):
            func(cur_path)

    if allow_head:
        func(path)

def rmdir(path):
    if len(os.listdir(path)) == 0:
        os.rmdir(path)
        return True

    return False

def remove(path):
    os.remove(path)

def unlink(path):
    os.unlink(path)

def kill_path(path):
    file_stat = os.stat(path)
    file_st_mode = file_stat.st_mode

    if stat.S_ISLNK(file_st_mode):
        unlink(path)
    elif stat.S_ISDIR(file_st_mode):
        return rmdir(path)
    elif stat.S_ISREG(file_st_mode):
        remove(path)
    else:
        return False

    return True

def test_path(path, accessed, modified, allow_unlink, allow_rmdir, collect_empty):
    file_stat = os.stat(path)
    file_st_mode = file_stat.st_mode

    if collect_empty and allow_rmdir and stat.S_ISDIR(file_st_mode) and len(os.listdir(path)) == 0:
        return True

    if file_stat.st_mtime <= modified or file_stat.st_atime <= accessed:
        if not allow_unlink and stat.S_ISLNK(file_st_mode):
            return False

        elif not allow_rmdir and stat.S_ISDIR(file_st_mode):
            return False

        else:
            return True

    return False

def modified_or_print(path, accessed, modified, allow_unlink, allow_rmdir, collect_empty):
    if test_path(path, accessed, modified, allow_unlink, allow_rmdir, collect_empty):
        print(path)

def modified_or_append(path, accessed, modified, allow_unlink, allow_rmdir, to_kill, collect_empty):
    if test_path(path, accessed, modified, allow_unlink, allow_rmdir, collect_empty):
        to_kill.append(path)

def main():
    parser = argparse.ArgumentParser(description='collect outdated files and folders.')
    parser.add_argument('-r', '--recursive', action='store_true', default=False, help='do recursive search')
    parser.add_argument('-b', '--allow-root', action='store_true', default=False, help='allow process root path')
    parser.add_argument('-f', '--follow', action='store_true', default=False, help='follow symlinks')
    parser.add_argument('-l', '--allow-link', action='store_true', default=False, help='allow process symlinks')
    parser.add_argument('-s', '--allow-dir', action='store_true', default=False, help='allow process directories')
    parser.add_argument('-d', '--delete', action='store_true', default=False, help='delete each file instead of displaying its path')
    parser.add_argument('-e', '--collect-empty', action='store_true', default=False, help='collect empty directories')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='echo each deleted file path to stdout')
    parser.add_argument('-m', '--modified', type=int, required=False, default=-1, metavar='SECONDS', help='seconds from last modifying')
    parser.add_argument('-a', '--accessed', type=int, required=False, default=-1, metavar='SECONDS', help='seconds from last access')
    parser.add_argument('-p', '--path', type=str, required=True, metavar='PATH', help='path for collect')
    parser.add_argument('-t', '--test-regex', type=str, required=False, metavar='REGEX', help='test regex for each entry')
    args = parser.parse_args()

    start_path = args.path
    if re.match('^".*"$', start_path):
        start_path = re.findall('(?<=^").*(?="$)'), start_path[0]

    if not os.path.exists(start_path):
        print('Path "{0}" not found'.format(start_path))
        return 1

    if args.accessed == -1 and args.modified == -1:
        print('At least one of modifying or accessed time must be set')
        return 1

    test_regex = re.compile(args.test_regex, re.UNICODE + re.IGNORECASE) if args.test_regex else None
    accessed = time.mktime(datetime.datetime.now().timetuple()) - args.accessed if args.accessed > 0 else 0
    modified = time.mktime(datetime.datetime.now().timetuple()) - args.modified if args.modified > 0 else 0
    verbose = args.verbose
    delete = args.delete
    allow_link = args.allow_link
    allow_dir = args.allow_dir
    recursive = args.recursive
    follow = args.follow
    allow_root = args.allow_root
    collect_empty = args.collect_empty

    list_to_kill = list()

    def func(path):
        if test_regex and not test_regex.match(path):
            return
            
        if delete:
            modified_or_append(path, accessed, modified, allow_link, allow_dir, list_to_kill, collect_empty)
        else:
            modified_or_print(path, accessed, modified, allow_link, allow_dir, collect_empty)

    walk_path(start_path, func, recursive, follow, allow_root)

    if delete:
        for path_to_kill in list_to_kill:
            if kill_path(path_to_kill):
                if verbose:
                    print("Removed: {0}".format(path_to_kill))

    return 0

if __name__ == "__main__":
    errcode = main()
    exit(errcode)
