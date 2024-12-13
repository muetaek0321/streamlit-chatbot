from pathlib import Path

import streamlit as st
import yaml
from streamlit_authenticator.utilities.hasher import Hasher

from modules.styles import HIDE_ST_STYLE
from modules.widgets import complate_signup_alert, error_dialog


# スタイルを適用
st.markdown(HIDE_ST_STYLE, unsafe_allow_html=True)

# 定数
AUTH_DIR_PATH = Path("./user")
AUTH_FILE_PATH = AUTH_DIR_PATH.joinpath("auth.yaml")
REQUIRED_MARK = "<span style='color: red'>*</span>"

st.title("新規ユーザ登録")

st.write("ユーザ名とパスワードを入力してください。")

with st.container(border=True):
    st.markdown(f"ユーザー名{REQUIRED_MARK}：", unsafe_allow_html=True)
    username = st.text_input(" ", label_visibility="collapsed", key="username_signup")
    st.markdown(f"パスワード{REQUIRED_MARK}：", unsafe_allow_html=True)
    password = st.text_input(" ", type='password', label_visibility="collapsed", key="password_signup")
    st.markdown(f"メールアドレス：", unsafe_allow_html=True)
    email = st.text_input(" ", label_visibility="collapsed", key="email")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("登録", use_container_width=True):
            # 認証データが書き込まれたファイルを読み込み
            with open(AUTH_FILE_PATH, mode="r") as f:
                yaml_data = yaml.safe_load(f)
                
                # ユーザデータが空の場合の対処
                if yaml_data["credentials"]["usernames"] is None:
                    yaml_data["credentials"]["usernames"] = dict()
            
            if (username == "") or (password == ""):
                # ユーザ名orパスワードの入力欄が空欄の場合
                error_dialog("ユーザ名およびパスワードの入力は必須です。")
            elif username in yaml_data["credentials"]["usernames"].keys():
                # 既に登録済みのユーザ名の場合
                error_dialog("登録済みのユーザ名と重複しています。<br>別のユーザ名で登録してください。")
            else:
                # パスワードをハッシュ化
                password_hashed = Hasher.hash(password)
                
                # 認証データファイルに書き込み
                yaml_data["credentials"]["usernames"][username] = {
                    "name": username,
                    "password": password_hashed,
                    "email": email
                }
                with open(AUTH_FILE_PATH, "w") as f:
                    yaml.dump(yaml_data, f)
                    
                # ユーザ専用の履歴フォルダを作成
                user_dir = AUTH_DIR_PATH.joinpath(username)
                user_dir.mkdir(exist_ok=True)
                    
                # トップ画面に戻る
                complate_signup_alert()

    with col2:
        if st.button("キャンセル", use_container_width=True):
            # 登録せずにトップページに戻る
            st.switch_page("./main.py")


