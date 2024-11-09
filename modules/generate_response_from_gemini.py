import os
import time

import streamlit as st
from markdown import Markdown
import google.generativeai as genai
import google.ai.generativelanguage_v1beta.types.content as content


# 定数
GEMINI_API_KEY = os.environ["GOOGLE_API_KEY"]


# AIの返答を作成
def response_generator():
    # APIキーを設定
    genai.configure(api_key=GEMINI_API_KEY)
    # モデルを準備
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # チャット履歴の形に変換
    history = []
    for chat_data in st.session_state.messages[:-1]:
        message = content.Content()
        message.parts.append({"text": chat_data["content"]})
        message.role = "model" if chat_data["role"] == "assistant" else chat_data["role"]
        history.append(message)
    
    # 返答を作成
    try:
        user_input = st.session_state.messages[-1]["content"]
        chat = model.start_chat(history=history)
        response = chat.send_message(user_input).text
        
        # 返答を成形（makrddown -> HTML）
        response = Markdown().convert(response)
    except Exception as e:
        # API側のエラーをキャッチして表示する
        response = f"<span style=\"color:#ff0000;\">{e}</span>"
    
    for word in response.split():
        yield word + " "
        time.sleep(0.05)