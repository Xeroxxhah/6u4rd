from socket import socket
import socket
import json
import secrets
import requests
from bs4 import BeautifulSoup


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
        except Exception as e:
            print(f'Exception: {e}')

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

        try:
            with open(self.config_path, 'w') as config:
                config.write(json_object)
        except Exception as e:
            print(e)

    
    def get_something(self):
        json_obj = requests.get('') 



class GeoStuff:

    def __init__(self) -> None:
        self.IP = self.get_public_ip()
        self.api_endpoint = f'https://ipgeolocation.io/ip-location/{self.IP}'
        self.continent_name = self.get_properties('continent_name')
        self.country_name = self.get_properties('country_name')
        self.country_capital = self.get_properties('country_capital')
        self.state = self.get_properties('state')
        self.latitude = self.get_properties('latitude')
        self.longitude = self.get_properties('longitude')


    def get_public_ip(self):
        try:
            return requests.get('https://api.ipify.org').text
        except Exception:
            return None
    

    def get_properties(self, property):
        properties = {}
        reponse = requests.get(self.api_endpoint)
        soup = BeautifulSoup(reponse.content, "html.parser")
        all_tags = soup.find_all('tr')

        for tag in all_tags:
            child_tag = tag.findChildren()

            if child_tag[0].text == 'IP':
                properties.update({'ip':child_tag[1].text})
            elif child_tag[0].text == 'Continent Name':
                properties.update({'continent_name':child_tag[1].text})
            elif child_tag[0].text == 'Country Name':
                properties.update({'country_name':child_tag[1].text})
            elif child_tag[0].text == 'Country Capital':
                properties.update({'country_capital':child_tag[1].text})
            elif child_tag[0].text == 'State/Province':
                properties.update({'state':child_tag[1].text})
            elif child_tag[0].text == 'Latitude & Longitude of City':
                properties.update({'latitude':child_tag[1].text.split(',')[0]})
                properties.update({'longitude':child_tag[1].text.split(',')[1]})
        
        try:
            return properties.get(property)
        except KeyError:
            return None




# Testing
"""
t = GeoStuff()

print(t.country_name)

"""


"""
h = Misc()

print(h.config_parser('auth_path'))"""

# Test pass