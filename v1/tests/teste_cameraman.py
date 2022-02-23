import multiprocessing
import time
import RPi.GPIO as gpio
from threading import Thread

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
# gpio.setup(14, gpio.IN, pull_up_down = gpio.PUD_UP)
gpio.setup(14, gpio.IN, pull_up_down=gpio.PUD_DOWN)

justOpenedDoor = True
justClosedDoor = False
initialLoop = True


class CameraMan():
	def __init__(self, camera):

		self.isAlive = False
		self.camera = camera

	def start_recorder(self):

		print("CONFIGURADO")

	def record_frame(self):

		while True:

			print("+1 FRAME EM: ", self.camera)
			time.sleep(0.5)

	def stop_recorder(self):

		print("TERMINOU")


if __name__ == '__main__':

	lista_processos = []
	lista_cameras = [
		CameraMan(0),
		CameraMan(2)
	]

	while True:

		if (gpio.input(14) == 1):  # Porta aberta
			justClosedDoor = False  # reseto a variável
			if justOpenedDoor:
				
				print("porta aberta")
                
				if (len(lista_processos) == 0):

					for lc in lista_cameras:

						lc.start_recorder()

						process = multiprocessing.Process(target=lc.record_frame)
						lista_processos.append(process)
						
						process.start()

				justOpenedDoor = False
				
				if not initialLoop:
					
					print("1o loop")

		else:
			
			justOpenedDoor = True #reseto a variável
			
			if not justClosedDoor:
			
				justClosedDoor = True
				
				if not initialLoop:

					for index, lc in enumerate(lista_cameras):

						lc.stop_recorder()
						lista_processos[index].kill()
						
					lista_processos = []
		
		initialLoop = False