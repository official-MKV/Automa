from ftplib import FTP 
import subprocess
import re
import time
import datetime
import os 

def connect_to_my_phone(mywifi):
    ssid = subprocess.check_output(['netsh','wlan','show','networks'])
    ssid = ssid.decode('utf-8')
    ssid_matches = re.findall(r"\s+SSID\s+\d+\s+[\s:]+(\w+)\s*",ssid)
    if len(ssid_matches)!=0:
        if mywifi in ssid_matches:
            connector = subprocess.check_output(['netsh','wlan','connect',mywifi])
            return [1,connector.decode('utf-8')]
        else:
            return[0,"Your devices was not detected."]
    else:
        return [0,"No Wifi Network was detected"]

def get_my_phone_ip():
    host = subprocess.check_output(['ipconfig'])
    text = host.decode('utf-8')
    match = re.findall(r"\s*Default\s+Gateway[.:\s]+\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})",text)
    host_ip = match[0]
    return host_ip
 
def download_videos(system_path, video_dir):
    try:
        ftp.cwd(video_dir)
        files = []
        ftp.dir(files.append)
        video_files = []
        for file in files:
            cleaned_output = re.findall(r"\s+(\d+[\_]\d+[\.]mp4)\s*",file) ##TODO: Adjust this to capture every video
            if len(cleaned_output)==1:
                video_files.append(cleaned_output[0])
        track_file_read = open(os.path.join(system_path,'track.txt'),'r')
        track_file_append = open(os.path.join(system_path,'track.txt'),'a')
        track_file = track_file_read.read()
        sub_video_files = video_files.copy()
        for video in sub_video_files:
            if video in track_file:
                video_files.remove(video)
            else:
                track_file_append.write(f'\n{video}')
            
        track_file_append.close()
        track_file_read.close()
        if len(video_files)>0:
            tic = time.perf_counter()
            for filename in video_files:
                print(f'Downloading...........{filename}')
                ##TODO: Code for a fancier terminal output
                file_path = os.path.join(system_path, filename)
                with open(file_path, "wb") as file:
                    ftp.retrbinary(f"RETR {filename}", file.write)
                ftp.delete(filename)
            toc = time.perf_counter()
            duration = time.strftime('%H:%M:%S',time.gmtime(toc-tic))

            print(f"Done downloading Videos. Duration:{duration}")
        else:
            print("No new files to download")
    except Exception as e:
        print(f"{video_dir} does not exist")
    




if __name__=="__main__":
    mywifi=""
    user=""
    password=""
    video_dir=""  #location of videos on phone
    system_path="" #location on system for videos to be stored
    msg =connect_to_my_phone(mywifi)
    if msg[0] !=0:
        time.sleep(5)
        host_ip = get_my_phone_ip()
                
        ftp= FTP()
        try:
            ftp.connect(host_ip,2121)
            ftp.login(user,password)
            print(ftp.getwelcome())
            download_videos(system_path,video_dir)
            ftp.quit()
        except Exception as er: 
            print(er)
    else: 
        print(msg[1])

    #TODO: Create an error log file
                

        

## Add loop to crontab

