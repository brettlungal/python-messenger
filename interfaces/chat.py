from utils.communication import Communication
import sys

class ChatClient:

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


    def launch_chat(self):
        self.display_friends()
        self.user_db.update_last_active(self.username)
        choice = input("Select a friend to chat with: ")
        try:
            parsed_choice = int(choice)
            # TODO check if index is in range of friends list
            friends = self.friend_db.get_friends(self.username)
            if parsed_choice > len(friends):
                raise ValueError
            else:
                chat_friend_username = friends[parsed_choice][0]
                friend_ip, friend_port = self.user_db.get_user_data(chat_friend_username)
                print(f"starting chat with {chat_friend_username} at address {friend_ip} on port {friend_port}")
                # chat = ChatClient(self.host, int(self.port), friend_ip, int(friend_port))
                
        except ValueError:
            print("Please enter valid friend index as integer")