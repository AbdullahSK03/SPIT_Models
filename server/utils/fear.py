import cv2
import numpy as np
from keras.preprocessing import image
import warnings
warnings.filterwarnings("ignore")
from keras.models import load_model
import time 

def detect_emotion(cap):
    model = load_model(r"C:\SPIT\video\best_model.h5")
    face_haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    

    emotions_detected = []
    start_time = time.time()
    while (time.time() - start_time) < 5:  # Capture frames for 5 seconds
        ret, test_img = cap.read()
        if not ret:
            continue
        gray_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)

        faces_detected = face_haar_cascade.detectMultiScale(gray_img, 1.32, 5)

        for (x, y, w, h) in faces_detected:
            cv2.rectangle(test_img, (x, y), (x + w, y + h), (0, 255, 0), thickness=1)
            roi_gray = gray_img[y:y + w, x:x + h]
            roi_gray = cv2.resize(roi_gray, (224, 224))
            img_pixels = image.img_to_array(roi_gray)
            img_pixels = np.expand_dims(img_pixels, axis=0)
            img_pixels /= 255

            predictions = model.predict(img_pixels)

            max_index = np.argmax(predictions[0])

            emotions = ('neutral', 'disgust', 'fear', 'happy', 'sad', 'neutral', 'angry')
            predicted_emotion = emotions[max_index]

            emotions_detected.append(predicted_emotion)

    cap.release()
    cv2.destroyAllWindows()
    avg_emotion = max(set(emotions_detected), key=emotions_detected.count)
    return avg_emotion

# Example usage:
cap = cv2.VideoCapture(0)
avg_emotion = detect_emotion(cap)
print("Average Emotion Detected:", avg_emotion)
