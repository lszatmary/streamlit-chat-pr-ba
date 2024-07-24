import json
from pathlib import Path

import streamlit as st
import boto3

def erase_messages():
    st.session_state.messages = []
    upload_file_to_s3()

def upload_file_to_s3():
    s3.put_object(Body=json.dumps(st.session_state.messages).encode('UTF-8'),   #, encoding="utf-8"
                  Bucket=bucket_name,
                  Key=bucket_key,
                  ContentType='application/json'
                  )


file_name = "history_proba.json"
bucket_name = "lsz-streamlit-chat-proba-bucket-1"
bucket_key = "/".join(("chat_proba_1", file_name))
filepath = Path(file_name)

s3 = boto3.client(
        service_name='s3',
        region_name=st.secrets.AWS_DEFAULT_REGION,
        aws_access_key_id=st.secrets.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=st.secrets.AWS_SECRET_ACCESS_KEY,
    )

st.title("Json írás-olvasás s3-on")

st.button("Session state törlése", on_click=erase_messages)

if "messages" not in st.session_state:
    st.session_state.messages = []
    response = s3.get_object(Bucket=bucket_name, Key=bucket_key)
    messages = json.loads(response["Body"].read().decode("utf-8"))
    st.write(messages)
    for m in messages:
        if isinstance(m, dict):
            st.session_state.messages.append(m)

if user_input := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content":user_input})
    st.session_state.messages.append({"role": "assistant", "content":str("".join([c for c in user_input[::2]]))})

    upload_file_to_s3()


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

