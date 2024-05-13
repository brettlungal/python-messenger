from persistence.mailbox_actions import MailboxActions
from persistence.user_actions import UserActions
from persistence.friend_actions import FriendActions
from interfaces.chat import ChatClient
from interfaces.mailbox import Mailbox
from tabulate import tabulate
import sys

class Menu:

    def __init__(self, user_info, db, cursor):
        self.username = user_info[0]
        self.host = user_info[2]
        self.port = user_info[3]
        self.user_db = UserActions(db, cursor)
        self.friend_db = FriendActions(db, cursor)
        self.mail_db = MailboxActions(db, cursor)


    def get_options(self):
        messages = self.mail_db.get_new_messages(self.username)
        msg_count = len(messages) if messages is not None else 0
        choice = input(f"1: Add Friends\n2: Show friends\n3: Start Chat\n4: Check Mailbox[{msg_count}]\n\n>")
        match(choice):
            #TODO - combine 1 and 2 into friends class where you can view or add friends
            case "1":
                friend_username = input("Enter friends username: ")
                self.add_friend(friend_username)
            case "2":
                self.display_friends()
            case "3":
                self.launch_chat()
            case "4":
                mail = Mailbox(messages)
                mail.launch_mailbox_interface()
            case "q":
                self.user_db.close_connection()
                self.friend_db.close_connection()
                self.mail_db.close_connection()
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
                print(f"starting chat with {chat_friend_username} at address {friend_ip} on port {friend_port}")
                # chat = ChatClient(self.host, int(self.port), friend_ip, int(friend_port))
                
        except ValueError:
            print("Please enter valid friend index as integer")