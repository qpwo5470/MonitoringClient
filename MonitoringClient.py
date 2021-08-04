import threading
import time
import platform
import requests
import json


class MonitoringClient:
    def __init__(self, server_ip):
        self.server_ip = server_ip
        self.data = {}
        self.data['device_name'] = platform.node()
        self.state = {}
        self.state['app'] = 'Python3'
        self.read_lock = threading.Lock()
        self.thread = threading.Thread(target=self.send, args=())
        self.thread.start()

    def fakeDeviceName(self, name):
        self.data['device_name'] = name

    def set(self, name, value):
        self.state[name] = value

    def send(self):
        while True:
            self.data['data'] = json.dumps(self.state)
            try:
                requests.post(self.server_ip, data=self.data, timeout=60)
            except Exception as e:
                print(e)
            time.sleep(5)
