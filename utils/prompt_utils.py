class PromptUtility:
    def __init__(self, prompt_style=">>", username=""):
        self.prompt = username + prompt_style

    def message_print(self, msg):
        print(f"{self.prompt}{msg}")
