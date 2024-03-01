# Import required libraries
from dotenv import load_dotenv
from itertools import zip_longest

import streamlit as st
from streamlit_chat import message

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
import cv2
from bpm import detect_bpm
from bloodF import get_avg_bpm
from fear import detect_emotion

# Load environment variables
load_dotenv()

# Set streamlit page configuration
st.set_page_config(page_title="ChatBot Starter")
st.title("ChatBot Starter")

# Initialize session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []  # Store AI generated responses

if 'past' not in st.session_state:
    st.session_state['past'] = []  # Store past user inputs

if 'entered_prompt' not in st.session_state:
    st.session_state['entered_prompt'] = ""  # Store the latest user input

# Initialize the ChatOpenAI model
chat = ChatOpenAI(
    temperature=0.5,
    model_name="gpt-3.5-turbo"
)


def build_message_list():
    cap = cv2.VideoCapture(0)
    resultant = []
    BPMstate = detect_bpm(cap)
    resultant.append(BPMstate)
    get_avg_bpm = detect_bpm(cap)
    resultant.append(get_avg_bpm)
    detect_emotion = detect_bpm(cap)
    resultant.append(detect_emotion)
    """
    Build a list of messages including system, human and AI messages.
    """
    # Start zipped_messages with the SystemMessage
    zipped_messages = [SystemMessage(
        """Given the following CONTEXT and a VALUE, generate an answer based on this context only.
        In the answer, try to provide as much text as possible from the "response" section in the source document context without making many changes.
        If the answer is not found in the context, kindly state "I don't know". Don't try to make up an answer.

        CONTEXT: You are a medical healthcare professional who uses an AI assistant to monitor and assist patients in need of urgent care. The AI assistant is equipped with sensors detail provided in 'VALUES' that can measure the patient’s beats per minute (BPM), injury or blood loss (if detected, then lethality percentage), and emotion. The AI assistant can also communicate with you and the patient through voice or text, and provide relevant information and suggestions based on the situation.
        Your task is to use the AI assistant to assess the patient’s condition, act professionally and quickly, provide them with remedy, quick medical help, etc., and ask them to contact emergency services if possible. You should also explain to the patient how the AI assistant was able to infer their condition from the sensor input, and what the implications are for their health and well-being.

        VALUE: {resultant}""")]

    # Zip together the past and generated messages
    for human_msg, ai_msg in zip_longest(st.session_state['past'], st.session_state['generated']):
        if human_msg is not None:
            zipped_messages.append(HumanMessage(
                content=human_msg))  # Add user messages
        if ai_msg is not None:
            zipped_messages.append(
                AIMessage(content=ai_msg))  # Add AI messages

    return zipped_messages


def generate_response():
    """
    Generate AI response using the ChatOpenAI model.
    """
    # Build the list of messages
    zipped_messages = build_message_list()

    # Generate response using the chat model
    ai_response = chat(zipped_messages)

    return ai_response.content


# Define function to submit user input
def submit():
    # Set entered_prompt to the current value of prompt_input
    st.session_state.entered_prompt = st.session_state.prompt_input
    # Clear prompt_input
    st.session_state.prompt_input = ""


# Create a text input for user
st.text_input('YOU: ', key='prompt_input', on_change=submit)



if st.session_state.entered_prompt != "":
    # Get user query
    user_query = st.session_state.entered_prompt

    # Append user query to past queries
    st.session_state.past.append(user_query)

    # Generate response
    output = generate_response()

    # Append AI response to generated responses
    st.session_state.generated.append(output)

# Display the chat history
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        # Display AI response
        message(st.session_state["generated"][i], key=str(i))
        # Display user message
        message(st.session_state['past'][i],
                is_user=True, key=str(i) + '_user')


# Add credit