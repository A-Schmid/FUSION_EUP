import os

path = "log" # the default log path is "log/" relative to the notebook file - maybe this variable should be in a global config file?

def set_log_path(log_path):
    global path
    path = log_path

def log_append_line(filename = "log.txt", message = ""):
    # dont log empty messages
    if message == "":
        return

    global path
    
    # create the log directory if it doesnt exist
    __check_path(path)

    with open("{}/{}".format(path, filename), "a") as logfile:
        logfile.write("{}\n".format(message))

def __check_path(path):
    try:
        os.stat(path)
    except:
        os.makedirs(path)
