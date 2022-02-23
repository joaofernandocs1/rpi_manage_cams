import multiprocessing
import time
import RPi.GPIO as gpio
import cv2 
from datetime import datetime
from aws_service import upload_file
import telegram_send
import os

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
# gpio.setup(14, gpio.IN, pull_up_down = gpio.PUD_UP)
gpio.setup(14, gpio.IN, pull_up_down=gpio.PUD_DOWN)

justOpenedDoor = False
justClosedDoor = True


class CameraMan():
	def __init__(self, camera):

		self.camera = camera
		self.cap = None
		self.out = None
		self.frame = None
		self.error_before = False 
		self.name = "ia"
		self.video_name_load = "loading_" + self.name + datetime.now().strftime("_%d-%m-%Y_%H-%M-%S") + '.avi'
		self.video_name = self.name + datetime.now().strftime("_%d-%m-%Y_%H-%M-%S") + '.avi'
		self.cap = cv2.VideoCapture(self.camera)
		self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
		#telegram_send.send(messages=["Iniciando o servico de gravacao"])

	def start_recorder(self):

		#print("CONFIGURADA: ", self.camera)
		self.video_name_load = "loading_" + self.name + datetime.now().strftime("_%d-%m-%Y_%H-%M-%S") + '.avi'
		self.video_name = self.name + datetime.now().strftime("_%d-%m-%Y_%H-%M-%S") + '.avi'
		#self.cap = cv2.VideoCapture(self.camera)
		#self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

		frame_width = int(self.cap.get(3))
		frame_height = int(self.cap.get(4))
		
		self.out = cv2.VideoWriter(self.video_name_load, cv2.VideoWriter_fourcc('M','J','P','G'), 3, (frame_width,frame_height))
		
		print("CONFIGURADA: ", self.camera)

	def record_frame(self):

		if self.cap != None:
			try: 
				ret, frame = self.cap.read() 
				self.out.write(self.frame) # escreve o frame no arquivo de saida de video previamente configurado
				print("+1 FRAME EM: ", self.camera)
				self.error_before = False
			except cv2.error as error:
				if not self.error_before:
					self.error_before = True
					print("1o erro de leitura no opencv")
				elif (self.error_before):
					print("erro novamente de leitura no opencv")

	def stop_recorder(self):

		#print("TERMINOU: ", self.camera)
		os.rename(r'{}'.format(self.video_name_load),r'{}'.format(self.video_name))
        #telegram_send.send(messages=["Novo video gravado"])
		self.cap.release()
		self.out.release()

		print("TERMINOU: ", self.camera)


if __name__ == '__main__':

	lista_processos = []
	lista_cameras = [
		CameraMan(0),
		#CameraMan(2)
	]

	while True:

		if (gpio.input(14) == 1):  # Porta aberta

			justClosedDoor = False # porta nao esta fechada
			justOpenedDoor = True # porta esta aberta

			if justOpenedDoor:

				print("porta aberta e gravacoes: ", len(lista_processos))
                
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

		elif (gpio.input(14) == 0):
			
			justOpenedDoor = False # porta nao esta aberta
			
			if not justClosedDoor:
			
				justClosedDoor = True # a porta esta fechada

				if (len(lista_processos) > 0):

					print("porta fechada e gravacoes: ", len(lista_processos))

					for lc in lista_cameras: # termina as gravacoes das cameras e esvazia lista de gravacoes

						#lista_processos[index].terminate()
						lc.stop_recorder()
						
					lista_processos = []
		#time.sleep(1)