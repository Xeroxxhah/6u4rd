import getpass
from core.auth import Auth
from core.mail import Mailer
from core.misc import Misc
from core.version import Version
from pyngrok import ngrok
import secrets


helper = Misc()
dummy_password = 'pass' 
auth = Auth(dummy_password)
mailer = Mailer()
version = Version()
app_auth = None
email= ''
password = ''
receiver_mail = ''

helper.config_write()

if auth.is_first():
    print("Welcome to 6u4rd")
    
    try:
        code_name = input(f"Enter code name ({helper.gethost()}): ")
        if len(code_name) != 0:
            auth.code_name = code_name
        auth.create_authkey()
        print('-'*50)
        print("Authentication Key created: {}".format(dummy_password))
        print('-'*50)
        ch = input("""
        Warning: Sender's Email address and password are being stored in plain text. 
        Please do NOT use your personal email address and password instead user DUMMY email account.
        I understand the risks and i am not using my personal information. (Y/N): 
        
        """)
        print("Sender's email info: \n")
        if ch.lower() == "y":
            email = input("Enter your email address: ")
            password = getpass.getpass("Enter your password: ")
            receiver_mail = input("Enter receiver email address: ")
        else:
            print("Quiting...")
            quit()
        print("\nSetting up ngrok...")
        ngrok_token = input("Enter ngrok token: ")
        ngrok.set_auth_token(ngrok_token)
        print('\n')
        host = input(f'Enter host address ({helper.config["host"]}): ')
        host = helper.config["host"] if len(host) == 0 else host
        port = input(f'Enter port number: ({helper.config["port"]}): ')
        port = helper.config["port"] if len(port) == 0 else port
        auth_path = input(f'Enter auth path: ({helper.config["auth_path"]}): ')
        auth_path = helper.config["auth_path"] if len(auth_path) == 0 else auth_path
        integ_path = input(f'Enter integ path: ({helper.config["integ_path"]}): ')
        integ_path = helper.config["integ_path"] if len(integ_path) == 0 else integ_path
        app_sk = secrets.token_hex(16)
        print(f"FLASK SECRET KEY: {app_sk}")
        helper.config_write(host=host,port=port,code_name=code_name,auth_path=auth_path,integ_path=integ_path,sender_mail=email,sender_password=password,receiver_mail=receiver_mail,app_sk=app_sk)
    except PermissionError:
        print("Run as administrator")
        quit()

print(f'Version: {version.currentVersion}')

if not version.IsUpdated():
    print(f'New version available: {version.updatedVersion}')


print("Code Name: {}".format(auth.code_name))


def change_auth_key(old_key,new_key):
    try:
        change_key = Auth(old_key)
        change_key.authenticate()
        if change_key.isAuthenticated:
            change_key.remove_auth()
            new_key = Auth(new_key)
            new_key.create_authkey()
            print("[+] Auth key changed successfully")

            ch = input("""
            Warning: Sender's Email address and password are being stored in plain text. 
            Please do NOT use your personal email address and password instead user DUMMY email account.
            I understand the risks and i am not using my personal information. (Y/N): """)
            if ch.lower() == "y":
                email = input("Enter your email address: ")
                password = getpass.getpass("Enter your password: ")
                receiver_mail = input("Enter receiver email address: ")
                app_sk = secrets.token_hex(16)
                print(f"FLASK SECRET KEY: {app_sk}")
                helper.config_write(sender_mail=email,sender_password=password,receiver_mail=receiver_mail,app_sk=app_sk)
                print('Configuration Saved successfully...')
            else:
                print("Quiting...")
                quit()
        else:
            print("[-] Authentication failed")
    except PermissionError:
        print("[-] Run as administrator")
        quit()

def main():
    menu = """
    1: Change Auth Key
    2: Delete Authentication
    3: exit
    """
    print(menu)
    option = input("Choose Option:")
    if option == "1":
        old_key = getpass.getpass("old key: ")
        new_key = getpass.getpass("new key: ")
        change_auth_key(old_key,new_key)
    elif option == "3":
        exit()
    elif option == "2":
        key = getpass.getpass("Enter key: ")
        delete_auth = Auth(key)
        delete_auth.authenticate()
        delete_auth.remove_auth()
        print("Authentication removed successfully")
main()

