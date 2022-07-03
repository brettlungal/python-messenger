from communication import Communication
import sys

class Client:

    def __init__(self,host_ip, host_socket, friend_ip, friend_socket):
        self.host_socket = host_socket
        self.comms = Communication(host_ip,host_socket)
        self.friend_data = (friend_ip,friend_socket)
        self.message_prompt()

    def message_prompt(self):
        print("Press Q to quit")
        while True:
            data = input("Me: ")
            self.comms.send_message(data, self.friend_data)
