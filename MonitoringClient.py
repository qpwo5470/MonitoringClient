import threading
from datetime import datetime
from time import sleep
from platform import node
from requests import post
from json import dumps as json_dumps
from signal import signal, SIGTERM, SIGINT
from socket import gethostbyname, gethostname


class MonitoringClient:
    def __init__(self, server_ip):
        self.server_ip = server_ip
        self.__data = {}
        self.__data['device_name'] = node()
        self.__state = {}
        self.__state['app'] = 'Python3'
        self.__state['local_ip'] = gethostbyname(gethostname())
        self.__read_lock = threading.Lock()
        self.__state['start_time'] = datetime.now().strftime('%Y-%m-%d %A %H:%M:%S')
        self.__thread = threading.Thread(target=self.__send, args=())
        self.__thread.start()
        signal(SIGTERM, self.__shutdown)
        signal(SIGINT, self.__shutdown)

    def fakeDeviceName(self, name):
        self.__data['device_name'] = name

    def set(self, name, value):
        self.__state[name] = value

    def __send(self):
        while True:
            self.__data['data'] = json_dumps(self.__state)
            try:
                response = post(self.server_ip, data=self.__data, timeout=60)
                if response == b'1':
                    import os
                    os.system("shutdown -t 0 -r -f")
            except Exception as e:
                print(e)
            sleep(5)

    def __shutdown(self):
        self.__state['exit_time'] = datetime.datetime.now().strftime('%Y-%m-%d %A %H:%M:%S')
        self.__data['data'] = json_dumps(self.__state)
        try:
            post(self.server_ip, data=self.__data, timeout=60)
        except Exception as e:
            print(e)

