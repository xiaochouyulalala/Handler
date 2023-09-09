import math
import mediapipe as mp

mp_hands = mp.solutions.hands
 

# def GestureRecognizer(img):
#     model_path = 'keras_model.h5'
#     BaseOptions = mp.tasks.BaseOptions
#     GestureRecognizer = mp.tasks.vision.GestureRecognizer
#     GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
#     VisionRunningMode = mp.tasks.vision.RunningMode


#     options = GestureRecognizerOptions(
#         base_options=BaseOptions(model_asset_path=model_path),
#         num_hands = 2,
#         running_mode=VisionRunningMode.IMAGE)

#     with GestureRecognizer.create_from_options(options) as recognizer:
#         recognition_result = recognizer.recognize(img)
#         return recognition_result

def calculateAngle(results):
    # 计算两个拳头的夹角

    handedness_list = results.multi_handedness 
    handedness = handedness_list[0]
    if(handedness=='Left'):
        left_fist = results.multi_hand_landmarks[0]
        right_fist = results.multi_hand_landmarks[1]
    else:
        left_fist = results.multi_hand_landmarks[1]
        right_fist = results.multi_hand_landmarks[0]

    x1, y1 = vector_from_landmarks(left_fist) 
    x2, y2 = vector_from_landmarks(right_fist)

    angle = math.atan((y1-y2)/(x1-x2))
    angle = math.degrees(angle)
    return angle


def vector_from_landmarks(landmarks):
    # 从手部关键点获取向量
    x = (landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x + landmarks.landmark[mp_hands.HandLandmark.WRIST].x)/2
    y = (landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y + landmarks.landmark[mp_hands.HandLandmark.WRIST].y)/2
    return x, y

def vector_2d_angle(v1,v2):

    v1_x=v1[0]
    v1_y=v1[1]
    v2_x=v2[0]
    v2_y=v2[1]
    try:
        angle_= math.degrees(math.acos((v1_x*v2_x+v1_y*v2_y)/(((v1_x**2+v1_y**2)**0.5)*((v2_x**2+v2_y**2)**0.5))))
    except:
        angle_ = 1234.
    if angle_ > 180.:
        angle_ = 1234.
    return angle_

def hand_angle(hand_):

    angle_list = []
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[2][0])),(int(hand_[0][1])-int(hand_[2][1]))),
        ((int(hand_[3][0])- int(hand_[4][0])),(int(hand_[3][1])- int(hand_[4][1])))
        )
    angle_list.append(angle_)
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])-int(hand_[6][0])),(int(hand_[0][1])- int(hand_[6][1]))),
        ((int(hand_[7][0])- int(hand_[8][0])),(int(hand_[7][1])- int(hand_[8][1])))
        )
    angle_list.append(angle_)
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[10][0])),(int(hand_[0][1])- int(hand_[10][1]))),
        ((int(hand_[11][0])- int(hand_[12][0])),(int(hand_[11][1])- int(hand_[12][1])))
        )
    angle_list.append(angle_)
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[14][0])),(int(hand_[0][1])- int(hand_[14][1]))),
        ((int(hand_[15][0])- int(hand_[16][0])),(int(hand_[15][1])- int(hand_[16][1])))
        )
    angle_list.append(angle_)
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[18][0])),(int(hand_[0][1])- int(hand_[18][1]))),
        ((int(hand_[19][0])- int(hand_[20][0])),(int(hand_[19][1])- int(hand_[20][1])))
        )
    angle_list.append(angle_)
    return angle_list

def check_fist(angle_list):
    thr_angle = 65.
    thr_angle_thumb = 53.

    if 1234. not in angle_list:
        if (angle_list[0]>thr_angle_thumb) and (angle_list[1]>thr_angle) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
            return True
    return False

def check_thumb(angle_list):
    thr_angle = 65.
    thr_angle_thumb = 25.
    if 1234. not in angle_list:
        if (angle_list[0]<thr_angle_thumb)  and (angle_list[1]>thr_angle) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
            return True
    return False

def update_gesture_status_low(detector):
    results = detector.results
    
    left_fist = False
    right_fist = False 
    left_thumb = False
    right_thumb = False
    angle = 0

    if results.multi_hand_landmarks:
        
        for idx,hand_landmarks in enumerate(results.multi_hand_landmarks):
            handedness = results.multi_handedness[idx].classification[0].label
            # print(handedness)
            hand_local = []
            for i in range(21):
                x = hand_landmarks.landmark[i].x*detector.y
                y = hand_landmarks.landmark[i].y*detector.x
                hand_local.append((x,y))
            if hand_local:
                angle_list = hand_angle(hand_local)
            if handedness == 'Right':
                right_fist = check_fist(angle_list)
                if(not right_fist):
                    right_thumb = check_thumb(angle_list)
            
            elif handedness == 'Left':
                left_fist = check_fist(angle_list)
                if(not left_fist):
                    left_thumb = check_thumb(angle_list)

    if ((left_fist == False) + (right_fist == False) + (left_thumb == False) + (right_thumb == False) < 3):
        angle = calculateAngle(results)
    return {
            "Left Fist": left_fist, 
            "Right Fist": right_fist,
            "Left Thumb": left_thumb,
            "Right Thumb": right_thumb,
            "Angle": angle 
            }

# 方案2
# def update_gesture_status(img):

#     left_fist = False
#     right_fist = False
#     left_thumb = False
#     right_thumb = False
#     angle = 0

#     results = GestureRecognizer(img)
#     hand_landmarks_list = results.hand_landmarks
#     handedness_list = results.handedness
#     gestures_list = results.gestures
#     for idx in range(len(hand_landmarks_list)):
#         # hand_landmarks = hand_landmarks_list[idx]
#         handedness = handedness_list[idx].category_name
#         gestures = gestures_list[idx].category_name
#         if(handedness=='Left' and gestures == 'fist'):
#             left_fist = True
#         elif(handedness=='Left' and gestures == 'thumb'):
#             left_thumb = True
#         elif(handedness=='Right' and gestures == 'fist'):
#             right_fist = True
#         elif(handedness=='Right' and gestures == 'thumb'):
#             right_thumb = True
    

#     if ((left_fist == False) + (right_fist == False) + (left_thumb == False) + (right_thumb == False) < 3):
#         angle = calculateAngle(results)
#     return {
#             "Left Fist": left_fist, 
#             "Right Fist": right_fist,
#             "Left Thumb": left_thumb,
#             "Right Thumb": right_thumb,
#             "Angle": angle 
#             }
