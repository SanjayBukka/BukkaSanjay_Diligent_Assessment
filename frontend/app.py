import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(page_title="Enterprise AI Assistant")

st.title("Enterprise AI Assistant")
st.write("Ask questions based on enterprise knowledge.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Enter your question")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    response = requests.post(
        API_URL,
        json={"query": user_input}
    ).json()

    answer = response.get("answer", "")
    source = response.get("source", "")

    assistant_reply = answer
    if source:
        assistant_reply += f"\n\nSource:\n{source}"

    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_reply}
    )

    st.rerun()
