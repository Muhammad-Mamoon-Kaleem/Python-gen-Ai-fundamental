from prompts.system_prompt import BASE_SYSTEM_PROMPT


class PromptBuilder:

    def build(
        self,
        chat_memory,
        profile_memory,
        context_memory,
    ):

        sections = [
            BASE_SYSTEM_PROMPT,
            self._build_chat_settings(chat_memory),
            self._build_profile(profile_memory),
            self._build_context(context_memory),
            self._build_instructions(),
        ]

        return "\n\n".join(
            section.strip()
            for section in sections
            if section.strip()
        )

    # -------------------------------------------------
    # Chat Settings
    # -------------------------------------------------

    def _build_chat_settings(self, chat_memory):

        settings = chat_memory.get_all()

        return f"""
======== CURRENT CHAT SETTINGS ========

Language: {settings.get("language", "english")}
Role: {settings.get("role", "assistant")}
Response Style: {settings.get("response_style", "friendly")}
Difficulty: {settings.get("difficulty", "normal")}
Output Format: {settings.get("output_format", "text")}
"""

    # -------------------------------------------------
    # User Profile
    # -------------------------------------------------

    def _build_profile(self, profile_memory):

        profile = profile_memory.get_all_profile()

        if not profile:
            return ""

        lines = []

        for key, value in profile.items():

            if value not in [None, "", [], {}]:
                lines.append(f"{key}: {value}")

        if not lines:
            return ""

        return (
            "======== USER PROFILE ========\n\n"
            + "\n".join(lines)
        )

    # -------------------------------------------------
    # Current Context
    # -------------------------------------------------

    def _build_context(self, context_memory):

        context = context_memory.get_all()

        lines = []

        for key, value in context.items():

            if value not in [None, "", [], {}]:
                lines.append(f"{key}: {value}")

        if not lines:
            return ""

        return (
            "======== CURRENT CONTEXT ========\n\n"
            + "\n".join(lines)
        )

    # -------------------------------------------------
    # Instructions
    # -------------------------------------------------

    def _build_instructions(self):

        return """
======== IMPORTANT INSTRUCTIONS ========

• Always respect the user's current chat settings.

• Use the user profile only when it is relevant.

• Use the current context to understand what the user is currently working on.

• If profile or context information is missing, do not invent it.

• If the user changes their preferences, follow the latest settings.
"""
