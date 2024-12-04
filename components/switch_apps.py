# Importing Libraries
import cv2
import mediapipe as mp
import pyautogui
import time


def tab_switch(mpHands, hands, Draw):
    # Start capturing video from webcam
    cap = cv2.VideoCapture(0)

    # Variables to track previous x-coordinates and gesture states
    previous_x = None
    gesture_state = None  # To track the current gesture state

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
                    x = int(landmarks.x * width)
                    y = int(landmarks.y * height)
                    landmarkList.append([_id, x, y])

                # Draw Landmarks
                Draw.draw_landmarks(frame, handlm, mpHands.HAND_CONNECTIONS)

            # Check for specific gestures
            if landmarkList:
                # Get the x-coordinate of the index finger tip (Landmark 8)
                index_x = landmarkList[8][1]

                # If previous_x is None, set it to current x
                if previous_x is None:
                    previous_x = index_x

                # Calculate the swipe distance
                swipe_distance = index_x - previous_x

                # Gesture state management
                if swipe_distance > 50 and gesture_state != "swipe_right":
                    # Swipe left to right to switch applications (Alt+Tab)
                    pyautogui.hotkey("alt", "tab")
                    time.sleep(1)  # Delay to avoid multiple triggers
                    cv2.putText(
                        frame,
                        "Switching Applications!",
                        (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2,
                    )
                    gesture_state = "swipe_right"  # Update gesture state

                # Reset gesture state if no significant movement is detected
                if abs(swipe_distance) < 30:
                    gesture_state = None

                # Update previous_x with the current index finger position
                previous_x = index_x

        # Display video and when 'q' is entered, destroy the window
        cv2.imshow("Image", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
