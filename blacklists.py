import os
import sys
from src.IpSet import IpSet
from src.File import IpSetFile
from src.Config import LoadConfig
from src.Exceptions import *

try:
    config = LoadConfig()
except ConfigException as e:
    print(e)
    sys.exit(os.EX_UNAVAILABLE)

# Push it direst to ipset
blacklist = IpSet(config)
blacklist.set_blacklist()

# Create files with ipset (Value folder in config file must be configured)
#ban_file = IpSetFile(config)
#ban_file.create_file()
