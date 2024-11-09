import json
from pathlib import Path

import streamlit as st

from modules.styles import HIDE_ST_STYLE
from modules.widgets import *
# from modules.generate_response_from_gemini import response_generator
from modules.generate_response_from_chain import response_generator


# 定数
JSON_PATH = Path("chat_history.json")


# スタイルを適用
st.markdown(HIDE_ST_STYLE, unsafe_allow_html=True)
    

# 初回の処理
if "messages" not in st.session_state:
    if JSON_PATH.is_file():
        with open(JSON_PATH, mode="r", encoding="utf-8") as f:
            st.session_state.chats = json.load(f)
    else:
        st.session_state.chats = [[]]
    
    # 初回は一番上のチャット（チャット1）の選択状態
    st.session_state.current_chat = 0
    st.session_state.messages = st.session_state.chats[0]
    st.session_state.chat_title = "チャット1"
    
    # 初回はユーザの入力待ち状態に設定
    st.session_state.current_role = "user"
    
# チャット一覧を表示するサイドバー
with st.sidebar:
    if st.button("新しいチャット", use_container_width=True, type='primary'):
        st.session_state.chats.append([])
        st.session_state.messages = st.session_state.chats[-1]
        st.session_state.chat_title = f"チャット{len(st.session_state.chats)}"
    
    for chat_num in range(len(st.session_state.chats)):
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button(f"チャット{chat_num+1}", use_container_width=True, key=f"chat{chat_num+1}"):
                st.session_state.current_chat = chat_num
                st.session_state.messages = st.session_state.chats[chat_num]
                st.session_state.chat_title = f"チャット{chat_num+1}"
        with col2:
            if st.button("", icon=":material/delete:", use_container_width=True, key=f"chat{chat_num+1}_del"):
                delete_chat_dialog(chat_num=chat_num)
            
st.title(st.session_state.chat_title)

# 対話内容の表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

if st.session_state.current_role == "user":
    # ユーザが入力するテキストボックス
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # ユーザの入力を履歴に保存
        st.session_state.messages.append({"role": "user", "content": prompt})
        # AIの返答待ち状態に切り替え
        st.session_state.current_role = "assistant"

if st.session_state.current_role == "assistant":
    with st.chat_message("assistant"):
        response = ""
        res_container = st.empty()
        for res in response_generator():
            response += res
            res_container.markdown(response, unsafe_allow_html=True)
        
        # AIの返答を履歴に保存
        st.session_state.messages.append({"role": "assistant", "content": response})
        # ユーザの入力待ち状態に切り替え
        st.session_state.current_role = "user"

with open(JSON_PATH, mode="w", encoding="utf-8") as f:
        json.dump(st.session_state.chats, f, indent=2)
    