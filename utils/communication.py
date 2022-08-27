import socket
import threading

class Communication:

    def __init__(self,ip,socket_no):
        self.address = (ip,socket_no)
        self.comm_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.comm_sock.bind(self.address)
        except socket.error as e:
            print("unable to bind with '{0}'".format(e.strerror))
            self.comm_sock.close()

        recv_thread = threading.Thread(target=self.receive_message)
        recv_thread.daemon = True
        recv_thread.start()
    

    def send_message(self,message:str, to_data:tuple) -> bool:
        self.comm_sock.sendto(message.encode(),to_data)

    def receive_message(self):
        while True:
            recvData,recvAddr = self.comm_sock.recvfrom(2048)
            sender = recvAddr[1]
            print(f'\n{sender}: {recvData.decode()}')