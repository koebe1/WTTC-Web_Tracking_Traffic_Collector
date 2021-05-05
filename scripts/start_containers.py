import path
import os
import time


scripts = path.scripts
dataset = path.dataset
dependencies = path.dependencies


def start_container_set_1_2_3():
    os.chdir("../dependencies")
    os.system("COMPOSE_PROFILES=all docker-compose up &")


def stop_containers():
    os.chdir("../dependencies")
    os.system("docker compose stop")
    # os.system("docker compose down")


def start_container_set_1_2():
    os.chdir("../dependencies")
    os.system("COMPOSE_PROFILES=container-set-1-2 docker-compose up &")


def start_container_set_1():
    os.chdir("../dependencies")
    os.system("COMPOSE_PROFILES=container-set-1 docker-compose up &")
# def stop_containers_1():


start_container_set_1_2_3()
