from client import Client
import mysql.connector
import urllib.request
import pwinput
db = mysql.connector.connect(user='python', password='&MotoX2192011!', host='184.64.57.111', database='python_messenger')
cursor = db.cursor()


def handle_login(username:str ,password:str ) -> bool:
    queryString = f"SELECT * FROM user WHERE username='{username}' AND password='{password}'"
    cursor.execute(queryString)
    acct = cursor.fetchone()
    return acct

def handle_signup(username:str, password:str) -> None:
    add_user = ("INSERT INTO user "
        "(username, password, ip, port) "
        "VALUES (%s, %s, %s, %s)")
    ip = get_public_ip()
    user_data = (username, password, ip,'9000')
    cursor.execute(add_user,user_data)
    db.commit()

def get_public_ip():
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    return external_ip

if __name__ == "__main__":
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
            success = False
            while not success:
                username = input('Username: ')
                if username.lower() == 'q':
                    break
                password = pwinput.pwinput('Password: ')
                success = handle_login(username,password)
                if not success:
                    print("Incorrect username or password please try again or (Q) to return to previous menu")
            
            if success:
                startup = False

        elif ( loginChoice == '2'):
            pass
            break
        else:
            print("Invalid entry")
    
    cursor.close()
    db.close()

