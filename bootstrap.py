#!/usr/bin/env python3
# encoding: utf-8

import sys
import logging
import argparse
import socket
import os
import inspect
import shutil

__version__ = "v1"

module = sys.modules['__main__'].__file__
log = logging.getLogger(module)

class Utils:


    def __init__(self, log, path):
        self.path_app = os.path.dirname(os.path.realpath(__file__))
        self.path_mod = path
        self.path_home = os.environ['HOME']
        self.log = log

    def exec(self, args):
        os.system(args)

    def install_packages(self, packages):
        log.info("update package list")
        self.exec("sudo apt-get update")

        log.info("install aptitude")
        self.exec("sudo apt-get -y install aptitude")

        log.info("install required packages")
        self.exec("sudo sudo aptitude --assume-yes -Z install {}".format(packages))

    def __is_exec(self, path):
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return True
        return False

    def copy_tree(self, root_dir, script=None):
        log.info("copy recursively: {}".format(root_dir))
        for dirname, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                src = os.path.join(dirname, filename)
                dst = src[len(root_dir):]
                log.info("copy {} to {}".format(src, dst))
                path = os.path.dirname(dst)
                if not os.path.isdir(path):
                    self.exec("sudo mkdir -p {}".format(path))
                self.exec("sudo cp {} {}".format(src, dst))
        if script:
            if self.__is_exec(script):
                log.info("execute script: {}".format(script))
                self.exec(script)
            else:
                log.error("cannot execute script: {}".format(script))



def prepare_paths(searched_name):
    tmp = os.path.split(inspect.getfile(inspect.currentframe()))[0]
    tmp = os.path.realpath(os.path.abspath(tmp))

    cmd_folder = os.path.realpath(os.path.abspath(tmp))
    if cmd_folder not in sys.path:
        sys.path.insert(0, cmd_folder)

    dirs = ["terminals", "router"]
    for dir_entry in dirs:
        t = os.path.join(tmp, os.path.join("templates", dir_entry))
        dirs = os.listdir(t)
        for entry in dirs:
            if searched_name == entry:
                f = os.path.join(t, entry)
                sys.path.insert(0, f)
                return True, f

    return False, None

def prepare_guest_environment():
    homedir = os.environ['HOME']
    log.debug("change working diretory to {}".format(homedir))
    os.chdir(homedir)

def do(args):
    hostname = socket.gethostname()
    if args.name:
        hostname = args.name
    log.debug('hostname {}'.format(hostname))
    ok, path = prepare_paths(hostname)
    if not ok:
        log.error('hostname not in DB {}'.format(hostname))
        return 1
    m = __import__("main")
    utils = Utils(log, path)
    prepare_guest_environment()
    m.main(utils)

def parse_command_line(argv):
    formatter_class = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(description=module,
                                     formatter_class=formatter_class)
    parser.add_argument("--version", action="version",
                        version="%(prog)s {}".format(__version__))
    parser.add_argument("-v", "--verbose", dest="verbose_count",
                        action="count", default=0,
                        help="increases log verbosity for each occurence.")
    parser.add_argument('-n','--name', help='allow to overwrite hostname', required=False)
    arguments = parser.parse_args(argv[1:])
    log.setLevel(max(2 - arguments.verbose_count, 0) * 10)
    return arguments

def main():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG,
                        format='%(message)s')
    try:
        args = parse_command_line(sys.argv)
        log.info('Bootstraping Host')
        return do(args)
    except KeyboardInterrupt:
        log.error('Program interrupted!')
    finally:
        logging.shutdown()

if __name__ == "__main__":
    sys.exit(main())
