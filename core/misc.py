from socket import socket
import socket
import json
import secrets


class Misc():

    def __init__(self) -> None:
        self.config_path = 'C:\\Windows\\System32\\6u4rd.conf'
        self.config = {
            "host":"0.0.0.0",
            "port":1337,
            "code_name": self.gethost(),
            "auth_path":"C:\\Windows\\System32\\6u4rd.key",
            "integ_path":"C:\\Windows\\System32\\6u4rd.integ",
            "sender_mail":"",
            "sender_password":"",
            "receiver_mail":"",
            "app_sk": secrets.token_hex(16)
        }

    def getip(self):
        try:
            sok = socket(socket.AF_INET, socket.SOCK_STREAM)
            sok.connect(('8.8.8.8',53))
            ip = sok.getsockname()[0]
            sok.close()
            return ip
        except:
            pass

    def gethost(self):
        return str(socket.gethostname())

    def config_parser(self, key):
        config_content = {}
        try:
            with open(self.config_path, 'r') as config:
                config_content = json.load(config)
                return config_content.get(key)
        except:
            pass

    def config_write(self,host="0.0.0.0",
    port=1337,
    code_name='',
    auth_path="C:\\Windows\\System32\\6u4rd.key",
    integ_path="C:\\Windows\\System32\\6u4rd.integ"
    ,sender_mail='',
    sender_password='',
    receiver_mail='',
    app_sk = secrets.token_hex(16)
    ):
        self.config["host"]=host
        self.config["port"]=port
        self.config["code_name"]=code_name
        self.config["auth_path"]=auth_path
        self.config["integ_path"]=integ_path
        self.config["sender_mail"]=sender_mail
        self.config["sender_password"]=sender_password
        self.config["receiver_mail"]=receiver_mail
        self.config["app_sk"]=app_sk

        json_object = json.dumps(self.config, indent=4)

        with open(self.config_path, 'w') as config:
            config.write(json_object)



# Testing
"""
h = Misc()

print(h.config_parser('auth_path'))"""

# Test pass