# app.py
import asyncio
import streamlit as st
from core import handle_query  # your handler

st.set_page_config(page_title="J.A.R.V.I.S.", page_icon="🤖", layout="wide")

# -------------------------
# Custom CSS (blue glow UI)
# -------------------------
st.markdown("""
<style>
:root{
  --bg:#060608;
  --text:#cbd6df;
  --muted:#8d98a3;
  --accent:#1e90ff;
  --accent-light:#5ec8ff;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg);
    color: var(--text);
    font-family: 'Poppins', sans-serif;
    height: 100%;
}

main .block-container {
    padding-top: 36px;
    padding-bottom: 120px; /* reserve space for input */
    max-width: 900px;  /* keep content nicely centered */
    margin: 0 auto;
}

/* Title */
h1 {
    text-align: center;
    color: var(--text);
    letter-spacing: 6px;
    margin-bottom: 6px;
    text-shadow: 0 6px 18px rgba(30,144,255,0.15);
    font-size: 42px;
}
h1::after{
    content: "";
    display:block;
    margin: 10px auto 0;
    width: 100px;
    height: 5px;
    border-radius: 999px;
    background: linear-gradient(90deg, rgba(94,200,255,0.12), rgba(30,144,255,0.22));
}

/* Chat messages */
[data-testid="stChatMessage"] {
    margin: 12px 0;
}
[data-testid="stChatMessage"] > div {
    border-radius: 14px;
    padding: 14px 18px;
    background: rgba(255,255,255,0.03);
    color: var(--text);
    line-height: 1.6;
    box-shadow: 0 3px 18px rgba(0,0,0,0.5);
}

/* Assistant = blue tint */
[data-testid="stChatMessage"][data-author="assistant"] > div {
    background: rgba(30,144,255,0.05);
    border-left: 4px solid var(--accent);
}

/* User = red tint */
[data-testid="stChatMessage"][data-author="user"] > div {
    background: rgba(229,9,20,0.06);
    border-right: 4px solid #ff4f4f;
}

/* Input box pinned bottom */
[data-testid="stChatInput"] > div {
    position: fixed;
    bottom: 18px;
    left: 50%;
    transform: translateX(-50%);
    width: calc(100% - 40px);
    max-width: 900px;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(30,144,255,0.18);
    border-radius: 999px;
    padding: 8px 14px;
    box-shadow: 0 6px 26px rgba(8,18,36,0.7);
    z-index: 1000;
}

/* Input field */
[data-testid="stChatInput"] input {
    background: transparent !important;
    border: none !important;
    color: var(--text) !important;
    font-size: 16px;
    flex: 1;
}
[data-testid="stChatInput"] input::placeholder {
    color: rgba(200,220,255,0.35) !important;
}

/* Send button */
[data-testid="stChatInput"] button {
    border-radius: 50%;
    background: var(--accent);
    color: white;
    border: none;
    width: 40px;
    height: 40px;
    transition: 0.2s;
}
[data-testid="stChatInput"] button:hover {
    background: var(--accent-light);
    transform: translateY(-2px);
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Main UI
# -------------------------
st.title("J.A.R.V.I.S.")
st.markdown("<p style='text-align:center;color:#8d98a3;'>Your personal AI assistant.</p>", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

# show chat history
for role, content in st.session_state.history:
    with st.chat_message(role):
        st.markdown(content)

# input handling
if prompt := st.chat_input("How may I assist you?"):
    st.session_state.history.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer = asyncio.run(handle_query(prompt))
            except Exception as e:
                answer = f"⚠️ Error: {e}"
            st.markdown(answer)
            st.session_state.history.append(("assistant", answer))
