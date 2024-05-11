import time
from utils.constants import ACTIVE_THRESHOLD

class UserActions:

    def __init__(self,db, cursor):
        self.db = db
        self.cursor = cursor

    def get_user_acct(self, username, password) -> tuple:
        query_string = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        self.cursor.execute(query_string)
        acct = self.cursor.fetchone()
        return acct

    def create_user_acct(self, username:str, password:str, ip:str, port:int) -> None:
        add_user = ("INSERT INTO users "
                    "(username, password, ip, port) "
                    "VALUES (%s, %s, %s, %s)")
        user_data = (username, password, ip,port)
        self.cursor.execute(add_user,user_data)
        self.db.commit()

    def get_user_data(self,username):
        query_string = f"SELECT ip,port FROM users WHERE username='{username}'"
        self.cursor.execute(query_string)
        data = self.cursor.fetchone()
        return data

    def username_exists(self, username:str) -> bool:
        query_string = f"SELECT * FROM users WHERE username='{username}'"
        self.cursor.execute(query_string)
        acct = self.cursor.fetchone()
        return True if acct else False

    def update_last_active(self, username:str) -> None:
        active = int(time.time())
        query_string = f"UPDATE users SET last_active={active} WHERE username='{username}'"
        self.cursor.execute(query_string)
        self.db.commit()

    def is_online(self, username:str) -> bool:
        query_string = f"SELECT last_active FROM users WHERE username='{username}'"
        self.cursor.execute(query_string)
        data = self.cursor.fetchone()
        
        last_active = data[0]
        now = int(time.time())
        return now - last_active < ACTIVE_THRESHOLD

    def update_ip(self, username, new_ip):
        query_string = f"UPDATE users SET ip='{new_ip}' WHERE username='{username}'"
        self.cursor.execute(query_string)
        self.db.commit()

    def close_connection(self):
        self.cursor.close()
        self.db.close()