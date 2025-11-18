import os
import psutil

non_kill_usrs = ['root', '_analyticsd', '_coreaudiod', '_hidd', '_trustd', '_windowserver', '_locationd']
my_pid = os.getpid()
print(f"My PID: {my_pid}")

for proc in psutil.process_iter(['pid', 'name', 'username']):
    print(proc.info)
    if proc.info['pid'] != my_pid and proc.info['username'] not in non_kill_usrs:
        print('This process might be killable!')
        if input('Kill it? (y/n) ') == 'y':
            os.system(f"kill -9 {proc.info['pid']} &")