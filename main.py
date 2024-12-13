from pathlib import Path

import streamlit as st

from modules.styles import HIDE_ST_STYLE
from modules.widgets import login_button


# 認証情報がある場合はリセット
if "authentication_status" in st.session_state:
    del st.session_state.authentication_status
if "messages" in st.session_state:
    del st.session_state.messages
    del st.session_state.chats
    

# スタイルを適用
st.markdown(HIDE_ST_STYLE, unsafe_allow_html=True)

st.title("素晴らしいチャットボット")

st.write("チャットを開始する！")
with st.container(border=True):
    st.markdown(f"ユーザー名：")
    username = st.text_input(" ", label_visibility="collapsed", key="username_login")
    st.markdown(f"パスワード：")
    password = st.text_input(" ", type='password', label_visibility="collapsed", key="password_login")

    # ログインボタン
    login_button(username, password)

st.divider()

col1, col2 = st.columns([2, 1])
with col1:
    st.write("ユーザ登録する！")
with col2:
    if st.button("新規登録", use_container_width=True):
        st.switch_page("./pages/signup.py")
    
