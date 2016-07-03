#!/usr/bin/env python3

import os

os.system("sudo systemctl enable finalizer.service")
os.system("sudo systemctl start finalizer.service")
os.system("sudo systemctl status finalizer.service")

