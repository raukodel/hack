import socket

from threading import Thread


class ProxyObject(Thread):

    def __init__(self, host, port):
        super(ProxyObject, self).__init__()
        self.port = port
        self.host = host
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(1)
        print("[proxy({})] setting up".format(self.port))

        self.client, addr = self.server.accept()

    def run(self):
        while True:
            data = self.server.recv(4096)
            if data:
                print(data)


master_server = ProxyObject("172.16.201.16", 46496)
master_server.start()
