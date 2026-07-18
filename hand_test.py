import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import time
import mouse
import pyautogui


BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode


options = GestureRecognizerOptions(
    base_options=BaseOptions(
        model_asset_path="gesture_recognizer.task"
    ),
    running_mode=VisionRunningMode.VIDEO
)

recognizer = GestureRecognizer.create_from_options(options)


mp_hands = mp.tasks.vision.HandLandmarksConnections
mp_drawing = mp.tasks.vision.drawing_utils
mp_drawing_styles = mp.tasks.vision.drawing_styles


def draw_landmarks(rgb_image, result):

    image = rgb_image.copy()

    for hand in result.hand_landmarks:

        mp_drawing.draw_landmarks(
            image,
            hand,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style()
        )

    return image



# اندازه صفحه
screen_w, screen_h = pyautogui.size()


cam = cv2.VideoCapture(0)


while True:

    ret, frame = cam.read()

    if not ret:
        break


    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


    image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )


    timestamp = int(time.time() * 1000)

    result = recognizer.recognize_for_video(
        image,
        timestamp
    )


    if result.gestures:

        gesture = result.gestures[0][0].category_name

        print(gesture)


        # مشت = کلیک
        if gesture == "Closed_Fist":

            mouse.click(button="left")
            time.sleep(1)


        # کف دست = حرکت موس
        elif gesture == "Open_Palm":

            if result.hand_landmarks:

                hand = result.hand_landmarks[0]


                # مرکز کف دست
                x = hand[9].x
                y = hand[9].y


                mouse_x = int(x * screen_w)
                mouse_y = int(y * screen_h)


                mouse.move(
                    mouse_x,
                    mouse_y,
                    absolute=True
                )


        # اشاره = اسکرول
        elif gesture == "Pointing_Up":

            mouse.scroll(-3)
            time.sleep(0.5)



    output = draw_landmarks(
        rgb_frame,
        result
    )


    cv2.imshow(
        "Hand Mouse",
        cv2.cvtColor(output, cv2.COLOR_RGB2BGR)
    )


    if cv2.waitKey(1) == ord("q"):
        break



cam.release()
cv2.destroyAllWindows()
