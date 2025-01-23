from openai_client import OpenAIClient


class NewBot(OpenAIClient):
    def __init__(self):
        super().__init__()
        self._prompt_role = "너는 저널리스트야. 너의 임무는 주어진 FACT 대로 뉴스를 쓰는 것이야. 너는 TONE과 LENGTH, STYLE의 지시에 맞춰야 해."

    def assist_journalist(self
                          , facts: list[str]
                          , tone: str
                          , length: str
                          , style: str) -> str:
        instruction = f"""FACT: {facts}
TONE: {tone}
LENGTH: {length}
STYLE: {style}"""
        return self.simple_question(self._prompt_role + instruction)

    def simple_journalist(self, facts: list[str]) -> str:
        return self.assist_journalist(
            facts=facts,
            tone="공손히",
            length="100자",
            style="뉴스"
        )
