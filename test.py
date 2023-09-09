import cv2
import utils
from gesture_detector import GestureDetector

gesture_status = {
    "Left Fist": False, 
    "Right Fist": False,
    "Left Thumb": False,
    "Right Thumb": False,
    "Angle": 0  
}
def show_gesture_status(img, gesture_status):

    font = cv2.FONT_HERSHEY_PLAIN
  
    cv2.putText(img, "Left Fist: " + str(gesture_status["Left Fist"]), 
    (10, 20), font, 1, (0,255,0), 2)

    cv2.putText(img, "Right Fist: " + str(gesture_status["Right Fist"]),
    (10, 50), font, 1, (0,255,0), 2)   

    cv2.putText(img, "Left Thumb: " + str(gesture_status["Left Thumb"]), 
    (10, 70), font, 1, (0,255,0), 2)

    cv2.putText(img, "Right Thumb: " + str(gesture_status["Right Thumb"]),
    (10, 90), font, 1, (0,255,0), 2) 
    cv2.putText(img, "Angle: " + str(gesture_status["Angle"]), 
    (10, 110), font, 1, (0,255,0), 2)

def main():
    cap = cv2.VideoCapture(0)
    detecor = GestureDetector()
    while True:
        success, img = cap.read()
        img= cv2.flip(img,1)

        img = detecor.findHands(img)
        detecor.findPosition(img)
        
        gesture_status = utils.update_gesture_status_low(detecor)
        # print(gesture_status)
        # signal(gesture_status)
        show_gesture_status(img, gesture_status)
        cv2.imshow('img',img)
        cv2.waitKey(0)


if __name__ == "__main__":
    main()