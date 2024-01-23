# Initialize OpenAI
import streamlit as st
from openai import OpenAI

########################################################SUMMARIZATIONAI######################################################
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

@st.cache_data
def summarize_text(text:str, start_pos:int) -> (str, int):
    summary = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt="Provide the key points that summarizes the following text :\n\n" + text[start_pos:],
        max_tokens=150,
        temperature=0.3
    )
    return summary.choices[0].text.strip(), len(text)

#########################################################file_utils##########################################################
#

#########################################################gif################################################################
