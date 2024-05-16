import sys

# Persistence
from persistence.mailbox_actions import MailboxActions
from persistence.user_actions import UserActions
from persistence.friend_actions import FriendActions

# Interfaces
from interfaces.chat import ChatClient
from interfaces.mailbox import Mailbox
from interfaces.friends import Friends


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
        choice = input(f"1: Friends\n2: Start Chat\n3: Check Mailbox[{msg_count}]\n\n>")
        match(choice):
            case "1":
                friends = Friends(self.friend_db, self.user_db, self.username)
                friends.launch_friends_menu()
            case "2":
                print('chat launched')
                # chat = ChatClient()
                # chat.launch_chat()
            case "3":
                print('mailbox')
                # mail = Mailbox(messages)
                # mail.launch_mailbox_menu()
            case "q":
                self.user_db.close_connection()
                self.friend_db.close_connection()
                self.mail_db.close_connection()
                sys.exit(1)