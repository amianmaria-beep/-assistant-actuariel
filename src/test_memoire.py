import streamlit as st
import anthropic
from dotenv import load_dotenv
import os

load_dotenv()

if "messages" not in st.session_state:
    st.session_state.messages = []

if prompt := st.chat_input("Question :"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        messages=st.session_state.messages
    )
    st.session_state.messages.append({
        "role": "assistant",
        "content": response.content[0].text
    })

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])