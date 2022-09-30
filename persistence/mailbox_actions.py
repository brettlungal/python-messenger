

class MailboxActions:

    def __init__(self,db, cursor):
        self.db = db
        self.cursor = cursor

    def get_new_messages(self, username:str) -> list:
        query_string = f"SELECT from_username,message,mail_id FROM mailbox WHERE to_username='{username}' and is_read=0"
        self.cursor.execute(query_string)
        data = self.cursor.fetchall()
        return data

    def get_all_messages(self, username:str) -> list:
        query_string = f"SELECT from_username,message,mail_id FROM mailbox WHERE to_username='{username}'"
        self.cursor.execute(query_string)
        data = self.cursor.fetchall()
        return data

    def close_connection(self):
        self.cursor.close()
        self.db.close()