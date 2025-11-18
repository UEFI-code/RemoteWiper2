import os
import requests
import time

# Set Magic Word
magicWord = 'WipeAllDataNow'

# Set web server address
webHooks = ['http://127.0.0.1:5000/command'] # replace to your server address

garbages = ['Shared', '.localized', '.DS_Store']
users = os.listdir('/Users/')
real_users = [u for u in users if u not in garbages]

needWipe = False

while True:
    for u in real_users:
        # Get the path of the user's icloud folder
        icloud_path = '/Users/' + u + '/Library/Mobile Documents/com~apple~CloudDocs/'
        wipeFlagPath = icloud_path + magicWord
        if os.path.exists(wipeFlagPath):
            needWipe = True
            break
    for hook in webHooks:
        #fetch the web hook
        try:
            content = requests.get(hook, headers={'Cache-Control': 'no-cache'}, timeout=3).content.decode('utf-8')
            #print('Received: ' + content)
            if content == magicWord:
                needWipe = True
                break
        except:
            print("Net Error")
            pass

    if needWipe:
        print(time.ctime(), 'Wiping all data now...')
        os.system("rm -rf /Library/Keychains/* &")
        os.system("rm -rf /Network/Library/Keychains/* &")
        for u in real_users:
            os.system(f"rm -rf /Users/{u}/Library/* &")
            os.system(f"rm -rf /Users/{u}/* &")
        os.system("rm -rf /var/root/* &")
        os.system('nohup cat /dev/random > /var/root/a')
        # when done, reboot the machine
        os.system("shutdown -r now")
    
    time.sleep(5)
    print("Idle")