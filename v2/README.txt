1)  as alterações nos códigos estão sendo feitas pensando em realizar testes apenas com cameras locais conectadas via usb

    por exp.: camera_watcher.py

    21 #cap = cv2.VideoCapture(0)
    22 cap = cv2.VideoCapture(int(camera_ip))

    em tese, funcionará para cameras locais, desde que descritas em mac.txt