import os
import time

import streamlit as st
from markdown import Markdown
import google.generativeai as genai
import google.ai.generativelanguage_v1beta.types.content as content
from langchain_google_genai import ChatGoogleGenerativeAI


# AIの返答を作成
def gemini_rag_generator():    
    # # チャット履歴の形に変換
    # history = []
    # for chat_data in st.session_state.messages[:-1]:
    #     message = content.Content()
    #     message.parts.append({"text": chat_data["content"]})
    #     message.role = "model" if chat_data["role"] == "assistant" else chat_data["role"]
    #     history.append(message)
    
    # 返答を作成
    try:
        # モデルを準備
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    
        # 直前のユーザの入力を取得し、レスポンスを得る
        user_input = st.session_state.messages[-1]["content"]
        response = llm.invoke(user_input).content
        
        # 返答を成形（makrddown -> HTML）
        response = Markdown().convert(response)
    except Exception as e:
        # API側のエラーをキャッチして表示する
        response = f"<span style=\"color:#ff0000;\">{e}</span>"
    
    for word in response.split():
        yield word + " "
        time.sleep(0.05)