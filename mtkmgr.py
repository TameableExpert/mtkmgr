#
# MikroTik Manager - Making managing MikroTiks magical.
#

import sys, os, io, json, datetime, Tkinter

class mtkmgr():
    def __init__(self):
        #
        # Setup
        #
        self.home_dir = os.path.expanduser('~') # Gets home dir crossplatform.
        self.config_folder = self.home_dir + "/.mtkmgr/"
        self.conf_fileName = self.config_folder + "mtkmgr.cfg.json"
        self.log_fileName = self.config_folder + "mtkmgr.log"

        #
        # Run Setup - Create config_folder, conf_file, and log_file
        #
        self.InitalSetup()
        self.LoadConfig()
        self.SetupInterface()

    def InitalSetup(self):
        #
        # Create 
        #
        if not os.path.exists(self.config_folder):
            #
            # Create folder for saving config and log.
            #
            os.mkdir(self.config_folder)
        self.LogData("Setup Complete.")

    def LogData(self, data):
        with open(self.log_fileName, "a+") as log_file:
            formatted_data = str(datetime.datetime.now()) + ": " + data + "\r"
            log_file.writelines(formatted_data)
            print formatted_data # Print out to the terminal so I don't have to keep looking in the log file.

    def LoadConfig(self):
        with open(self.conf_fileName, "w+") as conf_file:
                conf_file.write(json.dumps({})) # Creates empty json file if config doesn't exist.

    def SetupInterface(self):
        self.app_window = Tkinter.Tk()
        self.app_window.mainloop()

mtkmgr()