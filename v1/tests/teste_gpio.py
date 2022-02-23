import RPi.GPIO as gpio

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(14, gpio.IN, pull_up_down = gpio.PUD_DOWN)

porta_aberta = False

while True:

    if (gpio.input(14) == 1):

        print("HIGH")

    else:

        print("LOW")