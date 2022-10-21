from flask import Flask
from pyngrok import ngrok
from core.misc import Misc


helper = Misc()
class App():
    def __init__(self):
        self.app = Flask(__name__)
        #'Mydamnsecretkey'
        self.app.config['SECRET_KEY'] = helper.config_parser('app_sk')
        self.host = helper.config_parser('host')
        self.port = helper.config_parser('port')
        self.debug = False
    
    def create_app(self):
        return self.app
    

    def run(self):
        self.app.run(host=self.host, port=self.port, debug=self.debug)
    
    def create_ngrok(self):
        ngrok_instance = ngrok.connect(self.port)
        return ngrok_instance

