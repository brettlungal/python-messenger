import sys
import os
# Persistence
from persistence.user_actions import UserActions
from persistence.friend_actions import FriendActions

# Interfaces
from interfaces.chat import ChatClient
from interfaces.friends import Friends


class Menu:

    def __init__(self, user_info, db, cursor):
        self.username = user_info[0]
        self.host = user_info[2]
        self.port = user_info[3]
        self.user_db = UserActions(db, cursor)
        self.friend_db = FriendActions(db, cursor)


    def show(self):
        friend_requests = len(self.friend_db.get_friend_requests(self.username))
        while True:

            choice = input(f"1: Friends[{friend_requests}]\n2: Start Chat(Under Construction)\nq: Quit\n\n>")
            os.system('cls')
            match(choice):
                case "1":
                    friends = Friends(self.friend_db, self.user_db, self.username)
                    friends.launch_friends_menu()
                case "2":
                    print('chat launched')
                case "q":
                    self.user_db.close_connection()
                    self.friend_db.close_connection()
                    sys.exit(1)