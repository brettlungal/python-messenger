
from datetime import datetime, timezone

class FriendActions:

    def __init__(self, db, cursor):
        self.db = db
        self.cursor = cursor

    def get_friends(self, username) -> tuple:
        query_string = f"SELECT friend_username FROM friends WHERE username='{username}'"
        self.cursor.execute(query_string)
        friends = self.cursor.fetchall()
        formatted_friends = [friend[0] for friend in friends]
        return formatted_friends
    
    def create_friend_request(self, from_username, to_username) -> bool:
        add_friend = ("INSERT INTO friend_request "
                    "(from_username, to_username, status, send_at) "
                    "VALUES (%s, %s, %s, %s)")
        friendship_data = (from_username, to_username, "PENDING",datetime.now(timezone.utc))
        try:
            self.cursor.execute(add_friend,friendship_data)
            self.db.commit()
            return True
        except Exception as e:
            return False

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