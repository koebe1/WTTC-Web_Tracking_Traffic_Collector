import os.path
import datetime
import re


# PATHS

# ...to FOLDERS
scripts = os.path.dirname(__file__)
dataset = os.path.dirname(scripts)
captured = os.path.join(dataset, "captured")
dependencies = os.path.join(dataset, "dependencies")



# ...to CONFIG
config = os.path.join(dependencies, "config.yml")

# ...to SCRIPTS
create_folders = os.path.join(scripts, "create_folders.py")
get_ublock_log = os.path.join(scripts, "get_ublock_log.py")
open_docker = os.path.join(scripts, "open_docker.py")
start_containers = os.path.join(scripts, "start_containers.py")
# open_website_1 = os.path.join(scripts, "open_website_1.py")
# open_website_2 = os.path.join(scripts, "open_website_2.py")
# open_website_3 = os.path.join(scripts, "open_website_3.py")
