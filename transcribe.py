# transcription.py
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions, Microphone
import time
import asyncio
from summarize import summarize_text
import streamlit as st

# col1, col2 = st.columns(2)   
# transcription_container = col1.container(height=300, border=True)
# summary_container = col2.container(height=300, border=True)

# Initialize Deepgram Client
def init_deepgram(api_key):
    return DeepgramClient(api_key=api_key)

def on_message(transcription_queue):
    def callback(self, result, **kwargs):
        transcript = result.channel.alternatives[0].transcript
        if transcript:
            transcription_queue.put(transcript)
    return callback

def on_error():
    def callback(self, error, **kwargs):
        print(f"Error: {error}")
    return callback

async def transcribe_live(dg_client, transcription_queue, session_state):
    dg_connection = dg_client.listen.live.v("1")
    options = LiveOptions(
        smart_format=True,
        language="en-US",
        encoding="linear16",
        channels=1,
        sample_rate=16000,
    )

    dg_connection.start(options)
    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message(transcription_queue))
    dg_connection.on(LiveTranscriptionEvents.Error, on_error())

    microphone = Microphone(dg_connection.send)
    microphone.start()

    last_summary_time = time.time()
    last_pos = 0
    last_transcript_length = 0 

    try:
        while session_state['state']:
            await asyncio.sleep(1)
            current_time = time.time()
            
            while not transcription_queue.empty():
                transcript = transcription_queue.get()
                session_state.transcription += transcript + " "
                st.write(transcript)

            print (len(session_state.transcription) - last_pos)
            if current_time - last_summary_time >= 10 and session_state['state'] and (len(session_state.transcription) - last_pos >= 10):
                # Update this to your summarizing logic
                summary, new_pos = summarize_text(session_state.transcription, last_pos)
                session_state['summaries'].append(summary)
                st.markdown(f':nerd_face: ### Summaries :green[{summary}]')
                st.divider()
                last_summary_time = current_time
                last_pos = new_pos
    finally:
        microphone.finish()
        dg_connection.finish()
