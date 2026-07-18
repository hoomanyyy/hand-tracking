import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import cv2
import time
import mouse

model_path = './hand_landmarker.task'

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

    # Create a gesture recognizer instance with the video mode:
options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path='gesture_recognizer.task'),
    running_mode=VisionRunningMode.VIDEO
)

recognizer = GestureRecognizer.create_from_options(options)

mp_hands = mp.tasks.vision.HandLandmarksConnections
mp_drawing = mp.tasks.vision.drawing_utils
mp_drawing_styles = mp.tasks.vision.drawing_styles

MARGIN = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54)

def draw_landmarks_on_image(rgb_image, detection_result):
  hand_landmarks_list = detection_result.hand_landmarks
  handedness_list = detection_result.handedness
  annotated_image = np.copy(rgb_image)

  for idx in range(len(hand_landmarks_list)):
    hand_landmarks = hand_landmarks_list[idx]
    handedness = handedness_list[idx]

    mp_drawing.draw_landmarks(
      annotated_image,
      hand_landmarks,
      mp_hands.HAND_CONNECTIONS,
      mp_drawing_styles.get_default_hand_landmarks_style(),
      mp_drawing_styles.get_default_hand_connections_style())

    height, width, _ = annotated_image.shape
    x_coordinates = [landmark.x for landmark in hand_landmarks]
    y_coordinates = [landmark.y for landmark in hand_landmarks]
    text_x = int(min(x_coordinates) * width)
    text_y = int(min(y_coordinates) * height) - MARGIN

    cv2.putText(annotated_image, f"{handedness[0].category_name}",
                (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX,
                FONT_SIZE, HANDEDNESS_TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)

  return annotated_image

cam = cv2.VideoCapture(0)

frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))


while True:
    ret, frame = cam.read()


    rgb_frame = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)

    image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    timestamp = int(time.time() * 1000)
    result = recognizer.recognize_for_video(image, timestamp)
    
    screen_w = 1920
    screen_h = 1080

    if result.gestures:
        print(result.gestures[0][0].category_name)
        gesture = result.gestures[0][0].category_name

        if gesture == "Closed_Fist":
           print("close hand")
           mouse.click("left")
        
        if gesture == "Open_Palm":
           hand = result.hand_landmarks[0]

           x = hand[0].x
           y = hand[0].y

           mouse_x = int(x * screen_w)
           mouse_y = int(y * screen_h)

           mouse.move(mouse_x , mouse_y , absolute=True)
        
        if gesture == "Pointing_Up":
           mouse.scroll(-5)

            
    output_image = draw_landmarks_on_image(rgb_frame , result)

    cv2.imshow('Camera', output_image)

<<<<<<< HEAD
    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
out.release()
cv2.destroyAllWindows()
=======
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
                        
                        clicked = True
                        pyautogui.click()

                else:
                    clicked == False

    cv2.imshow("camera", frame)


    if cv2.waitKey(1) == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
>>>>>>> a150409b4c1c4624f012f0351547d6931c59d873
