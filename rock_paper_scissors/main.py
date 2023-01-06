import cv2
import mediapipe as mp
import math


def chceckThatFingerIsStraight(hand_landmarks, a, b, c):
    x1, y1 = hand_landmarks.landmark[a].x, hand_landmarks.landmark[a].y
    x2, y2 = hand_landmarks.landmark[b].x, hand_landmarks.landmark[b].y
    x3, y3 = hand_landmarks.landmark[c].x, hand_landmarks.landmark[c].y

    ab = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    bc = math.sqrt((x2 - x3) ** 2 + (y2 - y3) ** 2)
    ac = math.sqrt((x3 - x1) ** 2 + (y3 - y1) ** 2)

    if ac < bc:
        return 0
    elif bc / ab > 1:
        return 1
    else:
        return bc / ab


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

# start hands recognition
with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    # open video
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue
        # recgnision on BGR color
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # check all open finger in cuurent frame
                # thumb = chceckThatFingerIsStraight(hand_landmarks, 0, 2, 4)
                index_finger = chceckThatFingerIsStraight(hand_landmarks, 0, 5, 8)
                middle_finger = chceckThatFingerIsStraight(hand_landmarks, 0, 9, 12)
                ring_finger = chceckThatFingerIsStraight(hand_landmarks, 0, 13, 16)
                little_finger = chceckThatFingerIsStraight(hand_landmarks, 0, 17, 20)

                # recognize the hand gesture
                text = ""
                if (index_finger < 0.6 and
                        middle_finger < 0.6 and
                        ring_finger < 0.6 and
                        little_finger < 0.6):
                    text = "Stone"
                elif (index_finger > 0.6 and
                      middle_finger > 0.6 and
                      ring_finger < 0.6 and
                      little_finger < 0.6):
                    text = "Scissors"
                elif (index_finger > 0.6 and
                      middle_finger > 0.6 and
                      ring_finger > 0.6 and
                      little_finger > 0.6 and
                      hand_landmarks.landmark[0].y > hand_landmarks.landmark[9].y):
                    text = "Paper"
                elif (index_finger > 0.6 and
                      middle_finger > 0.6 and
                      ring_finger > 0.6 and
                      little_finger < 0.6):
                    text = "Fire"
                elif (index_finger > 0.6 and
                      middle_finger > 0.6 and
                      ring_finger > 0.6 and
                      little_finger > 0.6 and
                      hand_landmarks.landmark[0].y < hand_landmarks.landmark[9].y):
                    text = "Wather"

                # draw hand gesture
                width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                position = (int(hand_landmarks.landmark[0].x * height), int(hand_landmarks.landmark[0].y * width))
                cv2.putText(image, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                # draw ahnd mask
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

        # Show frame
        cv2.imshow('Rock Paper Scissors Game', image)
        if cv2.waitKey(5) & 0xFF == 27:  # Esc
            break
cap.release()
