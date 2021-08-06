import threading
import datetime
import time
import platform
import requests
import json
import signal
import socket


class MonitoringClient:
    def __init__(self, server_ip):
        self.server_ip = server_ip
        self.__data = {}
        self.__data['device_name'] = platform.node()
        self.__state = {}
        self.__state['app'] = 'Python3'
        self.__state['local_ip'] = socket.gethostbyname(socket.gethostname())
        self.__read_lock = threading.Lock()
        self.__state['start_time'] = datetime.datetime.now().strftime('%Y-%m-%d %A %H:%M:%S')
        self.__thread = threading.Thread(target=self.__send, args=())
        self.__thread.start()
        signal.signal(signal.SIGTERM, self.__shutdown)
        signal.signal(signal.SIGINT, self.__shutdown)

    def fakeDeviceName(self, name):
        self.__data['device_name'] = name

    def set(self, name, value):
        self.__state[name] = value

    def __send(self):
        while True:
            self.__data['data'] = json.dumps(self.__state)
            try:
                requests.post(self.server_ip, data=self.__data, timeout=60)
            except Exception as e:
                print(e)
            time.sleep(5)

    def __shutdown(self):
        self.__state['exit_time'] = datetime.datetime.now().strftime('%Y-%m-%d %A %H:%M:%S')
        self.__data['data'] = json.dumps(self.__state)
        try:
            requests.post(self.server_ip, data=self.__data, timeout=60)
        except Exception as e:
            print(e)

