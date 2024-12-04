import cv2
import numpy as np
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


def adjust_volume(mpHands, hands, Draw):
    # Initialize volume control
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

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
        # if hands are present in image(frame)
        if Process.multi_hand_landmarks:
            # detect handmarks
            for handlm in Process.multi_hand_landmarks:
                for _id, landmarks in enumerate(handlm.landmark):
                    # store height and width of image
                    height, width, color_channels = frame.shape

                    # calculate and append x, y coordinates
                    # of handmarks from image(frame) to lmList
                    x, y = int(landmarks.x * width), int(landmarks.y * height)
                    landmarkList.append([_id, x, y])

                # draw Landmarks
                Draw.draw_landmarks(frame, handlm, mpHands.HAND_CONNECTIONS)

        # If landmarks list is not empty
        if landmarkList:
            # store x,y coordinates of (tip of) thumb
            x_1, y_1 = landmarkList[4][1], landmarkList[4][2]

            # store x,y coordinates of (tip of) index finger
            x_2, y_2 = landmarkList[8][1], landmarkList[8][2]

            # draw circle on thumb and index finger tip
            cv2.circle(frame, (x_1, y_1), 7, (0, 255, 0), cv2.FILLED)
            cv2.circle(frame, (x_2, y_2), 7, (0, 255, 0), cv2.FILLED)

            # draw line from tip of thumb to tip of index finger
            cv2.line(frame, (x_1, y_1), (x_2, y_2), (0, 255, 0), 3)

            # calculate distance between thumb and index finger
            L = hypot(x_2 - x_1, y_2 - y_1)

            # Set volume level (0.0 - 1.0)
            v_level = np.interp(L, [15, 220], [0.0, 1.0])
            volume.SetMasterVolumeLevelScalar(v_level, None)

        # Display Video and when 'q' is entered, destroy the window
        cv2.imshow("Image", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()