

class ProfileMemory:
    def __init__(self):
        self.profile_data = {}

    def set_profile(self, key: str, value: str):
        self.profile_data[key] = value

    def get_profile(self, key: str):
        return self.profile_data.get(key, "")

    def get_all_profile(self):
        return self.profile_data

    def clear_profile(self):
        self.profile_data = {}
