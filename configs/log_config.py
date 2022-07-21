from sys import path, argv
import logging

module_name = argv[0].split("\\")[-1] #get the module name, which is a filename at the end of a path

if ".py" in module_name:
    module_name = module_name.split(".")[0]

LOG_FORMAT = "%(levelname)s %(asctime)s: %(message)s"
LOG_FILE = f"{path[0]}\log\{module_name}.log"
LOG_LEVEL = logging.INFO