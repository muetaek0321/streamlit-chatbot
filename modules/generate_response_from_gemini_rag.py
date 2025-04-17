import time
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
os.environ["HF_HOME"] = "./pretrained" # 事前学習モデルの保存先指定

import streamlit as st
from markdown import Markdown
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_chroma import Chroma
from langchain.embeddings import HuggingFaceEmbeddings


# 定数
TEMPLATE = """
あなたは質問応答タスクのアシスタントです。
検索された以下のコンテキストの一部を使って質問に丁寧に答えてください。
答えがわからなければ、わからないと答えてください。

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
    
    # # 会話履歴のデータを作成
    # history = ""
    # for message in st.session_state.messages[:-1]:
    #     history += f"{message['role'].capitalize()}: {message['content']}\n"
    
    # ベクトル化する準備
    model_kwargs = {"device": "cuda", "trust_remote_code": True}
    embedding = HuggingFaceEmbeddings(
        model_name="pfnet/plamo-embedding-1b",
        model_kwargs=model_kwargs
    )
    
    # DBを読み込んで知識データ取得
    vectorstore = Chroma(collection_name="elephants", 
                         persist_directory=DB_PATH, 
                         embedding_function=embedding)
    docs = vectorstore.similarity_search(query=user_input, k=10)
    context = "\n".join([f"Content:\n{doc.page_content}" for doc in docs])
    
    # 返答を取得
    response = rag_chain.invoke({
        "question": user_input, 
        "context": context
    }).content
    
    # 返答を成形（makrddown -> HTML）
    response = Markdown().convert(response)
    
    for word in response.split():
        yield word + " "
        time.sleep(0.05)