import paths
import os


scripts = paths.scripts
dataset = paths.dataset
dependencies = paths.dependencies


# manage DOCKER COMPOSE
def start_container_set_5():
    os.chdir("../dependencies")
    os.system("COMPOSE_PROFILES=container-set-5 docker-compose up --detach &")


def start_container_set_3():
    os.chdir("../dependencies")
    os.system("COMPOSE_PROFILES=container-set-3 docker-compose up --detach &")


def stop_containers():
    os.chdir("../dependencies")
    os.system("docker compose stop")
    # os.system("docker compose down")


def start_container_set_2():
    os.chdir("../dependencies")
    os.system("COMPOSE_PROFILES=container-set-2 docker-compose up  --detach&")


def start_container_set_1():
    os.chdir("../dependencies")
    os.system("COMPOSE_PROFILES=container-set-1 docker-compose up --detach &")
