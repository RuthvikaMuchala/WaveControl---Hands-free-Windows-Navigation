import mediapipe as mp


def mediapipe_model():
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(
        static_image_mode=False,
        model_complexity=1,
        min_detection_confidence=0.75,
        min_tracking_confidence=0.75,
        max_num_hands=2,
    )

    Draw = mp.solutions.drawing_utils

    return mpHands, hands, Draw
