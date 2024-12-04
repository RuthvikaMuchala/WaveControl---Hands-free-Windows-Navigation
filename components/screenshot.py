import cv2
import mediapipe as mp
from math import hypot
import pyautogui


def take_snapshot(mpHands, hands, Draw):
    # Start capturing video from webcam
    cap = cv2.VideoCapture(0)

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

            # Check for specific gesture (thumbs up)
            if landmarkList:
                # Store y-coordinate of thumb and index finger
                thumb_y = landmarkList[4][2]
                index_y = landmarkList[8][2]

                # Gesture detection logic
                if thumb_y < index_y:  # Thumbs up if thumb is above index finger
                    # Take a screenshot
                    screenshot = pyautogui.screenshot()
                    screenshot.save("screenshot.png")
                    cv2.putText(
                        frame,
                        "Screenshot Taken!",
                        (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2,
                    )

        # Display video and when 'q' is entered, destroy the window
        cv2.imshow("Image", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
