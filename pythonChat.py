from client import Client
import mysql.connector
import urllib.request
import ssl
import pwinput
db = mysql.connector.connect(user='python', password='&MotoX2192011!', host='184.64.57.111', database='python_messenger')
cursor = db.cursor()

class PythonChat:

    def __init__(self):
        self.logged_in_user = tuple()

    def get_public_ip(self) -> str:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        external_ip = urllib.request.urlopen('https://ident.me', context=ctx).read().decode('utf8')
        return external_ip

    def handle_login(self, username:str ,password:str ) -> bool:
        queryString = f"SELECT * FROM user WHERE username='{username}' AND password='{password}'"
        cursor.execute(queryString)
        acct = cursor.fetchone()
        return acct

    def handle_signup(self, username:str, password:str) -> None:
        add_user = ("INSERT INTO user "
            "(username, password, ip, port) "
            "VALUES (%s, %s, %s, %s)")
        ip = get_public_ip()
        user_data = (username, password, ip,'9000')
        cursor.execute(add_user,user_data)
        db.commit()

    def username_exists(self, username:str) -> bool:
        queryString = f"SELECT * FROM user WHERE username='{username}'"
        cursor.execute(queryString)
        acct = cursor.fetchone()
        return True if acct else False

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
        return startup

    def signup_logic(self) -> None:
        user_exists = True
        while user_exists:
            username = input("Choose a username: ")
            user_exists = username_exists(username)
            if user_exists:
                print("Username already exists, please enter another.")
        password = pwinput.pwinput('Enter a password: ')
        handle_signup(username,password)

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
        try:
            startup = True
            while startup:
                loginChoice = input('Enter option: ')
                if ( loginChoice == '1'):
                    # User chose to login
                    startup = self.login_logic()
                elif ( loginChoice == '2'):
                    # User chose to create an account
                    self.signup_logic()
                    break
                else:
                    print("Invalid entry")
            
            # If were here, startup sequence is complete and were logged in
            #TODO launch something
            print("Current logged in user info...")
            print(self.logged_in_user)

            # Lastly close connection
            cursor.close()
            db.close()
        except:
            print("Something went wrong - closing connections")
            cursor.close()
            db.close()

if __name__ == "__main__":
    chat = PythonChat()
    chat.run()

