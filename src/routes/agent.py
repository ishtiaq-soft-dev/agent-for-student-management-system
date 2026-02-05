from langchain_groq.chat_models import ChatGroq
from langchain.agents import create_agent
from .tools import list_of_tools
import os


def initialize_agent():
    groq_api_key = os.getenv("GROQ_API_KEY")


    llm = ChatGroq(
        api_key=groq_api_key,
        model="openai/gpt-oss-120b",
        temperature=0.7,
    )

    agent = create_agent(
        model=llm,
        tools=list_of_tools,
        system_prompt="You are a helpful assistant that manages student information. You can create, update, delete, and retrieve student records. Always format responses with tables and emojis for better clarity."
        )
    
    return agent
