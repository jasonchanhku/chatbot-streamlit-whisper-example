import streamlit as st
from tempfile import NamedTemporaryFile
from audiorecorder import audiorecorder
from whispercpp import Whisper

# Download whisper.cpp
w = Whisper('tiny')

def inference(audio):
    # Save audio to a file:
    with NamedTemporaryFile(suffix=".mp3") as temp:
        with open(f"{temp.name}", "wb") as f:
            f.write(audio.tobytes())
        result = w.transcribe(f"{temp.name}")
        text = w.extract_text(result)
    return text[0]

# Streamlit
with st.sidebar:
    audio = audiorecorder("Click to send voice message", "Recording... Click when you're done", key="recorder")
    st.title("Echo Bot with Whisper")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

response_container = st.container()
input_container = st.container()

with response_container:
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        
with input_container:
    
    # React to user input
    if (prompt := st.text_input('Movie title')) or len(audio):
        # If it's coming from the audio recorder transcribe the message with whisper.cpp
        if len(audio)>0:
            prompt = inference(audio)

        with response_container:
            # Display user message in chat message container
            st.chat_message("user").markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
        
            response = f"Echo: {prompt}"
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
