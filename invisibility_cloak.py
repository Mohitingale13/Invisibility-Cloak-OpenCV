import cv2
import numpy as np

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Allow the camera to warm up
import time
time.sleep(2)

# Capture the background
background = None
for _ in range(30):  # Capture 30 frames to get a stable background
    ret, background = cap.read()
    if not ret:
        print("Failed to capture background")
        exit()

# Flip the background to remove the mirror effect
background = cv2.flip(background, 1)

# Main loop
while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    # Flip the frame to remove the mirror effect
    frame = cv2.flip(frame, 1)

    # Convert the frame to HSV color space (easier to handle colors)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the range for green color in HSV
    lower_green = np.array([35, 50, 50])  # Lower bound for green
    upper_green = np.array([85, 255, 255])  # Upper bound for green

    # Create a mask for the green color
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Invert the mask (to keep everything except the green cloak)
    mask_inv = cv2.bitwise_not(mask)

    # Use the mask to extract the background and the cloak region
    cloak_region = cv2.bitwise_and(background, background, mask=mask)
    remaining_frame = cv2.bitwise_and(frame, frame, mask=mask_inv)

    # Combine the two regions to create the final output
    result = cv2.add(cloak_region, remaining_frame)

    # Display the result
    cv2.imshow("Invisibility Cloak", result)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()