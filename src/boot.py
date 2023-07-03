from config import cfg
from wlanc import wlanc
#import webrepl

wlanc (cfg["wlan"]["ssid"], cfg["wlan"]["pswd"])
#webrepl.start()
