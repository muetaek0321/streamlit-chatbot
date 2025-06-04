import asyncio
import time
import json

from markdown import Markdown
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_tool_calling_agent, AgentExecutor


# 定数
TEMPLATE = """
あなたは質問応答タスクのアシスタントです。
登録されているツールを使って質問に答えてください。

質問: {question}
答え: {agent_scratchpad}
"""
DB_PATH = "./rag/chroma"
MCP_CONFIG_PATH = "./data/mcp_config.json"

# AIの返答を作成
async def gemini_mcp_generator(user_input):        
    # モデルを準備
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    # プロンプトを設定
    prompt = PromptTemplate.from_template(TEMPLATE)

    # 直前のユーザの入力を取得
    # user_input = st.session_state.messages[-1]["content"]
    
    with open(MCP_CONFIG_PATH, mode="r") as f:
        mcp_config = json.load(f)
        
    # mcp_client = MultiServerMCPClient(mcp_config["mcpServers"])
    # async with mcp_client.session("fetch") as session:
    #    tools = await load_mcp_tools(session)
    
    mcp_client = MultiServerMCPClient(mcp_config["mcpServers"])
    tools = await mcp_client.get_tools()
    
    # エージェントを用意
    agent = create_tool_calling_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    
    # 返答を取得
    response = await executor.ainvoke({"question": user_input})

    # response = await llm.bind_tools(tools).ainvoke(user_input)
    # if isinstance(response.content, str):
    #     print("####", response.content)
    # elif isinstance(response.content, list):
    #     for content in response.content:
    #         if content["type"] == "text":
    #                 print(content["text"])

    # if response.tool_calls:
    #     for tool_call in response.tool_calls:
    #         selected_tool = {tool.name.lower(): tool for tool in tools}[
    #             tool_call["name"].lower()
    #         ]
    #         tool_msg = await selected_tool.ainvoke(tool_call)
    #         print(tool_msg.content)
    
    print(response["output"])
    
    # # 返答を成形（makrddown -> HTML）
    # response = Markdown().convert(response["output"])
    
    # for word in response.split():
    #     yield word + " "
    #     time.sleep(0.05)
    
    
if __name__ == "__main__":
    # 単体テスト
    MCP_CONFIG_PATH = "../data/mcp_config.json"
    
    # user_input = "エレファントカシマシについて教えてください"
    user_input = "https://www.elephantkashimashi.com/を参照して最新情報を取得してください。"
    # user_input = input("質問を入力 >>> ")
    
    asyncio.run(gemini_mcp_generator(user_input))