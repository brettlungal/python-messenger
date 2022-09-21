from persistence.user_actions import UserActions
from persistence.friend_actions import FriendActions
from interfaces.chat import ChatClient
from tabulate import tabulate
import sys

class Menu:

    def __init__(self, user_info, db, cursor):
        self.username = user_info[0]
        self.host = user_info[2]
        self.port = user_info[3]
        self.user_db = UserActions(db, cursor)
        self.friend_db = FriendActions(db, cursor)

        self.user_db.update_last_active(self.username)

    def get_options(self):
        choice = input("1: Add Friends\n2: Show friends\n3: Start Chat\n4: Mailbox")
        if choice == "1":
            friend_username = input("Enter friends username: ")
            self.add_friend(friend_username)
        elif choice == "2":
            self.display_friends()
        elif choice == "3":
            self.launch_chat()
        elif choice == "4":
            pass
        elif choice == "q":
            self.user_db.close_connection()
            self.friend_db.close_connection()
            sys.exit(1)
    
    def add_friend(self,friend_username):
        if self.user_db.username_exists(friend_username):
            self.friend_db.create_friendship(self.username, friend_username)
        else:
            print("Friends username does not exist!")
        self.user_db.update_last_active(self.username)

    def display_friends(self):
        friends = self.friend_db.get_friends(self.username)
        for i in range(len(friends)):
            friends[i] = list(friends[i])
            friend_username = friends[i][0]
            friends[i].append(friend_username)
            friends[i][0] = str(i)
            online = "Online" if self.user_db.is_online(friend_username) else "Offline"
            friends[i].append(online)
        print("\n\n")
        print(tabulate(friends, headers=['Friend', 'Status'], tablefmt='orgtbl'))
        print("\n\n")
        self.user_db.update_last_active(self.username)
    
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
                chat = ChatClient(self.host, int(self.port), friend_ip, int(friend_port))
                
        except ValueError:
            print("Please enter valid friend index as integer")