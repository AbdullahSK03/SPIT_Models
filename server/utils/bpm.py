import numpy as np
import cv2
import sys
import time
from cvzone.FaceDetectionModule import FaceDetector
from cvzone.PlotModule import LivePlot
import cvzone

def detect_bpm(webcam):
    realWidth = 640   
    realHeight = 480  
    videoWidth = 160
    videoHeight = 120
    videoChannels = 3
    videoFrameRate = 30

    # Webcam Parameters
    
    detector = FaceDetector()

    webcam.set(3, realWidth)
    webcam.set(4, realHeight)

    # Color Magnification Parameters
    levels = 3
    alpha = 170
    minFrequency = 1.0
    maxFrequency = 2.0
    bufferSize = 150
    bufferIndex = 0

    plotY = LivePlot(realWidth,realHeight,[60,120],invert=True)

    # Helper Methods
    def buildGauss(frame, levels):
        pyramid = [frame]
        for level in range(levels):
            frame = cv2.pyrDown(frame)
            pyramid.append(frame)
        return pyramid

    def reconstructFrame(pyramid, index, levels):
        filteredFrame = pyramid[index]
        for level in range(levels):
            filteredFrame = cv2.pyrUp(filteredFrame)
        filteredFrame = filteredFrame[:videoHeight, :videoWidth]
        return filteredFrame

    # Initialize Gaussian Pyramid
    firstFrame = np.zeros((videoHeight, videoWidth, videoChannels))
    firstGauss = buildGauss(firstFrame, levels+1)[levels]
    videoGauss = np.zeros((bufferSize, firstGauss.shape[0], firstGauss.shape[1], videoChannels))
    fourierTransformAvg = np.zeros((bufferSize))

    # Bandpass Filter for Specified Frequencies
    frequencies = (1.0*videoFrameRate) * np.arange(bufferSize) / (1.0*bufferSize)
    mask = (frequencies >= minFrequency) & (frequencies <= maxFrequency)

    # Heart Rate Calculation Variables
    bpmCalculationFrequency = 10   #15
    bpmBufferSize = 10
    bpmBuffer = np.zeros((bpmBufferSize))

    bpm_values = []
    start_time = time.time()
    while (time.time() - start_time) < 10:  # Capture frames for 5 seconds
        ret, frame = webcam.read()
        if ret == False:
            break

        frame, bboxs = detector.findFaces(frame,draw=False)
        frameDraw = frame.copy()

        if bboxs:
            x1, y1, w1, h1 = bboxs[0]['bbox']
            detectionFrame = frame[y1:y1 + h1, x1:x1 + w1]
            detectionFrame = cv2.resize(detectionFrame,(videoWidth,videoHeight))

            # Construct Gaussian Pyramid
            videoGauss[bufferIndex] = buildGauss(detectionFrame, levels+1)[levels]
            fourierTransform = np.fft.fft(videoGauss, axis=0)

            # Bandpass Filter
            fourierTransform[mask == False] = 0

            # Grab a Pulse
            if bufferIndex % bpmCalculationFrequency == 0:
                for buf in range(bufferSize):
                    fourierTransformAvg[buf] = np.real(fourierTransform[buf]).mean()
                hz = frequencies[np.argmax(fourierTransformAvg)]
                bpm = 60.0 * hz
                bpmBuffer = np.roll(bpmBuffer, -1)  # Shift the buffer
                bpmBuffer[-1] = bpm  # Add new BPM to the buffer

            # Amplify
            filtered = np.real(np.fft.ifft(fourierTransform, axis=0))
            filtered = filtered * alpha

            # Reconstruct Resulting Frame
            filteredFrame = reconstructFrame(filtered, bufferIndex, levels)
            outputFrame = detectionFrame + filteredFrame
            outputFrame = cv2.convertScaleAbs(outputFrame)

            bufferIndex = (bufferIndex + 1) % bufferSize

            bpm_value = bpmBuffer.mean()
            bpm_values.append(bpm_value)

    avg_bpm = np.mean(bpm_values)
    webcam.release()
    cv2.destroyAllWindows()
    return avg_bpm

# Example usage:
# webcam = cv2.VideoCapture(0)
cap = cv2.VideoCapture(0)
print("Average BPM:", detect_bpm(cap))
