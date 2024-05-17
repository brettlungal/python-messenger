import os
from tabulate import tabulate

class Friends:

    def __init__(self, friend_db, user_db, username):
        self.friend_db = friend_db
        self.user_db = user_db
        self.username = username
        self.pending_requests = self.friend_db.get_pending_friend_requests(self.username)
        self.received_requests = self.friend_db.get_friend_requests(self.username)
    
    def launch_friends_menu(self):
        while True:
            choice = input(f"1: Add Friend\n2: Show Friends List\n3: Show Friend Requests[{len(self.received_requests)}]\n4: Back\n>")
            os.system('cls')
            match(choice):
                case "1":
                    self.add_friend()
                case "2":
                    self.display_friends()
                case "3":
                    self.display_requests()
                case "4":
                    break
    
    def display_requests(self):
        print("Received Requests")
        print(tabulate(self.received_requests, headers=['Username','Sent At'], tablefmt='orgtbl'))
        print('\n')
        print("Sent Requests")
        print(tabulate(self.pending_requests, headers=['Username', 'Status' ,'Sent At'], tablefmt='orgtbl'))
        print('\n')

    def add_friend(self):
        friend_username = input('Enter your friends username: ')
        if self.user_db.username_exists(friend_username):
            success = self.friend_db.create_friend_request(self.username, friend_username)
            print("Friend request sent!") if success else print("Error sending friend request. Please try again.")
        else:
            print("Friends username does not exist!")
        self.user_db.update_last_active(self.username)

    def display_friends(self):
        friends = self.friend_db.get_friends(self.username)
        table_data = []
        for friend in friends:
            online = "Online" if self.user_db.is_online(friend) else "Offline"
            table_data.append([friend,online])
        print(tabulate(table_data, headers=['Friend', 'Status'], tablefmt='orgtbl'))
        print("\n")
        self.user_db.update_last_active(self.username)
