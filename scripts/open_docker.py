import subprocess
import sys
import psutil
import time
import yaml
import os.path
import path

scripts = path.scripts
dataset = path.dataset
dependencies = path.dependencies

with open(os.path.join(dependencies, 'config.yml')) as f:
    config = yaml.safe_load(f)
    docker_path = config["docker_path"]

# search for docker in processes
if "docker" in (p.name() for p in psutil.process_iter()):
    print("Docker is up and running!")
    
else:
    opener = "open" if sys.platform == "darwin" else "xdg-open"
    p = subprocess.call([opener, docker_path])
    print("Waiting for Docker to start...")
