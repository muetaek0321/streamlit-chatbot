import asyncio
import time
import json
from typing import Generator

from markdown import Markdown
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_tool_calling_agent, AgentExecutor


# 定数
TEMPLATE = """
あなたは質問応答タスクのアシスタントです。
登録されているツールを使って質問に答えてください。

質問: {question}
答え: {agent_scratchpad}
"""
MCP_CONFIG_PATH = "./data/mcp_config.json"


def gemini_mcp_generator(
    user_input: str
) -> Generator:
    """AIが作成した返答をstreamで返す関数
    """
    response = asyncio.run(create_gemini_mcp_response(user_input))
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


# AIの返答を作成
async def create_gemini_mcp_response(
    user_input: str
) -> str:        
    # モデルを準備
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    # プロンプトを設定
    prompt = PromptTemplate.from_template(TEMPLATE)
    
    # MCPサーバの設定を読み込み
    with open(MCP_CONFIG_PATH, mode="r") as f:
        mcp_config = json.load(f)
    
    # ツール化
    mcp_client = MultiServerMCPClient(mcp_config["mcpServers"])
    tools = await mcp_client.get_tools()
    
    # エージェントを用意
    agent = create_tool_calling_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    
    # 返答を取得
    response = await executor.ainvoke({"question": user_input})
    
    # 返答を成形（makrddown -> HTML）
    response = Markdown().convert(response["output"])
    
    return response
    
