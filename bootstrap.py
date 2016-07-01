#!/usr/bin/env python3
# encoding: utf-8

import sys
import logging
import argparse
import socket
import os
import inspect

__version__ = "v1"

module = sys.modules['__main__'].__file__
log = logging.getLogger(module)

class Utils:
    def exec(self, args):
        os.system(args)

def prepare_paths(searched_name):
    tmp = os.path.split(inspect.getfile(inspect.currentframe()))[0]

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
                return True

    return False
            

def do(args):
    hostname = socket.gethostname()
    log.debug('hostname {}'.format(hostname))
    ok = prepare_paths(hostname)
    if not ok:
        log.error('hostname not in DB {}'.format(hostname))
        return 1
    m = __import__("main")
    utils = Utils()
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
