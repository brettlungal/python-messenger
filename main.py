import requests
import pwinput
from interfaces.menu import Menu
from utils.constants import DEFAULT_PORT
from persistence.user_actions import UserActions
from dotenv import load_dotenv
import mysql.connector
import os
from dotenv import load_dotenv
import mysql.connector

'''
TODO items from pre-alpha testing
    0: loop not exiting upon signin and trying to treat it as a signin --done
    1: friend request actually goes to the friend to add them back
    2: last active trackers for actual online input (and add field to new accts)
    3: investigate file descriptor issue with socket communication
    4: get public ip upon login and update it if changed from whats in table -- done
'''

class PythonChat:

    def __init__(self):
        load_dotenv()
        self.db = mysql.connector.connect(user=os.environ['DB_USER'], password=os.environ['DB_PASS'], host=os.environ['DB_HOST'], database=os.environ['DB_NAME'])
        self.cursor = self.db.cursor()
        self.logged_in_user = tuple()
        self.user_db = UserActions(self.db,self.cursor)

    def get_public_ip(self) -> str:
        ip = requests.get('https://api.ipify.org').content.decode('utf8')
        return ip

    def handle_login(self, username:str ,password:str) -> tuple:
        user = self.user_db.get_user_acct(username, password)
        return user

    def handle_signup(self, username:str, password:str) -> None:
        #TODO return boolean if acct creation was successful or not
        user_ip = self.get_public_ip()
        self.user_db.create_user_acct(username, password, user_ip, DEFAULT_PORT)

    def login_logic(self) -> bool:
        # TODO clean this up - lots of cleanup needed
        success = False
        startup = True
        while not success:
            username = input('Username: ')
            if username.lower() == 'q':
                break
            password = pwinput.pwinput('Password: ')
            success = self.handle_login(username,password)
            if not success:
                print("Incorrect username or password please try again or (Q) to return to previous menu")
        if success:
            startup = False
            self.logged_in_user = success
            current_ip = self.get_public_ip()
            if current_ip != self.logged_in_user[2]:
                self.user_db.update_ip(self.logged_in_user[0], current_ip)
        return startup

    def signup_logic(self) -> None:
        user_exists = True
        while user_exists:
            username = input("Choose a username: ")
            user_exists = self.user_db.username_exists(username)
            if user_exists:
                print("Username already exists, please enter another.")
        password = pwinput.pwinput('Enter a password: ')
        self.handle_signup(username,password)

    def run(self):
        print("""             ____________________________________________________
                /                                                    \\
            |    _____________________________________________     |
            |   |                                             |    |
            |   |  Welcome to python messenger.               |    |
            |   |  v1.0                                       |    |
            |   |                                             |    |
            |   |  (1) Login                                  |    |
            |   |  (2) SignUp                                 |    |
            |   |                                             |    |
            |   |                                             |    |
            |   |                                             |    |
            |   |                                             |    |
            |   |  Created by Brett Lungal                    |    |
            |   |  www.brettlungal.com                        |    |
            |   |                                             |    |
            |   |_____________________________________________|    |
            |                                                      |
                \_____________________________________________________/
                    \_______________________________________/
                    _______________________________________________
                _-'    .-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.  --- `-_
            _-'.-.-. .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.--.  .-.-.`-_
        _-'.-.-.-. .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-`__`. .-.-.-.`-_
        _-'.-.-.-.-. .-----.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-----. .-.-.-.-.`-_
    _-'.-.-.-.-.-. .---.-. .-----------------------------. .-.---. .---.-.-.-.`-_
    :-----------------------------------------------------------------------------:
    `---._.-----------------------------------------------------------------._.---'
    """)
        startup = True
        while startup:
            loginChoice = input('Enter option: ')
            if ( loginChoice == '1'):
                # User chose to login
                startup = self.login_logic()
            elif ( loginChoice == '2'):
                # User chose to create an account
                self.signup_logic()
                # TODO add some sort of successful signup message
                continue
            else:
                print("Invalid entry")
        menu = Menu(self.logged_in_user, self.db, self.cursor)
        while True:
            menu.get_options()
        #Just in case I guess
        self.user_db.close_connection()


if __name__ == "__main__":
    chat = PythonChat()
    chat.run()

