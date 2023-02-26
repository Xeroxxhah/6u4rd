import hashlib
import pyAesCrypt
import os
from .misc import Misc
import random
from .mail import EmailSender

helper = Misc()

class Auth():
    
    def __init__(self,authkey,code_name = helper.gethost()):
        self.authkey = authkey
        self.isAuthenticated = False
        self.is_2fa_enabled = bool(helper.config_parser('2fa_enabled'))
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


class TwoFactorAuth:

    def __init__(self):

        self.key_size = 6
        self.only_nums = False
        self.__key = None
        self.mailer = EmailSender()

    @property
    def key(self):
        return self.__key


    @key.setter
    def key(self):
        raise ValueError("Cannot set `key`")


    def key_gen(self):
        
        if self.only_nums:
            key_list = ["".join([str(random.randint(0,9)) for _ in range(self.key_size) ]) for _ in range(self.key_size)]
            key = "".join(["".join(key_list[i][random.randint(0,self.key_size - 1)]) for i in range(6)])
            self.__key = key
        else:
            key_list = ["".join([str(random.randint(0,9)) for _ in range(self.key_size) ]) for _ in range(self.key_size)]
            key_phase1 = "".join(["".join(key_list[i]) for i in range(6)])
            key = hashlib.sha256(key_phase1.encode()).hexdigest()[0:self.key_size]
            self.__key = key

    def verify_key(self, key):
        return (True if hashlib.sha256(key.encode()).hexdigest() == hashlib.sha256(self.__key.encode()).hexdigest() else False)

    def send_key(self):
        self.mailer.send_email('6u4rd OTP', f'6u4rd OTP: {self.__key}')
    



 

