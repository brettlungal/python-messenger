
class FriendActions:

    def __init__(self, db, cursor):
        self.db = db
        self.cursor = cursor

    def get_friends(self, username) -> tuple:
        queryString = f"SELECT friend_username FROM friends WHERE username='{username}'"
        self.cursor.execute(queryString)
        friends = self.cursor.fetchall()
        return friends

    def create_friendship(self, current_user:str, friend_user:str) -> None:
        add_friend = ("INSERT INTO friends "
                    "(username, friend_username) "
                    "VALUES (%s, %s)")
        friendship_data = (current_user, friend_user)
        self.cursor.execute(add_friend,friendship_data)
        self.db.commit()

    def close_connection(self):
        self.cursor.close()
        self.db.close()