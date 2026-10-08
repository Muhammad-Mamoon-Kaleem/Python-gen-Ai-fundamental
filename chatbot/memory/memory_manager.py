from llm import get_llm
import json
from langchain_core.messages import SystemMessage, HumanMessage
from prompts.memory_manager_prompt import MEMORY_MANAGER_PROMPT

class MemoryManager:
    def __init__(self):
        self.llm = get_llm()

    def analyze(self,message):
        response = self.llm.invoke([
            SystemMessage(content=MEMORY_MANAGER_PROMPT),
            HumanMessage(content=message)
        ])

        try:
            result = json.loads(response.content)
            return result
        except Exception:
            return {
                "action":"none",
            }
