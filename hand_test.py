import mediapipe as mp
from mediapipe.tasks.python import vision
import cv2
import time
import pyautogui


# Gesture Recognizer
BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
RunningMode = mp.tasks.vision.RunningMode


options = GestureRecognizerOptions(
    base_options=BaseOptions(
        model_asset_path="gesture_recognizer.task"
    ),
    running_mode=RunningMode.VIDEO
)

recognizer = GestureRecognizer.create_from_options(options)


# Drawing
mp_hands = mp.tasks.vision.HandLandmarksConnections
mp_drawing = mp.tasks.vision.drawing_utils
mp_styles = mp.tasks.vision.drawing_styles



def draw_landmarks(image, result):

    output = image.copy()

    for hand in result.hand_landmarks:
        mp_drawing.draw_landmarks(
            output,
            hand,
            mp_hands.HAND_CONNECTIONS,
            mp_styles.get_default_hand_landmarks_style(),
            mp_styles.get_default_hand_connections_style()
        )

    return output



screen_w, screen_h = pyautogui.size()


cam = cv2.VideoCapture(0)


clicked = False
scrolling = False


while True:

    ret, frame = cam.read()

    if not ret:
        break


    # بدون flip -> تصویر آینه‌ای نمی‌شود
    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


    image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )


    timestamp = int(time.time() * 1000)


    result = recognizer.recognize_for_video(
        image,
        timestamp
    )


    if result.gestures:

        gesture = result.gestures[0][0].category_name


        print(gesture)



        # ✊ کلیک
        if gesture == "Closed_Fist":

            if not clicked:

                pyautogui.click()
                clicked = True


        else:
            clicked = False



        # 🖐 حرکت موس
        if gesture == "Open_Palm":

            if result.hand_landmarks:

                hand = result.hand_landmarks[0]


                # مرکز کف دست
                x = hand[9].x
                y = hand[9].y


                mouse_x = int(x * screen_w)
                mouse_y = int(y * screen_h)


                pyautogui.moveTo(
                    mouse_x,
                    mouse_y,
                    duration=0.05
                )



        # ☝ اسکرول
        if gesture == "Pointing_Up":

            if not scrolling:

                pyautogui.scroll(-3)
                scrolling = True


        else:
            scrolling = False




    output = draw_landmarks(
        rgb,
        result
    )


    cv2.imshow(
        "Hand Control",
        cv2.cvtColor(
            output,
            cv2.COLOR_RGB2BGR
        )
    )


    if cv2.waitKey(1) == ord("q"):
        break



cam.release()
cv2.destroyAllWindows()
