from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from dotenv import load_dotenv

from tools.sql import run_query_tool, list_tables

load_dotenv()

chat = ChatOpenAI(model="gpt-4")

tables = list_tables()
prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(content=f"You are an AI that has access to SQLite, tables: {tables}"),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)

tools = [run_query_tool]

agent = OpenAIFunctionsAgent(
    llm=chat,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools
)

result = agent_executor("Who is the first user?")
print(result["output"])
