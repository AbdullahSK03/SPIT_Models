import pickle
import numpy as np
import librosa

# Load the model from the pickle file
with open('pickle_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Define the function to extract features
def extract_features(audio_data, sample_rate, max_pad_len=500):
    audio_data = audio_data.astype(np.float32) / 32767.0
    mfccs = librosa.feature.mfcc(y=audio_data, sr=sample_rate, n_mfcc=40)
    
    # If the number of frames is less than max_pad_len, pad with zeros
    if (mfccs.shape[1] < max_pad_len):
        pad_width = max_pad_len - mfccs.shape[1]
        mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')

    # If the number of frames is more than max_pad_len, truncate the excess
    elif (mfccs.shape[1] > max_pad_len):
        mfccs = mfccs[:, :max_pad_len]

    # Flatten the array
    mfccs = mfccs.flatten()

    return mfccs

# Assume we have a .wav file for inference
file_path = r'C:\Users\ahmds\Desktop\SPIT\input\Actor_01\03-01-01-01-01-01-01.wav'

# Load the audio file
audio_data, sample_rate = librosa.load(file_path)

# Extract features
features = extract_features(audio_data, sample_rate)

# Use the model for inference
emotion = model.predict([features])

print("Predicted emotion: ", emotion[0])
