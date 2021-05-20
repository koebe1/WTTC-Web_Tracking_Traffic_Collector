import subprocess
import sys
import psutil
import yaml
import os.path
import paths
import time


def open_docker_app():

    dependencies = paths.dependencies

    with open(os.path.join(dependencies, 'config.yml')) as f:
        config = yaml.safe_load(f)
        docker_path = config["docker_path"]

    # search for docker in processes
    if "docker" in (p.name() for p in psutil.process_iter()):
        print("Docker is up and running!")

    # start docker application
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, docker_path])
        print("Starting Docker...")

        # wait for docker to start up
