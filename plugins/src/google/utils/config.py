from os import getenv

if getenv("DEV_MODE") == "1":
    from utils.dev_keys import *

else:
    SERPAPI_KEY = getenv("SERPAPI_KEY")
