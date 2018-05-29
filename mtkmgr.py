#
# MikroTik Manager - Making managing MikroTiks magical.
#

import sys, os, io

home_dir = os.path.expanduser('~') # Gets home dir crossplatform.
config_folder = home_dir + "/.mtkmgr/"
conf_file = config_folder + "mtkmgr.cfg"
log_file = config_folder + "mtkmgr.log"


def Main():
    #
    # Run Setup - Create config_folder, conf_file, and log_file
    #
    Setup()

def Setup():
    if os.path.exists(config_folder):
        # TODO: Do something here.
        print "I'll get to this later."
    else:
        os.mkdir(config_folder)

Main()