# Misc
import os
import sys
from dotenv import load_dotenv
import mysql.connector

# Interfaces
from interfaces.menu import Menu
from interfaces.login import Login

# Persistence
from persistence.user_actions import UserActions

# Constants
from utils.constants import WELCOME_MENU

class PythonChat:

    def __init__(self):
        load_dotenv()
        self.db = mysql.connector.connect(user=os.environ['DB_USER'], password=os.environ['DB_PASS'], host=os.environ['DB_HOST'], database=os.environ['DB_NAME'])
        self.cursor = self.db.cursor()
        self.user_db = UserActions(self.db,self.cursor)

    def run(self):
        login_helper = Login(self.user_db)
        signed_in = False
        while not signed_in:
            print(WELCOME_MENU)
            # TODO add welcome menu and login choice to its own class to encapsulate display and options in one place
            login_choice = input('Enter Option: ')
            match(login_choice):
                case "1":
                    authenticated_user = login_helper.login_logic()
                    if authenticated_user:
                        signed_in = True
                case "2":
                    login_helper.signup_logic()
                case "3":
                    self.user_db.close_connection()
                    sys.exit()

        menu = Menu(authenticated_user, self.db, self.cursor)
        menu.show()
        self.user_db.close_connection()


if __name__ == "__main__":
    chat = PythonChat()
    chat.run()

