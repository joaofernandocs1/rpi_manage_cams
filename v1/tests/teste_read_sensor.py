import RPi.GPIO as gpio
import time
from multiprocessing import Process
import cv2 
from datetime import datetime
#from aws_service import upload_file
#import telegram_send
import os

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
#gpio.setup(14, gpio.IN, pull_up_down = gpio.PUD_UP)
gpio.setup(14, gpio.IN, pull_up_down = gpio.PUD_DOWN)
justOpenedDoor = True
justClosedDoor = False
initialLoop = True
last_time = 0

class Recoder:
	def __init__(self, camera):
		self.camera = camera
		self.cap = None
		self.out = None
		self.error_before = False 
		self.name = "ia"
		self.video_name_load = "loading_" + self.name + datetime.now().strftime("_%d-%m-%Y_%H-%M-%S") + '.avi'
		self.video_name = self.name + datetime.now().strftime("_%d-%m-%Y_%H-%M-%S") + '.avi'
		#telegram_send.send(messages=["Iniciando o servico de gravacao"])

	def start_recorder(self):
		print("CONFIGURADO")
		self.video_name_load = "loading_" + self.name + datetime.now().strftime("_%d-%m-%Y_%H-%M-%S") + '.avi'
		self.video_name = self.name + datetime.now().strftime("_%d-%m-%Y_%H-%M-%S") + '.avi'
		self.cap = cv2.VideoCapture(self.camera)
		self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

		frame_width = int(self.cap.get(3))
		frame_height = int(self.cap.get(4))
		
		self.out = cv2.VideoWriter(self.video_name_load, cv2.VideoWriter_fourcc('M','J','P','G'), 23, (frame_width,frame_height))


	def record_frame(self):
		print("GRAVANDO")
		if self.cap != None:
			try: 
				ret, frame = self.cap.read() 
				self.out.write(frame)
				print("+1 frame")
				self.error_before = False
			except cv2.error as error:
				if not self.error_before:
					# Enviar para a AWS
					self.error_before = True
					print("erro de leitura no opencv")

	def stop_recoder(self):
		print("TERMINOU")
		os.rename(r'{}'.format(self.video_name_load),r'{}'.format(self.video_name))
		#telegram_send.send(messages=["Novo video gravado"])
		self.cap.release()
		self.out.release()

if __name__ == '__main__':

	lista_processos = []
	lista_cameras = [
		Recoder(0),
		#Recoder(2)
	]

	while True:

		'''init = time.time()

		if init - last_time > 5:

			#os.system('python3 manager_camera_videos.py')
			print(".")
			last_time = init'''

		if(gpio.input(14) == 1): # Porta aberta
			justClosedDoor = False #reseto a variável

			for lc in lista_cameras:
						
				#process.start()
				#process.terminate()

				lc.record_frame()

			if justOpenedDoor:
				print("porta aberta")

				if (len(lista_processos) == 0):

					for lc in lista_cameras: # preenche a lista de instancias, inicia elas e grava o 1o frame
						lc.start_recorder()
						#time.sleep(1)

						#process = multiprocessing.Process(target=lc.record_frame)
						#lista_processos.append(process)
						lista_processos.append(lc.record_frame)
						
						'''if not (process.is_alive()):

							process.start()
							process.terminate()'''

						lc.record_frame()

				elif (len(lista_processos) > 0): # caso ja tenham sido instanciadas, segue gravando frames

					for lc in lista_cameras:
						
						#process.start()
						#process.terminate()

						lc.record_frame()

				justOpenedDoor = False
				if not initialLoop:
					print("1o loop")
		else:
			justOpenedDoor = True #reseto a variável
			if not justClosedDoor:
				justClosedDoor = True
				if not initialLoop:

					if (len(lista_processos) > 0):

						print("porta fechada e gravacoes: ", len(lista_processos))

						for lc in lista_cameras: # termina as gravacoes das cameras e esvazia lista de gravacoes

							#lista_processos[index].terminate()
							lc.stop_recoder()
							
						lista_processos = []

		initialLoop = False
		# time.sleep(1)

	gpio.cleanup()
	exit()