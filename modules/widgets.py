import json
from pathlib import Path

import streamlit as st


__all__ = ["delete_chat_dialog", "error_dialog", "complate_signup_alert"]


@st.dialog("チャット削除")
def delete_chat_dialog(
    chat_num: int,
    json_path: Path
) -> None:
    st.write(f"チャット{chat_num+1}を削除しますか？")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("OK", use_container_width=True):
            with open(json_path, mode="r", encoding="utf-8") as f:
                chat_history = json.load(f)
                del chat_history[chat_num]
            
            st.session_state.chats = chat_history
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
    st.write(error_msg)
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