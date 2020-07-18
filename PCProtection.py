import cv2

from pynput import keyboard


clicks_to_take_picture = 3
current_clicks = 0


def take_picture():
    cam = cv2.VideoCapture(0)
    #cv2.namedWindow("test")
    ret, frame = cam.read()
    cv2.imshow("test", frame)
    img_name = "criminal.png"
    cv2.imwrite(img_name, frame)
    cam.release()
    cv2.destroyAllWindows()


def on_press(key):
    global clicks_to_take_picture
    global current_clicks

    print('Key {} pressed.'.format(key))
    current_clicks += 1

    if current_clicks == clicks_to_take_picture:
        take_picture()
        return False


with keyboard.Listener(
        on_press=on_press) as listener:

    listener.join()
