from Backup import *


if __name__=="__main__":
    mywifi="Vem"
    if scan_wifi(mywifi)[0]:
        if connect_to_wifi(mywifi)[0]:
            time.sleep(3)
            ## device has to sleep a while before ip is gotten
            device_ip=get_host_ip()
            startFTP(device_ip,2121,"test2","test")