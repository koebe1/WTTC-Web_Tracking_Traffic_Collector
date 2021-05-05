import os.path
import datetime
import re


# PATHS

# ...to FOLDERS
scripts = os.path.dirname(__file__)
dataset = os.path.dirname(scripts)
captured = os.path.join(dataset, "captured")
dependencies = os.path.join(dataset, "dependencies")

curr_dir = os.path.join(
    captured, datetime.datetime.now().strftime('%d_%m_%Y %H_%M_%S'))

# ...to CONFIG
config = os.path.join(dependencies, "config.yml")

# ...to SCRIPTS
create_folders = os.path.join(scripts, "create_folders.py")
get_ublock_log = os.path.join(scripts, "get_ublock_log.py")
open_docker = os.path.join(scripts, "open_docker.py")
start_containers = os.path.join(scripts, "start_containers.py")
