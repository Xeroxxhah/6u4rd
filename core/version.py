import requests
import json

class Version():

    def __init__(self):

        self.currentVersion = 'v0.1.0'
        try:
            self.updatedVersion = str(requests.get('https://api.github.com/repos/Xeroxxhah/6u4rd/releases/latest').json().get('body'))
        except Exception:
            self.updatedVersion = None
            print('An Error Ocurred: Could not check latest version.')
    

    def IsUpdated(self):
        if self.currentVersion == self.updatedVersion:
            return True
        return False