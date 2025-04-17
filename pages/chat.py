import json
from pathlib import Path

import streamlit as st
from PIL import Image
import torch

from modules.styles import HIDE_ST_STYLE, HIDE_IMG_FS
from modules.widgets import delete_chat_dialog, logout_dialog
from modules.st_utils import *
from modules.number_links import response_add_info
from modules.generate_response_from_gemini_api import gemini_generator
from modules.generate_response_from_gemini_rag import gemini_rag_generator
from modules.generate_response_from_gemma2_baku import gemma2_baku_generator


# 定数
AUTH_DIR_PATH = Path("./user")
JSON_FILE_NAME = "chat_history.json"

# スタイルを適用
st.markdown(HIDE_ST_STYLE, unsafe_allow_html=True)
st.markdown(HIDE_IMG_FS, unsafe_allow_html=True)

# 認証済みでない場合はトップページにリダイレクト
if "authentication_status" not in st.session_state:
    st.switch_page("./main.py")

## ユーザごとチャット履歴のパス
USER_DIR_PATH = AUTH_DIR_PATH.joinpath(st.session_state.username)
if not USER_DIR_PATH.is_dir():
    # 何らかの問題でユーザフォルダが無い場合に新規作成
    USER_DIR_PATH.mkdir(parents=True, exist_ok=True)
    USER_DIR_PATH.joinpath(".gitkeep").touch()
USER_JSON_PATH = USER_DIR_PATH.joinpath(JSON_FILE_NAME)

# 初回の処理
if "messages" not in st.session_state:
    if USER_JSON_PATH.is_file():
        with open(USER_JSON_PATH, mode="r", encoding="utf-8") as f:
            st.session_state.chats = json.load(f)
        if len(st.session_state.chats) == 0:
            st.session_state.chats.append({"title": "new chat", "messages": []})
    else:
        st.session_state.chats = [{"title": "new chat", "messages": []}]
    
    # 初回は一番上のチャット（チャット1）の選択状態
    st.session_state.current_chat = 0
    st.session_state.chat_title = st.session_state.chats[0]["title"]
    st.session_state.messages = st.session_state.chats[0]["messages"]
    
    # 初回はユーザの入力待ち状態に設定
    st.session_state.current_role = "user"
    
    # 返答生成モジュールの設定
    st.session_state.mode_select = ["Gemini", "Gemini_RAG"]
    st.session_state.generator = {
        "Gemini": gemini_generator, 
        "Gemini_RAG": gemini_rag_generator
    }
    if torch.cuda.is_available():
        # GPU環境でCUDAが使用できる場合
        st.session_state.mode_select += ["Gemma2_baku"]
        generator_cuda = {
            "Gemma2_baku": gemma2_baku_generator
        }
        st.session_state.generator = st.session_state.generator | generator_cuda
        
    # responseモードの指定（初回はGemini対話モード）
    st.session_state.respose_mode = "Gemini"
    
# チャット一覧を表示するサイドバー
with st.sidebar:
    # ロゴの表示
    logo_img = Image.open("./data/chatbot_logo.png")
    st.image(logo_img)
    
    st.divider() # 区切り線
    
    # レスポンスを返す関数を指定するプルダウン
    st.session_state.respose_mode = st.selectbox("チャットモード選択：", st.session_state.mode_select)
    
    st.divider() # 区切り線

    # チャットを追加するボタン
    if st.button("新しいチャット", icon=":material/chat_bubble:", use_container_width=True):
        st.session_state.chats.append({"title": "new chat", "messages": []})
        st.session_state.chat_title = st.session_state.chats[-1]["title"]
        st.session_state.messages = st.session_state.chats[-1]["messages"]
    
    with st.container(height=320):
        # スクロール可能なウィジェットを配置
        for chat_num in range(len(st.session_state.chats)):
            col1, col2 = st.columns([3, 1])
            with col1:
                chat_data = st.session_state.chats[chat_num]
                if st.button(f"{chat_data['title'][:8]}…", use_container_width=True, key=f"chat{chat_num+1}"):
                    st.session_state.current_chat = chat_num
                    st.session_state.chat_title = chat_data["title"]
                    st.session_state.messages = chat_data["messages"]
                    
            with col2:
                if st.button("", icon=":material/delete:", use_container_width=True, key=f"chat{chat_num+1}_del"):
                    delete_chat_dialog(chat_num)
    
    st.divider() # 区切り線          
    if st.button("ログアウト", use_container_width=True, type='primary'):
        logout_dialog()

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
        
        # 選択中のチャットモードによって返答するresponse_generatorを切り替え
        for res in st.session_state.generator[st.session_state.respose_mode]():
            response += res
            res_container.markdown(response, unsafe_allow_html=True)
            
        # 追加情報を付与
        add_info_text = response_add_info(response)
    
        # AIの返答を履歴に保存
        st.session_state.messages.append({"role": "assistant", "content": response+add_info_text})
        
        # ユーザの入力待ち状態に切り替え
        st.session_state.current_role = "user"

# 初回はタイトル生成
if (st.session_state.chat_title == "new chat") and (len(st.session_state.messages) == 2):
    create_chat_title()

# 履歴の保存
with open(USER_JSON_PATH, mode="w", encoding="utf-8") as f:
        json.dump(st.session_state.chats, f, indent=2)
        