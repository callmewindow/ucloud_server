import docker,time
import traceback
import os
base_url = 'tcp://101.200.219.50:6666'
client = None
def log(*args,**kwargs):
    print(*args,**kwargs)
def init():
    try:
        global client
        client = docker.Client(base_url=base_url)
        log('[uDocker] Client is ready.')
    except:
        traceback.print_exc()
        log('[uDocker] Unable to connect to docker client.')
def close():
    try:
        global client
        if client != None:
            client.close()
        log('[uDocker] Client is closed.')
    except:
        traceback.print_exc()
        log('[uDocker] Unable to close the client.')
def wrapper(func):
    def innerFunc(*args,**kwargs):
        if client != None:
            return func(*args,**kwargs)
        else:
            log('[uDocker] Client is not ready.')
            return
    return innerFunc
@wrapper
def images():
    return client.images()
@wrapper
def containers():
    return client.containers()

def createContainer(containerName):
    os.system('docker run --name {} -dit python:mirai_wyx /bin/bash'.format(containerName))
    time.sleep(5)
    os.system('docker exec -dit -w /home/mirai {} python main.py'.format(containerName))
    time.sleep(10)
    os.system('docker exec -dit -w /home/mirai {} python bot.py'.format(containerName))
@wrapper
def removeContainer(containerName):
    client = docker.Client(base_url)    
    client.stop(containerName)
    client.remove_container(containerName)
    print(client.containers())
    client.close()

def transferFile(containerName,hostPath,containerPath):
    os.system('docker cp {} {}:{}'.format(containerName,hostPath,containerPath))

if __name__ == '__main__':
    init()
    images = client.images()