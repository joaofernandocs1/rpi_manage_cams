import threading
import socket 
import time 
from multiprocessing import Process, Pool 
import cv2 
from datetime import datetime
import imutils
import os 
import logging 
import math 

def camera_watcher(camera_ip, user_id, port_number, suffix_data, name, resolution_type, frame_rate):
    # cam_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # cam_socket.connect((socket_server_ip, socket_server_port))
    #logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')
    #logging.info("connecting to camera from {}".format(camera_ip))
    # logging.info("frame rate: ", frame_rate)
    frame_rate = int(int(frame_rate)/2)
    if(camera_ip == "0" or camera_ip):
        logging.info("camera local inciada")
        #cap = cv2.VideoCapture(0)
        cap = cv2.VideoCapture(camera_ip)
    # elif(user_id == None):
    elif(type(camera_ip) != type(1) and user_id == None):
        cap = cv2.VideoCapture('rtsp://{}:{}{}'.format(camera_ip, port_number, suffix_data))
    # else:
    elif(type(camera_ip) != type(1)):
        cap = cv2.VideoCapture("rtsp://admin:{}@{}:{}{}".format(user_id, camera_ip, port_number, suffix_data))
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_rate)
    
    if(resolution_type == "fullhd"):
        size = (1920, 1080)
    elif(resolution_type == "hd"):
        size = (1280, 720)
    elif(resolution_type == "vga"):
        size = (854, 480)
    else:
        # print("resolução padrão da camera")
        size = (int(cap.get(3)), int(cap.get(4)))
        
    while True:
        i = 0
        logging.info("inciando o loop")
        # video_name_load = "loading_" + name + datetime.now().strftime("_%d-%m-%Y_%H-%M-%S") + '.mp4'
        video_name_load = "loading_" + name + datetime.now().strftime("_%d-%m-%Y_%H-%M-%S") + '.avi'
        # video_name = name + datetime.now().strftime("_%d-%m-%Y_%H-%M-%S") + '.mp4'
        video_name = name + datetime.now().strftime("_%d-%m-%Y_%H-%M-%S") + '.avi'
        # fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
        my_video = cv2.VideoWriter(video_name_load, (fourcc), frame_rate, size)
        total_seconds = 60*60
        max_frames = total_seconds*frame_rate
        logging.info("dados settados")
        init = datetime.now()
        last = datetime.now()
        # all_frames = list()
        # all_times = list()
        while i <= max_frames:
            # TODO: check if there is any command to camera
            now = datetime.now()
            if((now - init).seconds >= total_seconds):
                logging.info("bateu o tempo")
                break
            _, frame = cap.read()
            # all_times.append(datetime.now())
            # all_frames.append(frame)
            if(i%2 == 0):
                frame = imutils.resize(frame, width=size[0])
                fontface = cv2.FONT_HERSHEY_SIMPLEX
                fontscale = 1
                fontcolor = (255, 255, 255)
                cv2.putText(frame, str(now), (40,40), fontface, fontscale, fontcolor) 
                my_video.write(frame)
                print("+1 frame: ", camera_ip)
            i+=1

        # fps = len(all_frames)/((all_times[-1]-all_times[0]).seconds)
        # print("fps: ", fps)
        logging.info("quase pronto pra upload")
        my_video.release()
        os.rename(r'{}'.format(video_name_load),r'{}'.format(video_name))
        logging.info("tornando o video pronto para upload {}".format(video_name))
    cap.release()
    # cam_socket.sendall(b"saved video")
    # print("thread loop ", cam_socket.recv(1024))
