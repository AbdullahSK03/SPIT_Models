import cv2
import numpy as np

# Start video capture
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define range for red color in HSV
    lower_red = np.array([0,100,100])
    upper_red = np.array([10,255,255])

    # Threshold the HSV image to get only red colors
    mask = cv2.inRange(hsv, lower_red, upper_red)
    cv2.imshow('mask', mask)
    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Filter out small contours based on area
    large_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 100]

    # Draw contours on the original frame
    cv2.drawContours(frame, large_contours, -1, (0,255,0), 1)

    # Display the count of red objects
    print("Number of red objects:", len(large_contours))

    # Display the resulting frame
    cv2.imshow('frame', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()
