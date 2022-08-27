
class UserActions:

    def __init__(self,db, cursor):
        self.db = db
        self.cursor = cursor

    def get_user_acct(self, username, password) -> tuple:
        queryString = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        self.cursor.execute(queryString)
        acct = self.cursor.fetchone()
        return acct

    def create_user_acct(self, username:str, password:str, ip:str, port:int) -> None:
        add_user = ("INSERT INTO users "
                    "(username, password, ip, port) "
                    "VALUES (%s, %s, %s, %s)")
        user_data = (username, password, ip,port)
        self.cursor.execute(add_user,user_data)
        self.db.commit()

    def username_exists(self, username:str) -> bool:
        queryString = f"SELECT * FROM users WHERE username='{username}'"
        self.cursor.execute(queryString)
        acct = self.cursor.fetchone()
        return True if acct else False

    def close_connection(self):
        self.cursor.close()
        self.db.close()