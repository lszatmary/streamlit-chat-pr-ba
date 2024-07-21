import json
from pathlib import Path
import streamlit as st


filepath = Path("history_proba.json")

if "messages" not in st.session_state:
    st.session_state.messages = []
    with filepath.open("r", encoding="utf-8") as f:
        history = json.load(f)
    # print(type(history))
    for m in history:
        if isinstance(m, dict):
            st.session_state.messages.append(m)

# st.write(st.session_state)

# TODO githubra felrakni és deployolni

st.title("Json együttműködés")



if user_input := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content":user_input})

    st.session_state.messages.append({"role": "assistant", "content":str("".join([c for c in user_input[::2]]))})
    with filepath.open("w", encoding="utf-8") as f:
        json.dump(st.session_state.messages, f)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

