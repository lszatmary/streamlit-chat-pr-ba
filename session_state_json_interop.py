import json
from pathlib import Path

import streamlit as st
from st_files_connection import FilesConnection

filepath = Path("history_proba.json")

conn = st.connection('s3', type=FilesConnection)
df = conn.read("lsz-streamlit-chat-proba-bucket-1/chat_proba_1/history_proba.json", input_format="json", ttl=600)

if "messages" not in st.session_state:
    st.session_state.messages = []
    with filepath.open("r", encoding="utf-8") as f:
        history = json.load(f)
    # print(type(history))
    for m in history:
        if isinstance(m, dict):
            st.session_state.messages.append(m)

# st.write(st.session_state)
st.write(st.secrets.PROBA)
st.write(df)

# TODO githubra felrakni és deployolni
#TODO kiolvasás megy az s3-ról, de hogy tudok oda írni?
# Talán ez segít:  https://discuss.streamlit.io/t/cannot-upload-streamlit-uploaded-file-to-s3-bucket/33376





st.title("Json együttműködés")




if user_input := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content":user_input})

    st.session_state.messages.append({"role": "assistant", "content":str("".join([c for c in user_input[::2]]))})
    with filepath.open("w", encoding="utf-8") as f:
        json.dump(st.session_state.messages, f)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

