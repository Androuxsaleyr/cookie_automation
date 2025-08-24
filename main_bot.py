import pyautogui
import time
import keyboard
import cv2
import sys
import numpy as np
import os

# Function to take screenshot to be analyzed when we press S
def take_screenshot():
    while True:
        if keyboard.read_key() == 's':
            screenshot = pyautogui.screenshot()
            
            # Get the directory where the script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Create screenshots folder if it doesn't exist
            screenshots_dir = os.path.join(script_dir, "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            
            # Create the full path
            path = os.path.join(screenshots_dir, "cookie_screenshot.png")
            
            screenshot.save(path)
            print(f"Screenshot saved to: {path}")
            return path


img = cv2.imread(take_screenshot())

#main mask making and finder
def find_cookie(img):
    # lets detect brown color in the screenshot first we need to conver it from RGB to HSV (Hue, Saturation, Value)
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Then we define the range of colors of brown
    lower_brown = np.array([10,100,20])
    upper_brown = np.array([20,255,200]) 
    # Then we Create a mask for brown color
    brown_mask = cv2.inRange(hsv_image, lower_brown, upper_brown)
    contours, _ = cv2.findContours(brown_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
    output_image = cv2.cvtColor(brown_mask, cv2.COLOR_GRAY2BGR)
    # Find the largest contour
    largest_contour = max(contours, key=cv2.contourArea)

    cv2.drawContours(img, [largest_contour], -1, (0, 255, 0), 3)

    # Compute the moments of the largest contour
    M = cv2.moments(largest_contour)

    # Calculate the centroid
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
    else:
        cx, cy = 0, 0
    
    cv2.drawContours(img, [largest_contour], -1, (0, 255, 0), 2)
    cv2.circle(img, (cx, cy), 5, (255, 0, 0), -1)
    cv2.imwrite('largest_contour.png', img)
    return cx,cy

cx, cy = find_cookie(img)

def auto_click(x, y):
    while True:
        if keyboard.is_pressed('u'):
            break
        elif keyboard.is_pressed('p'):
            while True:
                if keyboard.is_pressed('c'):
                    break
                elif keyboard.is_pressed('u'):
                    return
                time.sleep(0.01)
        pyautogui.click(x, y)
        time.sleep(0.01)


while True:
    if keyboard.is_pressed('c'):
        auto_click(cx, cy)
    elif keyboard.is_pressed('u'):
        break
    time.sleep(0.01)
