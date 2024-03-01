import cv2
import numpy as np
import time
# Define a function that takes a video capture object as an argument
def get_avg_bpm(cap):
    # Initialize a list to store the number of red objects per frame
    red_objects = []
    # Initialize a variable to store the current time in seconds
    start_time = time.time()
    # Initialize a variable to store the duration of the video in seconds
    duration = 0
    # Loop until the duration reaches 10 seconds or the user presses 'q'
    while duration < 10:
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
        large_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 300]
        # Draw contours on the original frame
        cv2.drawContours(frame, large_contours, -1, (0,255,0), 1)
        # Display the resulting frame
        cv2.imshow('frame', frame)
        # Append the number of red objects to the list
        red_objects.append(len(large_contours))
        # Update the duration by subtracting the current time from the start time
        duration = time.time() - start_time
        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # Release the capture
    cap.release()
    cv2.destroyAllWindows()
    # Calculate the average BPM by multiplying the mean of the list by 6
    avg_bpm = np.mean(red_objects)*10
    # Return the average BPM
    return avg_bpm

# Start video capture
cap = cv2.VideoCapture(0)
# Call the function and print the result
print("Injury %:", get_avg_bpm(cap))
