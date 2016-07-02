
def install_packages(utils):
    packages = "git tcpdump python3-flask build-essential install smcroute bison flex gdb"
    utils.install_packages(packages)

def install_config_files(utils):
    pass

def start_services(utils):
    pass

def main(utils):
    #install_packages(utils)
    #install_config_files(utils)
    utils.exec("date")
