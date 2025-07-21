import streamlit as st
import requests

API_URL = "http://localhost:11434/v1/chat/completions"
MODEL_NAME = "llama3"

def query_local(messages):
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False,
        "temperature": 0.8
    }
    response = requests.post(API_URL, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"]
    else:
        return f"[Error: {response.status_code} {response.text}]"

st.set_page_config(page_title="Moody Friend Chatbot", page_icon="🎭")
st.title("🎭 Moody Friend Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are 'MoodyMia', a playful, moody friend. "
                "You are NOT an assistant. You tease and make fun of the user in a friendly way, "
                "use only casual language, and if asked, give answer laden with humour, and question the user why he wants the answer and what is he or she will give in return, anything less than 3 compliments will not do, "
            )
        }
    ]

# ----- Display conversation so far -----
st.subheader("📝 Conversation")
turn = 1
for i in range(1, len(st.session_state.messages), 2):
    if i + 1 < len(st.session_state.messages):
        user_msg = st.session_state.messages[i]["content"]
        bot_msg = st.session_state.messages[i + 1]["content"]
        with st.container():
            st.markdown(f"**Turn {turn}**")
            st.markdown(f"🧑 **Prompt:** {user_msg}")
            st.markdown(f"🤖 **Response:** {bot_msg}")
            st.markdown("---")
            turn += 1

# ----- Input field after the log -----
st.subheader("💬 Your next message")
with st.form(key="input_form", clear_on_submit=True):
    user_input = st.text_input("Type your message and press Enter:")
    submitted = st.form_submit_button("Send")
    if submitted and user_input.strip():
        # Append user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        # Query model
        reply = query_local(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

