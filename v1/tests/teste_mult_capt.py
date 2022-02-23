import cv2
import numpy as np
import time
import RPi.GPIO as gpio
from datetime import datetime


gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
#gpio.setup(14, gpio.IN, pull_up_down = gpio.PUD_UP)
gpio.setup(14, gpio.IN, pull_up_down = gpio.PUD_DOWN)

alreadyPressed = False
Pressing = False
closedFiles = False
openedCaptures = False

class CameraMan():
	def __init__(self, camera):

		self.camera = camera
		self.cap = None
		self.out = None
		self.frame = None
		self.ready = None
		self.loop_interval = 0.1
		# aparentemente esta e a melhor e mais simples forma de calibrar a captacao em si

	def start_recorder(self):

		self.cap = cv2.VideoCapture(self.camera)
		self.fps = 1.0
		self.cap.set(cv2.CAP_PROP_FPS, self.fps) 
		# self.cap.set(cv2.CAP_PROP_FPS, self.fps): quanto mais diminuir os frames, mais a camera vai conseguir gravar, mas os videos parecerao saltados.
		# na hora de reproduzir a variacao de posicao vai ser brusca ja que foram captados poucos frames
		self.buffersize = 1
		self.cap.set(cv2.CAP_PROP_BUFFERSIZE, self.buffersize) # de 1 a 10
		# self.fps = self.cap.get(cv2.CAP_PROP_FPS)
		# self.buffer = self.cap.get(cv2.CAP_PROP_BUFFERSIZE)
		# print("fps: ", self.fps, "buffer", self.buffer)
		# aparentemente a camera nao apresenta timeout ate o buffer ser preenchido. 
		# Depois que e preenchido, apresenta timeout constantemente

		self.fpswriter = 1.0 
		# nao sei o que esse parametro faz. Ele nao e igual a self.fps
		# Quantos frames por segundo escreve no arquivo?

		frame_width = int(self.cap.get(3)) # 640
		#print("frame_width: ", frame_width, type(frame_width))
		frame_height = int(self.cap.get(4)) # 480
		#print("frame_width: ", frame_height, type(frame_height))

		self.video_name = "vid_cam_" + str(self.camera) + "_fps_" + str(self.fps) + "_buffersize_" + str(self.buffersize) + "_fpswriter_" + str(self.fpswriter) + "_lp_" + str(self.loop_interval) + ".avi"
		#self.video_name = "vid_cam_" + str(self.camera) + datetime.now().strftime("_%d-%m-%Y_%H-%M-%S") + ".avi"
		
		self.out = cv2.VideoWriter(self.video_name, cv2.VideoWriter_fourcc('M','J','P','G'), self.fpswriter, (frame_width, frame_height)) 
		#self.out = cv2.VideoWriter(self.video_name, cv2.VideoWriter_fourcc(*'mp4v'), 23.0, (640, 480))


		print("CONFIGURADA: ", self.camera)

	def grab_frame(self):
		self.ready = self.cap.grab() # pegar um frame

		if (self.ready):
			print("grab " + str(self.camera) + ": OK!")

		return self.ready

	def retrieve_frame(self):
		if (self.ready):
			ret, self.frame = self.cap.retrieve() # retirar um frame para depois grava-lo

			if (ret):
				print("ret " + str(self.camera) + ": OK!", type(self.frame), np.shape(self.frame))
			else:
				print("ret EMPTY")
		
		return self.frame

	def write_frame(self):

		#self.frame = cv2.rotate(self.frame, cv2.ROTATE_180)
		self.out.write(self.frame)
		print("gravando em " + str(self.camera))

	def stop_record(self):

		self.cap.release()
		self.out.release()

		print("TERMINOU: ", str(self.camera))


if __name__ == "__main__":

	CAM_INDEX_0 = 0 # web fisheye
	CAM_INDEX_1 = 1 # cam LOGI
	CAM_INDEX_2 = 2 # cam azul

	lista_cameras = [
		CameraMan(CAM_INDEX_0),
		CameraMan(CAM_INDEX_2)
	]

	# para capturar frames em cada camera e exibir necessita de cv2.CAP_DSHOW (por ex.: streaming local). Nao sei explicar porque!

	while (True):

		if (gpio.input(14) == 1):
			Pressing = True
			closedFiles = False

			if (not openedCaptures):
				for cam in lista_cameras:
					cam.start_recorder() # CONFIGURADA
				openedCaptures = True
			
			for cam in lista_cameras:
				cam.grab_frame() # grab OK

			for cam in lista_cameras:
				cam.retrieve_frame() # ret OK

			for cam in lista_cameras:
				cam.write_frame() # gravando 

		elif (not gpio.input(14) and Pressing):
			alreadyPressed = True
			Pressing = False

		if (alreadyPressed and not Pressing):
			if (not closedFiles):
				for cam in lista_cameras:
					cam.stop_record() # TERMINOU

				#cv2.destroyAllWindows()
				openedCaptures = False
				alreadyPressed = False
				closedFiles = True
		
		time.sleep(CameraMan(CAM_INDEX_0).loop_interval) # ou time.sleep(CameraMan(CAM_INDEX_2).loop_interval)