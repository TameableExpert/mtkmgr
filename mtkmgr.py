#
# MikroTik Manager - Making managing MikroTiks magical.
#
#
# TODO: Create fields to add more information to the JSON vars.
# TODO: Restructure the GUI and allow for more variables to be saved.
#

import sys, os, io, json, datetime, tkinter as tk, subprocess, paramiko

class mtkmgr():
    tmpConfigFile = {}

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
            print(formatted_data) # Print out to the terminal so I don't have to keep looking in the log file.

    def LoadConfig(self):
        if os.path.isfile(self.conf_fileName):
            with open(self.conf_fileName, "r+") as conf_file:
                    loaded_config = conf_file.read() # Creates empty json file if config doesn't exist.
                    if len(loaded_config) > 0:
                        self.current_config = json.loads(loaded_config)
        else:
            with open(self.conf_fileName, "w+") as conf_file:
                    loaded_config = conf_file.read() # Creates empty json file if config doesn't exist.
                    if len(loaded_config) > 0:
                        self.current_config = json.loads(loaded_config)

    def SaveConfig(self):
        with open(self.conf_fileName, "w+") as conf_file:
            json_str = json.dumps(self.current_config)
            conf_file.write(json_str) # Creates empty json file if config doesn't exist.

    def Hosts_AddHost(self):
        try:
            ipaddress =  entry_ip_address.get()
            self.current_config['hosts'][ipaddress] = {}
            self.SaveConfig()
            self.HostList_Load()
            entry_ip_address.delete(0, 'end')
            
        except Exception as err:
            print("Something went wrong!", err)
            
    def Hosts_RemoveHost(self):
        selected_key = Hosts_ListBox.selection_get()
        selection = Hosts_ListBox.curselection()
        Hosts_ListBox.delete(selection[0])
        self.current_config['hosts'].pop(selected_key)
        self.SaveConfig()

    def Hosts_ConnectHost(self):
        host_key = Hosts_ListBox.selection_get()
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        # TODO: set this to load using the IP address.
        client.connect('127.0.0.1')
        stdin, stdout, stderr = client.exec_command("touch /home/grimm/Desktop/test.txt")
        client.close()

    def HostList_Clear(self):
        Hosts_ListBox.delete(0, 'end')

    def HostList_Load(self):
        self.HostList_Clear()
        if(self.current_config != {}):
            # TODO:Check to see if config has hosts, if not, create a blank instance.
                
            # Build list using host records.
            if len(self.current_config['hosts']) > 0:
                for key, value in self.current_config['hosts'].items():
                    Hosts_ListBox.insert(0, key) # Add host to listbox.
                self.LogData("There are things here.")
            else:
                self.LogData("Error: No records found.")
        else:
            self.LogData("Error: Configuration file empty.")

    def ReturnSelectedHost(self):
        print(Hosts_ListBox.selection_get())

    def SetupInterface(self):
        app_window = tk.Tk()
        app_window.title("MikroTik Manager")
        #app_window.geometry("400x300")

        # Top menu system
        mtkmgr_menu = tk.Menu(app_window)
        # File Menu
        file_menu = tk.Menu(mtkmgr_menu)
        
        file_export_menu = tk.Menu(file_menu)
        file_export_menu.add_command(label="Import")
        file_export_menu.add_command(label="Export")
        file_menu.add_cascade(label="Config", menu=file_export_menu)

        file_menu.add_command(label="Quit", command=app_window.destroy)
        mtkmgr_menu.add_cascade(label="File", menu=file_menu)
        app_window.config(menu=mtkmgr_menu)

        # Existing Host List
        frame_hosts = tk.Frame(app_window)
        frame_hosts.pack()
        label_hosts = tk.Label(frame_hosts, text="Hosts")
        label_hosts.pack()
        global Hosts_ListBox
        Hosts_ListBox = tk.Listbox()
        self.HostList_Load()
        Hosts_ListBox.pack(fill=tk.BOTH, expand=1)

        #Hostname Entry
        frame_hostname = tk.Frame(app_window)
        frame_hostname.pack(fill=tk.BOTH, expand=1)
        label_hostname = tk.Label(frame_hostname, text="Hostname")
        label_hostname.pack(side=tk.LEFT)
        global entry_hostname
        entry_hostname = tk.Entry(frame_hostname)
        entry_hostname.pack(fill=tk.X, expand=1, side=tk.LEFT)

        # IP Address Entry
        frame_ip_address = tk.Frame(app_window)
        frame_ip_address.pack(fill=tk.BOTH, expand=1)
        label_ip_address = tk.Label(frame_ip_address, text="IP Address")
        label_ip_address.pack(side=tk.LEFT)
        global entry_ip_address
        entry_ip_address = tk.Entry(frame_ip_address)
        entry_ip_address.pack(fill=tk.X, expand=1, side=tk.LEFT)
        
        # Add Host Button
        button_add_ip_address = tk.Button(frame_ip_address, text="Add", command=self.Hosts_AddHost)
        button_add_ip_address.pack(fill=tk.X, expand=1, side=tk.BOTTOM)

        # Host Actions Frame & Buttons
        frame_SelectedHostActions = tk.Frame(app_window)
        frame_SelectedHostActions.pack(fill=tk.BOTH, expand=1, side=tk.BOTTOM)

        btn_connectHost = tk.Button(frame_SelectedHostActions, text="Connect", command=self.Hosts_ConnectHost)
        btn_connectHost.pack()

        btn_removeHost = tk.Button(frame_SelectedHostActions, text="Remove", command=self.Hosts_RemoveHost)
        btn_removeHost.pack()

        # Display the window.
        app_window.mainloop()

class userInterface():
    """ Setup the user interface! """
    def __init__(self):
        print("User Interface Initialized.")

    def CreateControl(self, argType, argName, argParent, *args, **kwargs):
        log.toConsole("Creating Control")

class fileManager():
    def __init__(self):
        print("File Manager Initialized!")

    def FileExists(self, argFilepath, *args, **kwargs):
        return os.path.isfile(argFilepath)

    def CreateFile(self, argFilepath):
        log.toConsole("Creating File")
        #open(argFilepath, "w+", 0, )

    def LoadFile(self, argFilepath, argCreate):
        tmpIsFile = os.path.isfile(argFilepath)
        

class outputManager():
    def __init__(self):
        print("Output Manager Initialized.")
    
    def toConsole(self, argMessage):
        print(argMessage)

    def toFile(self, argMessage):
        print("This needs to be updated.")
        

class MikroTik():
    def __init__(self):
        print("MikroTik Created.")

    def Connect(self):
        pass

log = outputManager()