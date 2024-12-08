import os
os.environ["HF_HOME"] = "./pretrained" # 事前学習モデルの保存先指定

from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

# 定数
URLS = [
    "https://ja.wikipedia.org/wiki/%E3%82%A8%E3%83%AC%E3%83%95%E3%82%A1%E3%83%B3%E3%83%88%E3%82%AB%E3%82%B7%E3%83%9E%E3%82%B7",
    "https://ja.wikipedia.org/wiki/%E5%AE%AE%E6%9C%AC%E6%B5%A9%E6%AC%A1_(%E3%82%A8%E3%83%AC%E3%83%95%E3%82%A1%E3%83%B3%E3%83%88%E3%82%AB%E3%82%B7%E3%83%9E%E3%82%B7)",
    
]
TEMPLATE = """
あなたは質問応答のアシスタントです。質問に答えるために、検索された文脈の以下の部分を使用してください。
答えがわからない場合は、わからないと答えましょう。回答は2文以内で簡潔に。

質問: {question}
コンテキスト: {context}
答え:
"""


class JapaneseCharacterTextSplitter(RecursiveCharacterTextSplitter):
    """句読点も句切り文字に含めるようにするためのスプリッタ"""

    def __init__(self, **kwargs):
        separators = ["\n\n", "\n", "。", "、", " ", ""]
        super().__init__(separators=separators, **kwargs)


def main() -> None:
    # Webページの内容を知識として読み込み
    loader = UnstructuredURLLoader(urls=URLS)
    docs = loader.load()
    
    # 読込した内容を分割する
    text_splitter = JapaneseCharacterTextSplitter(chunk_size=200, chunk_overlap=40)
    docs = text_splitter.split_documents(docs)
    
    # ベクトル化する準備
    embedding = HuggingFaceEmbeddings(
        model_name="intfloat/multilingual-e5-base"
    )
    
    # 読込した内容を保存
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embedding,
        persist_directory="./chroma",
        collection_name="elephants"
    )
    
    query = "エレファントカシマシとはどんなバンドですか"

    # 検索する
    docs = vectorstore.similarity_search(query=query, k=5)

    # for index, doc in enumerate(docs):
    #     print("%d:" % (index + 1))
    #     print(doc.page_content)
        
    return query, docs


if __name__ == "__main__":
    query, docs = main()
    
    # モデルを準備
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    # プロンプトを設定
    prompt = PromptTemplate.from_template(TEMPLATE)
    # チェーンを準備
    rag_chain = (prompt | llm)
    
    # DBを読み込んで知識データ取得
    context = "\n".join([f"Content:\n{doc.page_content}" for doc in docs])
    
    # 返答を取得
    response = rag_chain.invoke({"question": query, "context": context}).content
    
    print(response)
    
    
