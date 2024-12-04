import tkinter as tk
from tkinter import font
from components import brightness, mouse_pointer, screenshot, volume, switch_apps
from model.mediapipeModel import mediapipe_model

mpHands, Hands, Draw = mediapipe_model()


def feature_control_brightness():
    brightness.adjust_brightness(mpHands=mpHands, hands=Hands, Draw=Draw)


def feature_mouse_control():
    mouse_pointer.move_pointer(mpHands=mpHands, hands=Hands, Draw=Draw)


def feature_volume_control():
    volume.adjust_volume(mpHands=mpHands, hands=Hands, Draw=Draw)


def feature_screenshot():
    screenshot.take_snapshot(mpHands=mpHands, hands=Hands, Draw=Draw)


def feature_application_switch():
    switch_apps.tab_switch(mpHands=mpHands, hands=Hands, Draw=Draw)


window = tk.Tk()
window.title("Windows Gesture Control")
window.geometry("500x500")
window.configure(bg="#282C34")

title_font = font.Font(family="Helvetica", size=20, weight="bold")
button_font = font.Font(family="Helvetica", size=12)

title_label = tk.Label(
    window, text="Gesture Control Panel", font=title_font, fg="#61AFEF", bg="#282C34"
)
title_label.pack(pady=20)


# Function to style buttons consistently
def create_button(text, command):
    return tk.Button(
        window,
        text=text,
        font=button_font,
        width=20,
        height=2,
        bg="#98C379",  # Soft green color
        fg="white",  # White text
        bd=0,  # No border
        relief="flat",  # Flat appearance
        activebackground="#56B6C2",  # Different color when pressed
        activeforeground="white",  # Text color when pressed
        command=command,
    )


# Adding buttons for each feature
btn_brightness = create_button("Brightness Control", feature_control_brightness)
btn_mouse = create_button("Mouse Control", feature_mouse_control)
btn_volume = create_button("Volume Control", feature_volume_control)
btn_screenshot = create_button("Screenshot", feature_screenshot)
btn_app_switch = create_button("Application Switch", feature_application_switch)

# Display buttons with spacing
btn_brightness.pack(pady=10)
btn_mouse.pack(pady=10)
btn_volume.pack(pady=10)
btn_screenshot.pack(pady=10)
btn_app_switch.pack()

# Start the Tkinter event loop
window.mainloop()
