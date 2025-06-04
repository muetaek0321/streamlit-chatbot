import os
import time
import traceback

import streamlit as st
from markdown import Markdown
import google.generativeai as genai
import google.ai.generativelanguage_v1beta.types.content as content


# 定数
GEMINI_API_KEY = os.environ["GOOGLE_API_KEY"]


# AIの返答を作成
def gemini_generator(
    user_input: str
):    
    # 返答を作成
    try:
        # APIキーを設定
        genai.configure(api_key=GEMINI_API_KEY)
        # モデルを準備
        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash-preview-04-17',
            system_instruction="あなたはエレファントカシマシについて答えるアシスタントです。"
        )
        
        # チャット履歴の形に変換
        history = []
        for chat_data in st.session_state.messages[:-1]:
            message = content.Content()
            message.parts.append({"text": chat_data["content"]})
            message.role = "model" if chat_data["role"] == "assistant" else chat_data["role"]
            history.append(message)
        
        # 直前のユーザの入力を取得し、レスポンスを得る
        chat = model.start_chat(history=history)
        response = chat.send_message(user_input).text
        
        # 返答を成形（makrddown -> HTML）
        response = Markdown().convert(response)
    except Exception:
        # API側のエラーをキャッチして表示する
        response = f"<span style=\"color:#ff0000;\">{traceback.format_exc()}</span>"
    
    for word in response.split():
        yield word + " "
        time.sleep(0.05)