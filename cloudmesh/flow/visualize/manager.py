
import requests
import os


def shutdown():
    url = "http://127.0.0.1:8080/shutdown"
    response = requests.get(url)

def start():
    os.system('python server.py')


