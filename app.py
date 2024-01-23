import streamlit as st
import asyncio
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions, Microphone
import time
import queue
from summarize import summarize_text
from transcribe import init_deepgram,transcribe_live

def reset_session_state():
    st.session_state['transcription'] = ""
    st.session_state['summaries'] = []
    st.session_state['state'] = False
    
def initialize_session_state():
    if 'summaries' not in st.session_state:
        st.session_state['summaries'] = []
    if 'state' not in st.session_state:
        st.session_state['state'] = False
    if 'transcription' not in st.session_state:
        st.session_state.transcription = ""
        
def main():
   
    # Initialize Deepgram Client
    deepgram = DeepgramClient(api_key=st.secrets["DEEPGRAM_API_KEY"])
    # Create a thread-safe queue
    transcription_queue = queue.Queue()
    
    st.title("Note taking / Real-Time Transcription :studio_microphone:")
    initialize_session_state()
    

    transcription_queue = queue.Queue()
    deepgram = init_deepgram(st.secrets["DEEPGRAM_API_KEY"])

    col1, col2 = st.columns(2)
    

    if col2.button('Clear Transcription'):
        reset_session_state()

    if col1.button('Start/Stop Transcription'):
        st.session_state['state'] = not st.session_state['state']
        if st.session_state['state']:
            col1.image("public/noice.gif",use_column_width=True  )
            with col2.container(height=300, border=True):
                    asyncio.run(transcribe_live(deepgram, transcription_queue, st.session_state))

        else:
            # Display the transcription and summaries
            st.text_area("Transcription", st.session_state.transcription, height=300)
            st.write("Summaries")
            for summary in st.session_state['summaries']:
                st.markdown(summary)

if __name__ == "__main__":
    main()
