import requests
import pwinput

from utils.constants import DEFAULT_PORT

class Login:
    def __init__(self, user_db):
        self.logged_in_user = tuple()
        self.user_db = user_db

    def get_public_ip(self) -> str:
        # TODO add error handling here
        ip = requests.get('https://api.ipify.org').content.decode('utf8')
        return ip

    def handle_login(self, username:str ,password:str) -> tuple:
        user = self.user_db.get_user_acct(username, password)
        return user

    def handle_signup(self, username:str, password:str) -> None:
        # TODO return boolean if acct creation was successful or not
        # TODO add password requirements and rejections for invalid passwords
        # TODO add password encryption
        user_ip = self.get_public_ip()
        self.user_db.create_user_acct(username, password, user_ip, DEFAULT_PORT)

    def login_logic(self) -> bool:
        # TODO clean this up - lots of cleanup needed
        success = False
        while not success:
            username = input('Username: ')
            if username.lower() == 'q':
                return None
            password = pwinput.pwinput('Password: ')
            success = self.handle_login(username,password)
            if not success:
                print("Incorrect username or password please try again or (Q) to return to previous menu")
        if success:
            self.logged_in_user = success
            current_ip = self.get_public_ip()
            if current_ip != self.logged_in_user[2]:
                self.user_db.update_ip(self.logged_in_user[0], current_ip)
        return success

    def signup_logic(self) -> None:
        # TODO add option to quit from signup logic - currently only way out is successful signup
        # TODO add logic to handle failed signup
        user_exists = True
        while user_exists:
            username = input("Choose a username: ")
            user_exists = self.user_db.username_exists(username)
            if user_exists:
                print("Username already exists, please enter another.")
        password = pwinput.pwinput('Enter a password: ')
        self.handle_signup(username,password)
