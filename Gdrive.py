from __future__ import print_function
import mimetypes
from turtle import up
import re
import logging 

from Google import *
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import os 


backup_root ='C:\\Users\\vemma\\Backup'
backuplog = logging.basicConfig(os.path.join(backup_root,'log.txt'),level=logging.INFO,format="%(asctime)s %(message)s")
 
## Note: This is kind of redundant, because of @mediaSearch function
def get_mimetype(file):
        ext = re.findall(r'\.(\w+)',file)
        ext = ext[0].lower()
        if ext in ['jpeg','jpg','png','gif'] :
            return f'image/{ext}'
        elif ext in ['webm','mkv','mp4','avi' ]:
            return f'video/{ext}'
        elif ext in ['mp3']:
            return f'audio/{ext}'
 
def upload_basic(inputfile,cat,cwd):
    parent_dir={
        'music':'1raJBhOYt3_knUKmPVt8k9mOV5iNpuNTa',
        'video':'178xH2Zw7y8RXNbXZCE6gHQkehGmVZ9p3',
        'pictures':'1jBxut-TeHZ1i0jaKYBJ8SdQLJn6N0e_O'
    }
    
    try:
        service = create_service_from_account('credentials.json')
        file_metadata = {'name': inputfile, 'parents':[parent_dir[cat]]}
        media = MediaFileUpload(os.path.join(cwd,inputfile),
                                mimetype=get_mimetype(inputfile))

        file = service.files().create(body=file_metadata, media_body=media,
                                      fields='id').execute()


    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

## ALGO 
# Go into backup folder
# get all categories file 
# go into the categories folder
    # Upload each file to category in cloud 
    # Delete once uploaded
# Close 
def backup():
    os.chroot(backup_root)
    subfolders = os.listdir()
    size =0
    for sub in subfolders:
        os.chdir(sub)
        cwd = os.getcwd()
        files = os.listdir()
        for file in files:
            size+= os.stat(file).st_size
            #TODO: Add a progress bar
            # os.remove(file)
            upload_basic(file,sub,cwd)
    backuplog.info(f'Message: Backup Completed  Size:{size} bytes')


 
