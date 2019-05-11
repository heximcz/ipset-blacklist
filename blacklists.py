import os
import sys
from src.IpSet import IpSet
from src.Config import LoadConfig
from src.Exceptions import *

try:
    config = LoadConfig()
except ConfigException as e:
    print(e)
    sys.exit(os.EX_UNAVAILABLE)

blacklist = IpSet(config)
blacklist.set_blacklist()
