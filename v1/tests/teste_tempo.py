import time

last_time = 0

while True:

    init = time.time()

    if init - last_time > 1:
        
        print(".")
        last_time = init