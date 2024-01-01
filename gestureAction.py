# gesture_actions.py
import pyautogui
import cv2
import time
import math
import subprocess
import mediapipe as mp

def set_volume(volume):
    applescript = f"set volume output volume {volume}"
    subprocess.run(["osascript", "-e", applescript])
    
def get_current_volume():
    result = subprocess.run(["osascript", "-e", "output volume of (get volume settings)"], capture_output=True, text=True)
    return int(result.stdout.strip())

def performGestureAction(fingers, frame, hand, current_volume, volumeGesture, volumeTime, init_volume, dist, lm, mpHands, mpDraw):
    # Move the cursor if all fingers are extended
    if ["1", "1", "1", "1", "1"] == fingers:
        frame_h, frame_w, _ = frame.shape
        landmarks = hand[0].landmark
        finger_tip = landmarks[8]

        # Calculate the coordinates of the finger tip
        x = int(finger_tip.x * frame_w)
        y = int(finger_tip.y * frame_h)
        screen_w, screen_h = pyautogui.size()

        # Calculate the cursor's coordinates on the screen
        screen_x = int(finger_tip.x * screen_w * 1.25)
        screen_y = int(finger_tip.y * screen_h * 1.25)

        # Move the cursor to the calculated coordinates
        pyautogui.moveTo(screen_x, screen_y)

    elif ["1", "1", "1", "1"] == fingers[1:5]:
        pyautogui.click()
        pyautogui.sleep(1)

    elif ["1", "1"] == fingers[1:3]:
        pyautogui.scroll(-5)

    elif ["0", "1"] == fingers[0:2]:
        pyautogui.scroll(5)

    elif ["1", "1"] == fingers[0:2]:
        cv2.putText(frame, f"volume {current_volume}", (10, 200), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 255))
        if volumeGesture:
            if time.time() - volumeTime >= 0.5:
                tf = [lm[4].x, lm[4].y]
                pf = [lm[8].x, lm[8].y]
                if dist:
                    current_dist = math.dist(tf, pf)
                    current_volume = init_volume + round((current_dist - dist) * 450)
                    if current_volume > 100: current_volume = 100
                    elif current_volume < 0: current_volume = 0
                    set_volume(current_volume)
                else:
                    dist = math.dist(tf, pf)
        else:
            init_volume = get_current_volume()
            current_volume = init_volume
            volumeGesture = True
            volumeTime = time.time()
    else:
        volumeGesture = False
        dist = None
    mpDraw.draw_landmarks(frame, hand[0], mpHands.HAND_CONNECTIONS)

    return current_volume, volumeGesture, volumeTime, init_volume, dist
