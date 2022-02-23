import time
import glob
from multiprocessing import Process
from aws_service import upload_file
import boto3
import os 
import telegram_send


class Manager:
    def __init__(self):
        self.services_list = list()
        self.process_upload_list = list()
        try:
            #telegram_send.send(messages=["Serviço de captura iniciado!"])
            print("random") # instrucao para manter a estrutura try + except
        except:
            print("erro ao enviar mensagem ao telegram")
            
    def check_video_to_upload(self):
        list_of_videos_to_upload = glob.glob("*.avi")
        print("videos para upload: ")
        for video_to_upload in list_of_videos_to_upload:
            print("fazendo upload: {}".format(video_to_upload))
            if(video_to_upload.split("_")[0] == "loading"):
                # print("video ainda carregando")
                pass
            else:
                video_uploaded = True
                try:
                    print("video do up ", video_to_upload)
                    size = os.path.getsize(video_to_upload)
                    #if size > 30000:
                    if size > 30000:
                        upload_file(video_to_upload, "input-bucket-roda", "ia_samples")
                        print("video enviado")
                    else:
                        print("excluir video")
                except Exception as e:
                    print("não consegui guardar o video")
                    print(e)
                    video_uploaded = False

                if video_uploaded:
                    #telegram_send.send(messages=["Video carregado na aws - {}".format(video_to_upload.split("_"))])
                    os.remove(video_to_upload)

if __name__ == "__main__":
    manager = Manager()
    #telegram_send.send(messages=["Iniciando o servico de upload"])
    while True:
        manager.check_video_to_upload()
        time.sleep(5)