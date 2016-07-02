import os
import shutil

def install_packages(utils):
    packages = "git tcpdump python3-flask build-essential install smcroute bison flex gdb"
    utils.install_packages(packages)

def install_config_files(utils):
    d = os.path.dirname(utils.path_mod)
    fs_copy_root = os.path.join(d, "shared", "fs-copy")
    for dirname, dirnames, filenames in os.walk(fs_copy_root):
        for filename in filenames:
            src = os.path.join(dirname, filename)
            dst = src[len(fs_copy_root)]
            os.makedirs(os.path.dirname(dst))
            shutil.copy2(src, dst)
            utils.log.info("copy {} to {}".format(src, dst))

def start_services(utils):
    utils.exec("sudo systemctl enable smcroute")
    utils.exec("sudo systemctl start smcroute")

def setup_distribution(utils):
    install_packages(utils)
    install_config_files(utils)
    start_services(utils)

def prepare_src_dir(utils, p):
    shutil.rmtree(p)
    os.makedirs(p)

def clone_repos(utils, p):
    utils.exec("git clone https://github.com/hgn/mcast-discovery-daemon.git")
    utils.exec("git clone https://github.com/hgn/ipproof.git")
    utils.exec("chown -R admin:admin {}".format(p))

def setup_third_pary_daemons(utils):
    p = os.path.join(utils.path_home, "src", "daemons")
    orig_dir = os.pwd()
    prepare_src_dir(utils, p)
    clone_repos(utils, p)
    os.chdir(orig_dir)

def main(utils):
    setup_distribution(utils)
    setup_third_pary_daemons(utils)
    utils.exec("date")
