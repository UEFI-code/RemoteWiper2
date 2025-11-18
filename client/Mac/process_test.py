import os
import psutil

my_pid = os.getpid()
print(f"My PID: {my_pid}")

for proc in psutil.process_iter(['pid', 'name', 'username']):
    print(proc.info)
    if proc.info['pid'] != my_pid and proc.info['username'] != 'root':
        print('This process might be killable!')