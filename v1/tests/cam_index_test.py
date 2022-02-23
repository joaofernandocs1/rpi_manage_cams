import cv2

'''while True:
	ret, image = cam.read()
	cv2.imshow('Imagetest',image)
	k = cv2.waitKey(1)
	if k != -1:
		break'''

CAM_INDEX_0 = 0 # webcam integrada
CAM_INDEX_1 = 1 # cam LOGI (demora muito para responder)
CAM_INDEX_2 = 2 # cam azul

try:
    cam_0 = cv2.VideoCapture(CAM_INDEX_0) # -1 detecta automaticamente, mas detecta qualquer coisa.

    ret_0, image_0 = cam_0.read(CAM_INDEX_0)
    cv2.imwrite('testimage_0.jpg', image_0)

    cam_0.release()
except Exception as error_0:
    print("Erro 0: ", error_0)

try:
    cam_1 = cv2.VideoCapture(CAM_INDEX_1) # -1 detecta automaticamente, mas detecta qualquer coisa.

    ret_1, image_1 = cam_1.read(CAM_INDEX_1)
    cv2.imwrite('testimage_1.jpg', image_1)

    cam_1.release()
except Exception as error_1:
    print("Erro 1: ", error_1)

try:
    cam_2 = cv2.VideoCapture(CAM_INDEX_2) # -1 detecta automaticamente, mas detecta qualquer coisa.

    ret_2, image_2 = cam_2.read(CAM_INDEX_2)
    cv2.imwrite('testimage_2.jpg', image_2)

    cam_2.release()
except Exception as error_2:
    print("Erro 2: ", error_2)


# sudo apt-get install v4l-utils
# v4l2-ctl --list-devices
# exp.: "/dev/video1" -> index == 1