from tabulate import tabulate

class Friends:

    def __init__(self, friend_db, user_db, username):
        self.friend_db = friend_db
        self.user_db = user_db
        self.username = username
    
    def launch_friends_menu(self):
        choice = input("1: Add Friend\n2: Show Friends List\n3: Back\n>")
        match(choice):
            case "1":
                print('add friend')
            case "2":
                self.display_friends()
            case "3":
                pass
        

    def add_friend(self):
        friend_username = input('Enter your friends username: ')
        if self.user_db.username_exists(friend_username):
            self.friend_db.create_friendship(self.username, friend_username)
        else:
            print("Friends username does not exist!")
        self.user_db.update_last_active(self.username)

    def display_friends(self):
        friends = self.friend_db.get_friends(self.username)
        table_data = []
        for friend in friends:
            online = "Online" if self.user_db.is_online(friend) else "Offline"
            table_data.append([friend,online])
        print("\n\n")
        print(tabulate(table_data, headers=['Friend', 'Status'], tablefmt='orgtbl'))
        print("\n\n")
        self.user_db.update_last_active(self.username)
