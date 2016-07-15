import os
import shutil

def install_packages(utils):
    packages = "tcpdump python3 strace"
    # performacne test tools, just make sure everybody is happy
    packages += "iperf3 netcat-openbsd hping3"
    utils.install_packages(packages)

def copy_global_shared_tree(utils):
    shared_dir = os.path.join(utils.path_app, "templates", "shared")
    fs_copy_root = os.path.join(shared_dir, "fs-copy")
    fs_copy_root_script = os.path.join(shared_dir, "fs-copy-finish.py")
    utils.copy_tree(fs_copy_root, script=fs_copy_root_script)


def copy_router_shared_tree(utils):
    shared_dir = os.path.join(os.path.dirname(utils.path_mod), "shared")
    fs_copy_root = os.path.join(shared_dir, "fs-copy")
    fs_copy_root_script = os.path.join(shared_dir, "fs-copy-finish.py")
    utils.copy_tree(fs_copy_root, script=fs_copy_root_script)

def start_services(utils):
    pass

def setup_distribution(utils):
    install_packages(utils)
    copy_global_shared_tree(utils)
    copy_router_shared_tree(utils)
    start_services(utils)

def prepare_src_dir(utils, p):
    if os.path.isdir(p):
        shutil.rmtree(p)
    os.makedirs(p)
    os.chdir(p)

def setup_misc_apps(utils, p):
    utils.exec("git clone https://github.com/hgn/mcast-discovery-daemon.git")
    utils.exec("chown -R admin:admin {}".format(p))

def setup_third_pary_daemons(utils):
    orig_dir = os.getcwd()
    p = os.path.join(utils.path_home, "src", "daemons")
    prepare_src_dir(utils, p)
    setup_misc_apps(utils, p)
    os.chdir(orig_dir)

def main(utils):
    setup_distribution(utils)
    setup_third_pary_daemons(utils)
