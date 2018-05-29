#
# MikroTik Manager - Making managing MikroTiks magical.
#

import sys, os, io, json, datetime

home_dir = os.path.expanduser('~') # Gets home dir crossplatform.
config_folder = home_dir + "/.mtkmgr/"
conf_fileName = config_folder + "mtkmgr.cfg.json"
log_fileName = config_folder + "mtkmgr.log"

def Main():
    #
    # Run Setup - Create config_folder, conf_file, and log_file
    #
    Setup()

def Setup():
    if not os.path.exists(config_folder):
        os.mkdir(config_folder) # Create folder for saving config and log.
        LogData("Directory created: " + config_folder)
        LogData("File created: " + log_fileName)
    if not os.path.exists(conf_fileName):
        with open(conf_fileName, "w+") as conf_file:
            conf_file.write(json.dumps({})) # Creates empty json file.
            LogData("File created: " + conf_fileName)

    
def LogData(data):
    with open(log_fileName, "a+") as log_file:
        log_file.writelines(str(datetime.datetime.now()) + ": " + data + "\r")

Main()