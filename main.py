import time
import numpy as np
import mss
import pyautogui

def detect_color_and_jump(region_red, region_green, jump_interval=0.1, duration=10):
    """
    Detects red in the first region and green in the second region, and jumps automatically when detected.
    
    Parameters:
    - region_red: Tuple (x, y, width, height) specifying the area to monitor for red.
    - region_green: Tuple (x, y, width, height) specifying the area to monitor for green.
    - jump_interval: Minimum time in seconds between jumps.
    - duration: Total time in seconds to run the script.
    """
    start_time = time.time()
    last_jump_time = 0
    red_rgb = (255, 0, 0)
    green_rgb = (0, 255, 0)
    blue_rgb = (0, 0, 255)

    print("Starting color detection automation...")

    with mss.mss() as sct:
        while time.time() - start_time < duration:
            # Capture screenshots for both regions using mss for better performance
            screenshot_red = np.array(sct.grab(region_red))[:, :, :3]
            screenshot_green = np.array(sct.grab(region_green))[:, :, :3]

            # Efficient check for red/blue in the first region using numpy array operations
            found_red_or_blue = np.any(
                (screenshot_red == red_rgb).all(axis=2) | (screenshot_red == blue_rgb).all(axis=2)
            )

            # Efficient check for green in the second region
            found_green = np.any((screenshot_green == green_rgb).all(axis=2))

            # Trigger jump if color is found and the jump interval has passed
            if (found_red_or_blue or found_green) and (time.time() - last_jump_time >= jump_interval):
                pyautogui.press('space',interval=0.01)
                last_jump_time = time.time()
                detected_color = "Red/Blue" if found_red_or_blue else "Green"
                print(f"{detected_color} detected! Jumping...")

    print("Color detection automation complete!")

# Get screen resolution
screen_width, screen_height = pyautogui.size()

# Define regions for detection
center_x, center_y = screen_width // 2 - 100, screen_height // 2
region_width = 5
region_height = 400

# Red detection region
left_red = center_x - region_width // 2
top_red = center_y - region_height // 2
right_red = left_red + region_width
bottom_red = top_red + region_height

# Green detection region (50 pixels to the left)
left_green = left_red - 90
top_green = top_red
right_green = left_green + region_width
bottom_green = bottom_red

# Set the regions as (left, top, right, bottom)
region_red = (left_red, top_red, right_red, bottom_red)
region_green = (left_green, top_green, right_green, bottom_green)

# Run the script
detect_color_and_jump(region_red, region_green, jump_interval=0, duration=999999)
