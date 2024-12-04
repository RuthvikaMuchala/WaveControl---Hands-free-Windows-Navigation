import cv2
from math import hypot
import pyautogui
import numpy as np


def move_pointer(mpHands, hands, Draw):
    # Start capturing video from webcam
    cap = cv2.VideoCapture(0)

    # Get screen width and height
    screen_width, screen_height = pyautogui.size()

    # Start capturing video from webcam
    while True:
        # Read video frame by frame
        _, frame = cap.read()

        # Flip image
        frame = cv2.flip(frame, 1)

        # Convert BGR image to RGB image
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the RGB image
        Process = hands.process(frameRGB)

        landmarkList = []
        # If hands are present in image(frame)
        if Process.multi_hand_landmarks:
            # Detect hand landmarks
            for handlm in Process.multi_hand_landmarks:
                for _id, landmarks in enumerate(handlm.landmark):
                    # Store height and width of image
                    height, width, color_channels = frame.shape

                    # Calculate and append x, y coordinates of hand landmarks
                    x, y = int(landmarks.x * width), int(landmarks.y * height)
                    landmarkList.append([_id, x, y])

                # Draw Landmarks
                Draw.draw_landmarks(frame, handlm, mpHands.HAND_CONNECTIONS)

        # If landmarks list is not empty
        if landmarkList:
            # Store x,y coordinates of (tip of) thumb
            x_1, y_1 = landmarkList[4][1], landmarkList[4][2]

            # Store x,y coordinates of (tip of) index finger
            x_2, y_2 = landmarkList[8][1], landmarkList[8][2]

            # Draw circle on thumb and index finger tip
            cv2.circle(frame, (x_1, y_1), 7, (0, 255, 0), cv2.FILLED)
            cv2.circle(frame, (x_2, y_2), 7, (0, 255, 0), cv2.FILLED)

            # Draw line from tip of thumb to tip of index finger
            cv2.line(frame, (x_1, y_1), (x_2, y_2), (0, 255, 0), 3)

            # Calculate distance between thumb and index finger
            L = hypot(x_2 - x_1, y_2 - y_1)

            # Normalize coordinates to move the mouse
            mouse_x = np.interp(x_2, [0, frame.shape[1]], [0, screen_width])
            mouse_y = np.interp(y_2, [0, frame.shape[0]], [0, screen_height])

            # Move the mouse
            pyautogui.moveTo(mouse_x, mouse_y)

        # Display video and when 'q' is entered, destroy the window
        cv2.imshow("Image", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
