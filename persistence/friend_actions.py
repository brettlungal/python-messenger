
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
                    "(from_username, to_username, status, sent_at) "
                    "VALUES (%s, %s, %s, %s)")
        friendship_data = (from_username, to_username, "PENDING",str(datetime.now(timezone.utc)))
        try:
            self.cursor.execute(add_friend,friendship_data)
            self.db.commit()
            return True
        except Exception as e:
            return False
        
    def update_pending_friend_request(self, to_username, from_username, new_status) -> bool:
        add_friend = ("update friend_request set status = %s where from_username=%s and to_username=%s and status='PENDING'")
        friendship_data = (new_status,from_username, to_username)
        try:
            resp = self.cursor.execute(add_friend,friendship_data)
            print(resp)
            com_resp = self.db.commit()
            print(com_resp)
            return True
        except Exception as e:
            print(e)
            return False
        
    
    def accept_friend_request(self, request, current_user):
        self.create_friendship(current_user, request[0])
        success = self.update_pending_friend_request(current_user, request[0],'ACCEPTED')
        return success

    def reject_friend_request(self, request, current_user):
        success = self.update_pending_friend_request(current_user, request[0],'REJECTED')
        return success

        
    def get_pending_friend_requests(self, from_username):
        query_string = f"SELECT to_username, status, sent_at FROM friend_request WHERE from_username='{from_username}' AND status='PENDING'"
        self.cursor.execute(query_string)
        requests = self.cursor.fetchall()
        formatted_requests = [[friend_req[0],friend_req[1], friend_req[2].replace(tzinfo=timezone.utc).astimezone(tz=None)] for friend_req in requests]
        return formatted_requests

    def get_friend_requests(self, to_username):
        query_string = f"SELECT from_username, sent_at FROM friend_request WHERE to_username='{to_username}' AND status='PENDING'"
        self.cursor.execute(query_string)
        requests = self.cursor.fetchall()
        formatted_requests = [[friend_req[0],friend_req[1].replace(tzinfo=timezone.utc).astimezone(tz=None)] for friend_req in requests]
        return formatted_requests

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