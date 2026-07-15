import cv2
import mediapipe as mp
import pyautogui
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


base_options = python.BaseOptions(
    model_asset_path="hand_landmarker.task"
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1
)

detector = vision.HandLandmarker.create_from_options(options)

print("Model loaded!")


cap = cv2.VideoCapture(0)

clicked = False

while True:

    ret, frame = cap.read()

    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )


    result = detector.detect(mp_image)


    if result.hand_landmarks:

        for hand in result.hand_landmarks:

            for i, point in enumerate(hand):

                h, w, _ = frame.shape

                x = int(point.x * w)
                y = int(point.y * h)

                print(
                    f"ID: {i} X:{x} Y:{y}"
                )

                cv2.circle(
                    frame,
                    (x, y),
                    5,
                    (0,255,0),
                    -1
                )

                if i == 8:

                    screen_width, screen_height = pyautogui.size()

                    mouse_x = int(point.x * screen_width)
                    mouse_y = int(point.y * screen_height)

                    pyautogui.moveTo(mouse_x, mouse_y)

                thumb = hand[4]
                index = hand[8]

                if abs(thumb.x - index.x) < 0.03 and abs(thumb.y -index.y) < 0.03:

                    if clicked == False:
                        
                        clicked == True
                        pyautogui.click()

                else:
                    clicked == False

    cv2.imshow("camera", frame)


    if cv2.waitKey(1) == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()