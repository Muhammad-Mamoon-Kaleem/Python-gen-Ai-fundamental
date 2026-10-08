class CurrentChatMemory:
    def __init__(self):
        self.setting = {
            "language": "english",
            "response_style": "friendly",
            "role": "assistant",
            "difficulty": "normal",
            "output_format": "text",
        }

    def get(self, key):
        return self.setting.get(key)

    def set(self, key, value):
        self.setting[key] = value

    def get_all(self):
        return self.setting

    def clear(self):
        self.setting = {
            "language": "english",
            "response_style": "friendly",
            "role": "assistant",
            "difficulty": "normal",
            "output_format": "text",
        }
