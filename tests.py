import unittest
import socket
import subprocess
import time


#def bash_command(cmd):
#    subprocess.Popen(['/bin/bash', '-c', cmd])


class Client:
    def __init__(self, addr, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.settimeout(5.0)
        self.addr = str.encode(addr)
        self.port = port

    def start(self):
        subprocess.Popen(['/bin/bash', '-c', "cmake-build-debug/untitled -p %s" % self.port])

    def send(self):
        pass

    def put(self, block_number, offset, length, data):
        # put: 2b - block number, 2b - offset, 2b - length, [length]b - data
        put_data = bytes([0x20])
        put_data += bytes([block_number & 0xFF, block_number >> 8 & 0xFF])
        put_data += bytes([offset & 0xFF, offset >> 8 & 0xFF])
        put_data += bytes([length & 0xFF, length >> 8 & 0xFF])
        put_data += bytes(data)

        self.__send_data(put_data)

    def receive(self, block_number):
        receive_data = bytes([0x50])
        receive_data += bytes([block_number & 0xFF, block_number >> 8 & 0xFF])

        self.__send_data(receive_data)

        return self.client_socket.recvfrom(65207)[0]
        
    def quit(self):
        self.__send_data(b"\0")

    def dispose(self):
        self.client_socket.close()

    def __send_data(self, data):
        self.client_socket.sendto(data, (self.addr, self.port))


class ServerTests(unittest.TestCase):
    def setUp(self):
        port = 5100
        self.client = Client("127.0.0.1", 5100)
        self.client.start()

    def test_put_and_receive(self):
        block_number = 7
        offset = 4
        data = [1, 2, 3]
        data_bytes = b"\x01\x02\x03"
        length = len(data)

        self.client.put(block_number, offset, length, data)
        result = self.client.receive(block_number)[offset : offset + length]

        self.assertEqual(data_bytes, result)

    def tearDown(self):
        time.sleep(1)
        self.client.quit()
        self.client.dispose()
        time.sleep(1)


if __name__ == "__main__":
    unittest.main()