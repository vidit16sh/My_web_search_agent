import asyncio
import streamlit as st
from core import handle_query
import base64

st.set_page_config(page_title="J.A.R.V.I.S.", page_icon="🤖", layout="wide")

# Convert background image to base64
def get_base64(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

background_image = "image.png"
bg_base64 = get_base64(background_image)

# Custom CSS with embedded base64 background
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');

html, body, [data-testid="stAppViewContainer"] {{
    font-family: 'Poppins', sans-serif;
    color: #e0e0e0;
    min-height: 100vh;
    background: url("data:image/png;base64,{bg_base64}") no-repeat center center fixed;
    background-size: cover;
}}

/* Title */
h1 {{
    font-family: 'Bebas Neue', sans-serif;
    text-align: center;
    color: #FFD700;
    text-shadow: 0 0 20px rgba(255, 215, 0, 0.7);
    margin-bottom: 0.2em;
}}
p {{
    text-align: center;
    color: #bbb;
    margin-top: -0.3em;
}}

/* Chat bubbles */
[data-testid="stChatMessage"] {{
    padding: 0.9em 1.1em;
    margin: 0.5em 0;
    border-radius: 14px;
    backdrop-filter: blur(14px);
    border-left: 3px solid;
    word-wrap: break-word;
    white-space: pre-wrap;
    animation: fadeIn 0.3s ease-in-out;
}}

/* User bubble */
[data-testid="stChatMessage"][data-author="user"] {{
    background: rgba(229, 9, 20, 0.12);
    border-color: #E50914;
    margin-left: auto;
    max-width: 60%;
}}

/* Assistant bubble */
[data-testid="stChatMessage"][data-author="assistant"] {{
    background: rgba(255, 215, 0, 0.12);
    border-color: #FFD700;
    margin-right: auto;
    max-width: 75%;
}}

/* Smooth fade-in animation */
@keyframes fadeIn {{
  from {{ opacity: 0; transform: translateY(8px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}
</style>
""", unsafe_allow_html=True)

# Main UI
_, center_col, _ = st.columns([1, 4, 1])
with center_col:
    st.title("J.A.R.V.I.S.")
    st.markdown("<p>Your personal AI assistant.</p>", unsafe_allow_html=True)

    # Conversation history
    if "history" not in st.session_state:
        st.session_state.history = []

    for role, content in st.session_state.history:
        with st.chat_message(role):
            st.markdown(content)

    # Chat input
    if query := st.chat_input("How may I assist you?"):
        with st.chat_message("user"):
            st.markdown(query)

        answer = asyncio.run(handle_query(query))
        with st.chat_message("assistant"):
            st.markdown(answer)

        st.session_state.history.append(("user", query))
        st.session_state.history.append(("assistant", answer))
