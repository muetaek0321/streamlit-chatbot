import time
import os
os.environ["HF_HOME"] = "./rag/pretrained" # 事前学習モデルの保存先指定

import streamlit as st
from markdown import Markdown
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings


# 定数
TEMPLATE = """
あなたは質問応答のアシスタントです。質問に答えるために、検索された文脈の以下の部分を使用してください。
答えがわからない場合は、わからないと答えましょう。

質問: {question}
コンテキスト: {context}
答え:
"""
DB_PATH = "./rag/chroma"

# AIの返答を作成
def gemini_rag_generator():        
    # モデルを準備
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-thinking-exp")
    # プロンプトを設定
    prompt = PromptTemplate.from_template(TEMPLATE)
    # チェーンを準備
    rag_chain = (prompt | llm)

    # 直前のユーザの入力を取得
    user_input = st.session_state.messages[-1]["content"]
    
    # ベクトル化する準備
    embedding = HuggingFaceEmbeddings(
        model_name="intfloat/multilingual-e5-base"
    )
    
    # DBを読み込んで知識データ取得
    vectorstore = Chroma(collection_name="elephants", persist_directory=DB_PATH, embedding_function=embedding)
    docs = vectorstore.similarity_search(query=user_input, k=5)
    context = "\n".join([f"Content:\n{doc.page_content}" for doc in docs])
    
    # 返答を取得
    response = rag_chain.invoke({"question": user_input, "context": context}).content
    
    # 返答を成形（makrddown -> HTML）
    response = Markdown().convert(response[1])
    
    for word in response.split():
        yield word + " "
        time.sleep(0.05)