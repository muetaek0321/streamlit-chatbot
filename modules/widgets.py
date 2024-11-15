import streamlit as st


__all__ = ["delete_chat_dialog"]


@st.dialog("チャット削除")
def delete_chat_dialog(
    chat_num: int
) -> None:
    st.write(f"チャット{chat_num+1}を削除しますか？")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("OK", use_container_width=True):
            del st.session_state.chats[chat_num]
            st.rerun()
    with col2:
        if st.button("キャンセル", use_container_width=True):
            st.rerun()