import hashlib
import pyAesCrypt
import os
from .misc import Misc

helper = Misc()

class Auth():
    
    def __init__(self,authkey,code_name = helper.gethost()):
        self.authkey = authkey
        self.isAuthenticated = False
        self.code_name = code_name
        self.auth_path = helper.config_parser('auth_path')
        self.integ_path = helper.config_parser('integ_path')
        #self.filename = os.path.basename(self.auth_path)


    def check_auth_integrity(self):
        try:
            pyAesCrypt.decryptFile(f'{self.integ_path}.lock', self.integ_path, self.authkey)
            with open(self.integ_path, 'r') as stored_checksum:
                content_stored_checksum = stored_checksum.read()
            with open(self.auth_path, 'rb') as auth_checksum:
                if str(hashlib.sha256(auth_checksum.read()).hexdigest()) == content_stored_checksum:
                    pyAesCrypt.encryptFile(self.integ_path,f"{self.integ_path}.lock",self.authkey)
                    return True
                else:
                    pyAesCrypt.encryptFile(self.integ_path,f"{self.integ_path}.lock",self.authkey)
                    return False
        except ValueError:
            print("Authentication Failed!!!")
            return None


    def create_authkey(self):
        integ = ''
        with open(self.auth_path, 'w') as auth:
            integ = hashlib.sha256(str(hashlib.sha256(self.authkey.encode()).hexdigest()).encode()).hexdigest()
            auth.write(hashlib.sha256(self.authkey.encode()).hexdigest())
        with open(self.integ_path,'w') as integ_write:
            integ_write.write(integ)
        pyAesCrypt.encryptFile(self.integ_path,f"{self.integ_path}.lock",self.authkey)
        os.remove(self.integ_path)
    
    
    def authenticate(self):
        if self.check_auth_integrity():
            with open(self.auth_path, 'r') as auth:
                if str(hashlib.sha256(self.authkey.encode()).hexdigest()) == auth.read():
                    self.isAuthenticated = True
    
    def is_first(self):
        if os.path.exists(self.auth_path):
            return False
        return True
    
    def remove_auth(self):
        if self.isAuthenticated:
            if os.path.exists(self.auth_path):
                os.remove(self.auth_path)
            if os.path.exists(self.integ_path):
                os.remove(self.integ_path)
            if os.path.exists(f'{self.integ_path}.lock'):
                os.remove(f'{self.integ_path}.lock')
            if os.path.exists('C:\\Windows\\System32\\6u4rd.mail'):
                os.remove('C:\\Windows\\System32\\6u4rd.mail')
        else:
            print("Authentication failed")


    def revoke_authentication(self):
        self.isAuthenticated = False

    def getcodename(self):
        return helper.config_parser('code_name')

