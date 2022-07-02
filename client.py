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



if __name__ == "__main__":
    my_ip = sys.argv[1]
    my_port = int(sys.argv[2])
    friend_ip = sys.argv[3]
    friend_port = int(sys.argv[4])

    c1 = Client(my_ip, my_port, friend_ip, friend_port)