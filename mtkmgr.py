#
# MikroTik Manager - Making managing MikroTiks magical.
#

import sys, os, io, json, datetime, Tkinter

class mtkmgr():
    def __init__(self):
        #
        # Config
        #
        self.current_config = {}
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
        if os.path.isfile(self.conf_fileName):
            with open(self.conf_fileName, "r+") as conf_file:
                    loaded_config = conf_file.read() # Creates empty json file if config doesn't exist.
                    if len(loaded_config) > 0:
                        self.current_config = json.loads(loaded_config, encoding="utf-8")
        else:
            with open(self.conf_fileName, "w+") as conf_file:
                    loaded_config = conf_file.read() # Creates empty json file if config doesn't exist.
                    if len(loaded_config) > 0:
                        self.current_config = json.loads(loaded_config, encoding="utf-8")

    def SaveConfig(self):
        with open(self.conf_fileName, "w+") as conf_file:
            json_str = json.dumps(self.current_config, encoding="utf-8")
            conf_file.write(json_str) # Creates empty json file if config doesn't exist.

    def AddHost(self):
        try:
            keys =  enumerate(self.current_config)
            if "hosts" not in keys:
                self.current_config["hosts"] = {}
            ipaddress =  entry_ip_address.get()
            self.current_config["hosts"][ipaddress] = {}
            self.SaveConfig()
        except Exception, err:
            print "Something went wrong!", err

    def ReturnSelectedHost(self):
        print listbox_hosts.selection_get()

    def SetupInterface(self):
        app_window = Tkinter.Tk()
        app_window.title("MikroTik Manager")
        app_window.geometry("400x300")
        
        # Existing Host List
        frame_hosts = Tkinter.Frame(app_window)
        frame_hosts.pack()
        label_hosts = Tkinter.Label(frame_hosts, text="Hosts")
        label_hosts.pack()
        global listbox_hosts
        listbox_hosts = Tkinter.Listbox()

        if(self.current_config != {}):
            # TODO:Check to see if config has hosts, if not, create a blank instance.
                
            # Build list using host records.
            if len(self.current_config["hosts"]) > 0:
                for key, value in self.current_config["hosts"].items():
                    listbox_hosts.insert(0, key) # Add host to listbox.
                self.LogData("There are things here.")
            else:
                self.LogData("Error: No records found.")
        else:
            self.LogData("Error: Configuration file empty.")

        listbox_hosts.pack()

        # IP Address Entry
        frame_ip_address = Tkinter.Frame(app_window)
        frame_ip_address.pack()
        label_ip_address = Tkinter.Label(frame_ip_address, text="IP Address")
        label_ip_address.pack(side=Tkinter.LEFT)
        global entry_ip_address
        entry_ip_address = Tkinter.Entry(frame_ip_address)
        entry_ip_address.pack(side=Tkinter.LEFT)
        button_add_ip_address = Tkinter.Button(frame_ip_address, text="Add", command=self.AddHost)
        button_add_ip_address.pack(side=Tkinter.LEFT)

        frame_SelectedHostActions = Tkinter.Frame(app_window)
        frame_SelectedHostActions.pack(side=Tkinter.BOTTOM)

        btn_getSelectedHost = Tkinter.Button(frame_SelectedHostActions, text="Get Host Value", command=self.ReturnSelectedHost)
        btn_getSelectedHost.pack()

        # Display the window.
        app_window.mainloop()

mtkmgr()