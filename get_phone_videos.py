from ftplib import FTP 
import subprocess
import re
import time
import datetime
import os 

## Cleanup-code

## Connect to the hotspot
ssid = subprocess.check_output(['netsh','wlan','show','networks'])
ssid = ssid.decode('utf-8')
ssid_matches = re.findall(r"\s+SSID\s+\d+\s+[\s:]+(\w+)\s*",ssid)
if len(ssid_matches)!=0:
    for match in ssid_matches:
        print(match)
    ssid_to_connect = ssid_matches[0]
    connector = subprocess.check_output(['netsh','wlan','connect',ssid_to_connect])
    print(connector.decode('utf-8'))
else:
    print("No Wifi was detected")

time.sleep(5)
## Get the Host IP
host = subprocess.check_output(['ipconfig'])
text = host.decode('utf-8')
match = re.findall(r"\s*Default\s+Gateway[.:\s]+\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})",text)
host_ip = match[0]
 
## Get user and password
user ='test'
password = 'test'

## Connect to FTP server 
ftp= FTP()
try:
    ftp.connect(host_ip,2121)
    ftp.login(user,password)
    print(ftp.getwelcome())
except Exception as er: 
    print(er)

## Download necessary videos
phone_videos_path = 'C:\\Users\\vemma\\Videos\\phone'
download_dir='DCIM/Camera'
ftp.cwd(download_dir)
files = []
ftp.dir(files.append)
video_files = []
for file in files:
    cleaned_output = re.findall(r"\s+(\d+[\_]\d+[\.]mp4)\s*",file)
    if len(cleaned_output)==1:
        video_files.append(cleaned_output[0])

 
##TODO: Write code to create restrict downloads to only new_files
track=1
for filename in video_files:
    print('Downloading...........',track)
    ##TODO: Code for a fancier terminal output
    file_path = os.path.join(phone_videos_path, filename)
    with open(file_path, "wb") as file:
        ftp.retrbinary(f"RETR {filename}", file.write)
    track+=1
    ftp.delete(filename)





## Disconnect from server 

ftp.quit()
## Add loop to crontab

