from copyreg import pickle
from ftplib import FTP 
import subprocess
import re
import time
import datetime
import os 
from progress.bar import ChargingBar
##TODO: write android app to start ftp server when my laptop/device is detected

def scan_wifi(mywifi):
    ##TODO:Write code to check to see if my hotspot or wifi is on
    ssid = subprocess.check_output(['netsh','wlan','show','networks'])
    ssid = ssid.decode('utf-8')
    ssid_matches = re.findall(r"\s+SSID\s+\d+\s+[\s:]+(\w+)\s*",ssid)
    if len(ssid_matches)!=0:
        if mywifi in ssid_matches:
            return [True,{"msg":"wifi found"}]
        else:
            return [False,{"msg":"wifi not found"}]
    else:
        return "I think your wifi is off"

def connect_to_wifi(mywifi):
    try:
        connector = subprocess.check_output(['netsh','wlan','connect',mywifi])
        return [True,{"msg":connector.decode('utf-8')}]
    except Exception as e:
        return [ False,{"msg":"Unable to connect to wifi try again in 5 minutes"}]
        ##TODO: log the error and stop the program

def get_host_ip():
    host = subprocess.check_output(['ipconfig'])
    text = host.decode('utf-8')
    match = re.findall(r"\s*Default\s+Gateway[.:\s]+\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})",text)
    host_ip = match[0]
    return host_ip  

class FileObj:
    def __init__(self,file):
        self.permissions=file[0]
        self.user_id= file[1]
        self.user_name = file[2]
        self.file_size = file[4]
        self.date_created=[file[5],file[6],file[7]]
        self.file_name =file[8]
        self.is_file= self.is_file_check()
        self._path =None
   
    def is_file_check(self):
        if int(self.file_size)>0 and '.tmp':
            return True
        else:
            return False
    @property
    def path(self):
        return self._path

    @path.setter
    def path(self,a):
        self._path=a

    def __repr__(self) -> str:
        return f"{self.file_name}"

 
def startFTP(host,port,user,password):
    ftp = FTP()
    port=port
    #TODO: Get user and password from secret encrypted file
    ftp.connect(host,port)
    ftp.login(user,password)
    welcome = ftp.getwelcome()
    print(welcome)
    # file Handling searching 
    
    root_dir =["WhatsApp","Telegram"]
     
    def searchDir(path):
        content=[]
        def search(line):
            match=re.findall(r'\s*([\w\d.:-]*)\s*',line)
            file=[]
            for i in match:
                if i !="":
                    if len(file)==9:
                        if i in '-/+_.':
                            file[8]+=i
                        else:
                            file[8]+=f' {i}'
                    else:
                        file.append(i)
            #Content selection
            if file[8]==".nomedia" or ".chck" in file[8] or ".tmp" in file[8]:
                print("rejected",file)
            else:
                obj = FileObj(file)
                if type(path)== FileObj:
                    obj.path=f"{path.path}/{obj.file_name}"
                else:
                    obj.path=f"{path}/{obj.file_name}"
                content.append(obj)
                 
        ftp.retrlines("LIST",search)
        return content
    ## Implementing Breath-First-Search Algorithm
    Traverse = True
    tracker =0
    Allfiles =[]
    while Traverse:
        print(tracker)
        print(root_dir)
        found_dir = []
        for i in root_dir:
            if tracker==0:
                ftp.cwd(f'/{i}')
                content = searchDir(i)
                for j in content:
                    if j.is_file:
                        Allfiles.append(j)
                    else:
                        found_dir.append(j)
            else:
                print("path",i.path)
                ftp.cwd(f"/{i.path}")
                content = searchDir(i)
                for j in content:
                    if j.is_file:
                        Allfiles.append(j)
                    else:
                        found_dir.append(j)
        tracker+=1
        if len(found_dir)>1:
            Traverse=True
            root_dir=found_dir
        else:
            Traverse=False
    ## End of BSF
    def mediaSearch(Allfiles):
        mediaFiles={'videos':[],'music':[],'pictures':[]}
        for file in Allfiles: 
            if '.mp4' in file.file_name :
                mediaFiles["video"].append(file)
            elif '.mp3' in file.file_name:
                mediaFiles["music"].append(file)
            elif '.png' in file.file_name or '.jpg' in file.file_name or '.jpeg'in file.file_name:
                mediaFiles["pictures"].append(file)
        return mediaFiles
    
    ## TODO: test this function
    def localBackup():
        backup_root=""
        trackfile =open(os.path.join(backup_root,'.noname'),'wb+')
        trackobj = pickle.load(trackfile)
        backup_files = mediaSearch(Allfiles)
        print("Backup Beginning")
        bar = ChargingBar("Downloading")
        for cat in backup_files:
            for file in backup_files[cat]:
                if file.file_name not in trackobj:
                    with open(os.path.join(backup_root,cat,file.file_name),'wb') as f:
                        ftp.retrbinary(f'RETR {file.path}', f.write)
                        trackobj.append(file.file_name)
                bar.next()
        bar.finish()
        pickle.dump(trackobj,trackfile)
        trackfile.close()
                


## TODO: CloudBackup