from langchain_core.messages import SystemMessage, HumanMessage,AIMessage
from prompts import SYSTEM_PROMPT

class ConversationMemory:
    def __init__(self):
        self.messages = [SystemMessage(content=SYSTEM_PROMPT)]

    def add_user_message(self,user_input):
        self.messages.append(HumanMessage(content=user_input))

    def add_ai_message(self, ai_response):
        self.messages.append(AIMessage(content=ai_response))

    def get_conversation(self):
        return self.messages

    def clear_conversation(self):
        self.messages = [SystemMessage(content=SYSTEM_PROMPT)]
