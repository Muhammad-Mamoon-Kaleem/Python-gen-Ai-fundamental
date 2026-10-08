from chatbot import chat_with_ai

print("Welcome to the AI Chatbot! Type 'exit' or 'quit' to end the conversation.")

while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        print("Existing the chatbot. Goodbye!")
        break
    else:
        response = chat_with_ai(user_input)
        print("AI:", response)
