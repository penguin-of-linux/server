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

    def send(self, target_address, target_port, block_number, offset, length, data):
        # send: 4b - target address, 2b - target port, 2b - block number, 4b - offset, 2b - length
        send_data = bytes([0x30])

        send_data += bytes(target_address)
        send_data += bytes([target_port & 0xFF, target_port >> 8 & 0xFF])
        send_data += bytes([block_number & 0xFF, block_number >> 8 & 0xFF])
        send_data += bytes([offset & 0xFF, offset >> 8 & 0xFF, offset >> 16 & 0xFF,  offset >> 24 & 0xFF])
        send_data += bytes([length & 0xFF, length >> 8 & 0xFF])
        send_data += bytes(data)
        
        self.__send_data(send_data)

    def put(self, block_number, offset, length, data):
        # put: 2b - block number, 4b - offset, 2b - length, [length]b - data
        put_data = bytes([0x20])
        put_data += bytes([block_number & 0xFF, block_number >> 8 & 0xFF])
        put_data += bytes([offset & 0xFF, offset >> 8 & 0xFF, offset >> 16 & 0xFF,  offset >> 24 & 0xFF])
        put_data += bytes([length & 0xFF, length >> 8 & 0xFF])
        put_data += bytes(data)

        self.__send_data(put_data)

    def receive(self, block_number, offset):
        receive_data = bytes([0x50])
        receive_data += bytes([block_number & 0xFF, block_number >> 8 & 0xFF])
        receive_data += bytes([offset & 0xFF, offset >> 8 & 0xFF, offset >> 16 & 0xFF,  offset >> 24 & 0xFF])

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
        self.client1 = Client("127.0.0.1", 1111)
        self.client2 = Client("127.0.0.1", 2222)
        #self.client1.start()
        self.client2.start()

    def test_put_and_receive(self):
        block_number = 7
        offset = 4
        data = [1, 2, 3]
        data_bytes = b"\x01\x02\x03"
        length = len(data)

        #self.client1.put(block_number, offset, length, data)
        result = self.client2.receive(block_number, offset)[:length]

        self.assertEqual(data_bytes, result)

    def test_send_and_receive(self):
        block_number = 0
        offset = 0
        data = [1, 2, 3]
        data_bytes = b"\x01\x02\x03"
        length = len(data)
        self.client1.put(block_number, offset, length, data)

        target_address = b"\x01\x00\x00\x7f"
        target_port = self.client2.port
        self.client1.send(target_address, target_port, block_number, offset, length, data)

        result = self.client2.receive(block_number, offset)[:length]
        self.assertEqual(data_bytes, result)

    def tearDown(self):
        time.sleep(1)
        #self.client1.quit()
        self.client1.dispose()
        self.client2.quit()
        self.client2.dispose()
        time.sleep(1)


if __name__ == "__main__":
    unittest.main()