from pathlib import Path

import streamlit as st
import yaml
from streamlit_authenticator.controllers import AuthenticationController


__all__ = ["delete_chat_dialog", "error_dialog", "complate_signup_alert"]

# 定数
AUTH_DIR_PATH = Path("./user")
AUTH_FILE_PATH = AUTH_DIR_PATH.joinpath("auth.yaml")

with open(AUTH_FILE_PATH, mode="r") as f:
    auth = yaml.safe_load(f)

auth_controller = AuthenticationController(auth['credentials'])


@st.dialog("チャット削除")
def delete_chat_dialog(
    chat_num: int
) -> None:
    st.write(f"チャット{chat_num+1}を削除しますか？")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("OK", use_container_width=True):
            # 指定のチャットを削除
            del st.session_state.chats[chat_num]
            st.rerun()
    with col2:
        if st.button("キャンセル", use_container_width=True):
            st.rerun()
            

@st.dialog("Error")
def error_dialog(
    error_msg: str
) -> None:
    """汎用のエラーダイアログ
    """
    st.write(error_msg, unsafe_allow_html=True)
    _, col2 = st.columns(2)
    with col2:
        if st.button("OK", use_container_width=True):
            st.rerun()


@st.dialog("ユーザ登録")
def complate_signup_alert() -> None:
    """ユーザ登録完了を知らせるアラート
    """
    st.write("ユーザ登録が完了しました。")
    _, col2 = st.columns(2)
    with col2:
        if st.button("OK", use_container_width=True):
            st.switch_page("./main.py")


def login_button(username: str, password: str) -> None:
    """ログインのボタン
    """
    if st.button("ログイン", use_container_width=True, type='primary'):
        auth_ok = auth_controller.login(username, password)
        # ログイン成功
        if auth_ok:
            st.switch_page("./pages/chat.py")
        # ログイン失敗
        else:
            error_dialog("ユーザ名またはパスワードが間違っています。")
 
            
@st.dialog("ログアウト")
def logout_dialog() -> None:
    """ログアウトの確認ダイアログ
    """
    st.write("ログアウトしますか？")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("OK", use_container_width=True):
            auth_controller.logout()
            st.switch_page("./main.py")
    with col2:
        if st.button("キャンセル", use_container_width=True):
            st.rerun()

