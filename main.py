from pathlib import Path

import streamlit as st
import yaml
from streamlit_authenticator.controllers import AuthenticationController

from modules.styles import HIDE_ST_STYLE
from modules.widgets import error_dialog


# 定数
AUTH_DIR_PATH = Path("./user")
AUTH_FILE_PATH = AUTH_DIR_PATH.joinpath("auth.yaml")

with open(AUTH_FILE_PATH, mode="r") as f:
    auth = yaml.safe_load(f)

auth_controller = AuthenticationController(auth['credentials'])

# 認証情報がある場合はリセット
if "authentication_status" in st.session_state:
    del st.session_state.authentication_status
if "messages" in st.session_state:
    del st.session_state.messages

# スタイルを適用
st.markdown(HIDE_ST_STYLE, unsafe_allow_html=True)

st.title("素晴らしいチャットボット")

st.write("チャットを開始する！")
with st.container(border=True):
    username = st.text_input("ユーザー名：")
    password = st.text_input("パスワード：", type='password')

    if st.button("ログイン", use_container_width=True):
        auth_ok = auth_controller.login(username, password)
        # ログイン成功
        if auth_ok:
            st.switch_page("./pages/chat.py")
        # ログイン失敗
        else:
            error_dialog("ユーザ名またはパスワードが間違っています。")

st.divider()

col1, col2 = st.columns([2, 1])
with col1:
    st.write("ユーザ登録する！")
with col2:
    if st.button("新規登録", use_container_width=True):
        st.switch_page("./pages/signup.py")
    
