import time
import glob
from camera_watcher import camera_watcher
from multiprocessing import Process
from aws_service import upload_file
from get_ip import get_my_ip
#import boto3
import os 
#import telegram_send

class Manager:
    def __init__(self):
        self.socket_server_ip = '127.0.0.1'
        self.socket_server_port = 65432
        self.services_list = list()
        self.process_upload_list = list()
        try:
            #telegram_send.send(messages=["Serviço de captura iniciado!"])
            print("Serviço de captura iniciado!")
        except:
            print("erro ao enviar mensagem ao telegram")
            
    def start_service(self, camera_config):
        # TODO: find ip from macaddress
        macaddress = camera_config.split(',')[0]
        user_id = camera_config.split(',')[1]
        port_number = camera_config.split(',')[2]
        suffix_data = camera_config.split(',')[3]
        fps = camera_config.split(',')[4]
        name = camera_config.split(',')[5]
        resolution = camera_config.split(',')[6]

        # if(macaddress == "E8:DB:84:3B:40:84"):
        #     camera_ip = "192.168.1.90"
        # elif(macaddress == "0" or macaddress == 0):
        #     camera_ip = "0"
        # else:
        #     camera_ip = "192.168.1.104"
        print("searching camera ip")
        # if(macaddress != "0" and macaddress):
        if(macaddress != "0" and macaddress != "1" and macaddress != "2" and macaddress):
            print("passando o macddress {}".format(macaddress))
            camera_ip = get_my_ip(macaddress)
        else:
            # camera_ip = "0"
            camera_ip = macaddress
            camera_ip = int(camera_ip)
            print("camera local {} esta a iniciar".format(camera_ip))
        if(camera_ip or camera_ip == "0"):
            print("achei: ", camera_ip)
            camera_watcher_process = Process(target=camera_watcher, args=(camera_ip, user_id, port_number, suffix_data, name, resolution, fps))
            service_info = {
                "service_macaddress": macaddress,
                "process": camera_watcher_process 
            }
            print("starting service")
            camera_watcher_process.start()
            print("service started")
            self.services_list.append(service_info)
    
    def start_all_services(self):
        list_of_mac = open('mac.txt', 'r')
        list_of_mac = list_of_mac.read().split('\n')
        for camera_config in list_of_mac:
            try:
                print("inicializando: ", camera_config.split(',')[0])
                self.start_service(camera_config)
            except:
                print("não foi possível inicializar o serviço: ", camera_config.split(',')[0])

    def kill_service(self, index):
        for service in self.services_list:
            service["process"].terminate()

    def check_new_services(self):
        list_of_mac = open('mac.txt', 'r').read().split('\n')
        print("checking if there is any service that should be initializated")
        for camera_config in list_of_mac:
            try:
                #print("inicializando: ", camera_config.split(',')[0])
                self.start_service(camera_config)
            except:
                print("não foi possível inicializar o serviço: ", camera_config.split(',')[0])

    def check_service_status(self):
        can_upload_video = True
        for index, upload_process in enumerate(self.process_upload_list):
            if upload_process.is_alive():
                #print("não posso fazer upload, já estou fazendo de 1 video")
                can_upload_video = False
                break
            else:
                # print("matando processo desligado {}".format(upload_process))
                self.process_upload_list.pop(index)
        if can_upload_video:
            # print("inciando processo de upload")
            save_video_process = Process(target=self.check_video_to_upload, args=())
            self.process_upload_list.append(save_video_process)
            save_video_process.start()

        for index, service in enumerate(self.services_list):
            #print("service index {} - ".format(index), service["process"].is_alive())
            if(not service["process"].is_alive()):
                self.services_list.pop(0)
                self.check_new_services()
        if(len(self.services_list) <= 0):
            print("Nenhum serviço conectado, reiniciar tudo")
            self.start_all_services()
    
    def check_video_to_upload(self):
        list_of_videos_to_upload = glob.glob("*.mp4")
        #print("videos para upload: ")
        for video_to_upload in list_of_videos_to_upload:
            # print("fazendo upload: {}".format(video_to_upload))
            if(video_to_upload.split("_")[0] == "loading"):
                # print("video ainda carregando")
                pass
            else:
                video_uploaded = True
                try:
                    upload_file(video_to_upload, "roda-watcher01", video_to_upload.split("_")[0])
                except Exception as e:
                    print("não consegui guardar o video")
                    print(e)
                    video_uploaded = False

                if video_uploaded:
                    #telegram_send.send(messages=["Video carregado na aws - {}".format(video_to_upload.split("_")[0])])
                    os.remove(video_to_upload)

if __name__ == "__main__":
    manager = Manager()
    manager.start_all_services()
    while True:
        manager.check_video_to_upload()
        manager.check_service_status()
        time.sleep(5)
