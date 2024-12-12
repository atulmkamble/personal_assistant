from dotenv import load_dotenv
from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from loguru import logger
from personal_assistant_tools import personal_assistant_tools
from typing import Annotated
from typing_extensions import TypedDict
import os
load_dotenv()


class PersonalAssistantState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


class PersonalAssistant:
    def __init__(self):
        self.system_instruction = SystemMessage(content="""You are a helpful AI assistant. Provide clear, accurate, and concise answers to user queries. Use available tools when needed as per their descriptions.
If no function fits, use your knowledge to respond. However, always prefer to use the tools. If you can't answer, politely say so. Always maintain a friendly and professional tone.""")
        self.model = os.environ.get("MODEL_NAME")
        self.tools = personal_assistant_tools
        self.initialize_model()

    def initialize_model(self):
        if self.model == 'groq_llama':
            self.llm = ChatGroq(model='llama3-groq-70b-8192-tool-use-preview')
        else:
            self.llm = ChatOllama(model='llama3.1:8b', temperature=0)
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        logger.info(f'Using LLM: {self.llm.model}')

    def personal_assistant(self, state: PersonalAssistantState):
        return {'messages': [self.llm_with_tools.invoke([self.system_instruction] + state['messages'])]}

    def build_graph(self):
        # Build graph
        builder = StateGraph(PersonalAssistantState)

        # Add Nodes
        builder.add_node("personal_assistant", self.personal_assistant)
        builder.add_node("tools", ToolNode(self.tools))

        # Add Edges
        builder.add_edge(START, "personal_assistant")
        builder.add_conditional_edges(
            "personal_assistant",
            tools_condition,
        )
        builder.add_edge("tools", "personal_assistant")

        # Compile graph
        graph = builder.compile()
        return graph
