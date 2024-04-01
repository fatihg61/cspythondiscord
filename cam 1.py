from PIL import ImageGrab
import cv2

def cam_photo():
    # Gebruik de cv2 bibliotheek om de webcam te activeren en een foto te maken
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    # Sla de foto op als 'tmp.png'
    cv2.imwrite('tmp.png', frame)

    # Stop de video-opname
    cap.release()
    cv2.destroyAllWindows()

def screen_shot():
    # Code voor het maken van een screenshot
    im = ImageGrab.grab()
    im.save('screenshot.png')
