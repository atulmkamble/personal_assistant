from personal_assistant import PersonalAssistant
from helper import execution_timer
from langchain_core.messages import HumanMessage
from loguru import logger
from langfuse.callback import CallbackHandler


class Orchestrator:
    def __init__(self):
        self.personal_assistant = PersonalAssistant().build_graph()
        self.langfuse_handler = CallbackHandler()

    @execution_timer
    def get_personal_assistant_response(self, user_query):
        response = self.personal_assistant.invoke(
            {'messages': HumanMessage(user_query)},
            config={'callbacks': [self.langfuse_handler]},
            stream_mode='values'
        )
        logger.info(response['messages'][-1].content)
        return response['messages'][-1].content
