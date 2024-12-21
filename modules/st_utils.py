import streamlit as st


__all__ = ["create_chat_title"]


def create_chat_title() -> None:
    """入力した初回にチャットタイトルを作成
    """
    if len(st.session_state.messages) > 0:
        # とりあえず最初のユーザの入力の頭の内容を取得するのみにする
        title_str = st.session_state.messages[0]["content"][:12]
        st.session_state.chats[st.session_state.current_chat]["title"] = title_str
        st.session_state.chat_title = title_str  
        st.rerun()

