from persistence.user_actions import UserActions
from persistence.friend_actions import FriendActions
from tabulate import tabulate

class Menu:

    def __init__(self, user_info, db, cursor):
        self.username = user_info[0]
        self.host = user_info[2]
        self.port = user_info[3]
        self.user_db = UserActions(db, cursor)
        self.friend_db = FriendActions(db, cursor)

    def get_options(self):
        choice = input("1: Add Friends\n2: Show friends\n")
        if choice == "1":
            friend_username = input("Enter friends username: ")
            self.add_friend(friend_username)
        elif choice == "2":
            self.display_friends()
        elif choice == "q":
            self.user_db.close_connection()
            self.friend_db.close_connection()
        
    
    def add_friend(self,friend_username):
        if self.user_db.username_exists(friend_username):
            self.friend_db.create_friendship(self.username, friend_username)
        else:
            print("Friends username does not exist!")

    def display_friends(self):
        friends = self.friend_db.get_friends(self.username)
        for i in range(len(friends)):
            friends[i] = list(friends[i])
            friends[i].append("offline")
        print("\n\n")
        print(tabulate(friends, headers=['Friend', 'Status'], tablefmt='orgtbl'))
        print("\n\n")