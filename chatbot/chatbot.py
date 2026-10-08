from llm import get_llm

from memory.conversation_memory import ConversationMemory
from memory.current_chat import CurrentChatMemory
from memory.memory_manager import MemoryManager
from prompts import PromptBuilder
from memory.profile_memory import ProfileMemory
from memory.current_context import CurrentContextMemory

from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)

llm = get_llm()

conversation_memory = ConversationMemory()
chat_memory = CurrentChatMemory()
profile_memory = ProfileMemory()
context_memory = CurrentContextMemory()
memory_manager = MemoryManager()
prompt_builder = PromptBuilder()


def chat_with_ai(user_input: str):

    # -------------------------
    # Step 1
    # Analyze user message
    # -------------------------

    decision = memory_manager.analyze(user_input)

    # -------------------------
    # Step 2
    # Update memories
    # -------------------------

    if decision["action"] == "update":

        if decision["memory_type"] == "chat":

            updates = decision["updates"]

            for key, value in updates.items():
                chat_memory.set(key, value)

            print("\n[Chat Memory Updated]")
            print(chat_memory.get_all())

        if decision["memory_type"] == "profile":
            updates = decision["updates"]

            for key, value in updates.items():
                profile_memory.set_profile(key, value)

            print("\n[Profile Memory Updated]")
            print(profile_memory.get_all_profile())

        if decision["memory_type"] == "context":
            updates = decision["updates"]

            for key, value in updates.items():
                context_memory.set(key, value)

            print("\n[Context Memory Updated]")
            print(context_memory.get_all())
    # -------------------------
    # Step 3
    # Build system prompt
    # -------------------------

    system_prompt = prompt_builder.build(chat_memory, profile_memory, context_memory)

    # -------------------------
    # Step 4
    # Collect conversation history
    # -------------------------

    messages = [
        SystemMessage(content=system_prompt)
    ]

    messages.extend(conversation_memory.get_messages())

    messages.append(
        HumanMessage(content=user_input)
    )

    # -------------------------
    # Step 5
    # Ask LLM
    # -------------------------

    response = llm.invoke(messages)

    # -------------------------
    # Step 6
    # Save history
    # -------------------------

    conversation_memory.add_user_message(user_input)

    conversation_memory.add_ai_message(
        response.content
    )

    return response.content
