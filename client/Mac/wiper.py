import os
my_pid = os.getpid()
import psutil
import requests
import time

# Set Magic Word
magicWord = 'WipeAllDataNow'

# Set web server address
webHooks = ['http://127.0.0.1:5000/command'] # replace to your server address

garbages = ['Shared', '.localized', '.DS_Store']
real_users = [u for u in os.listdir('/Users/') if u not in garbages]

def chk_need_wipe():
    for u in real_users:
        # Get the path of the user's icloud folder
        icloud_path = '/Users/' + u + '/Library/Mobile Documents/com~apple~CloudDocs/'
        wipeFlagPath = icloud_path + magicWord
        if os.path.exists(wipeFlagPath): return True
    for hook in webHooks:
        try:
            content = requests.get(hook, headers={'Cache-Control': 'no-cache'}, timeout=3).content.decode('utf-8')
            #print('Received: ' + content)
            if content == magicWord: return True
        except:
            print("Net Error")
    return False

while True:
    if chk_need_wipe():
        print(time.ctime(), 'Wiping all data now...')
        # delete keychains
        os.system("rm -rf /Library/Keychains/* &")
        os.system("rm -rf /Network/Library/Keychains/* &")
        # delete user data
        for u in real_users:
            os.system(f"rm -rf /Users/{u}/Library/* &")
            os.system(f"rm -rf /Users/{u}/* &")
        os.system("rm -rf /var/root/* &")
        # kill all processes except root and self
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            if proc.info['pid'] != my_pid and proc.info['username'] != 'root':
                print(f"Attempting to kill process: {proc.info}")
                os.system(f"kill -9 {proc.info['pid']} &")
        # fill disk space with garbage data
        os.system('nohup cat /dev/random > /var/root/a')
        # when done, reboot the machine
        os.system("shutdown -r now")
    
    time.sleep(5)
    print("Idle")