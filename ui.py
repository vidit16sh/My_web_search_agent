import asyncio
import streamlit as st
from core import handle_query

st.set_page_config(page_title="J.A.R.V.I.S.", page_icon="🤖", layout="wide")

# Correct the path to your background image
background_image = "image.png"

# Custom CSS with background image
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');

html, body, [data-testid="stAppViewContainer"] {{
    font-family: 'Poppins', sans-serif;
    color: #e0e0e0;
    min-height: 100vh;
    background: url("{background_image}");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

h1 {{
    font-family: 'Bebas Neue', sans-serif;
    text-align: center;
    color: #FFD700;
    text-shadow: 0 0 15px rgba(255, 215, 0, 0.6);
    padding-bottom: 0.3em;
}}

p {{
    text-align: center;
    color: #a0a0a0;
    margin-top: -0.5em;
}}

/* Fix chat bubbles for st.chat_message */
[data-testid="stChatMessage"] {{
    display: flex;
    justify-content: flex-start;
    align-items: flex-start;
    padding: 0.9em 1.1em;
    margin: 0.6em 0;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(12px);
    border-left: 3px solid;
    word-wrap: break-word;
    white-space: pre-wrap;
}}

/* User chat bubble styling */
[data-testid="stChatMessage"][data-author="user"] {{
    background: rgba(229, 9, 20, 0.1);
    border-color: #E50914;
    margin-left: auto;
    max-width: 60%;
    min-width: 15%;
}}

/* Assistant chat bubble styling */
[data-testid="stChatMessage"][data-author="assistant"] {{
    background: rgba(255, 215, 0, 0.1);
    border-color: #FFD700;
    margin-right: auto;
    max-width: 80%;
    min-width: 25%;
}}
</style>
""", unsafe_allow_html=True)

# Main container for centering content
_, center_col, _ = st.columns([1, 4, 1])

with center_col:
    # Title and description
    st.title("J.A.R.V.I.S.")
    st.markdown("<p>Your personal AI assistant.</p>", unsafe_allow_html=True)

    # Conversation history
    if "history" not in st.session_state:
        st.session_state.history = []

    # Display chat history within the centered column
    for role, content in st.session_state.history:
        with st.chat_message(role):
            st.markdown(content)

    # Chat input
    if query := st.chat_input("How may I assist you?"):
        # Display user message
        with st.chat_message("user"):
            st.markdown(query)

        # Get bot response and display
        answer = asyncio.run(handle_query(query))
        with st.chat_message("assistant"):
            st.markdown(answer)

        # Append to history
        st.session_state.history.append(("user", query))
        st.session_state.history.append(("assistant", answer))