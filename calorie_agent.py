import json

from openai_client import OpenAIClient


class CalorieAgent(OpenAIClient):
    PROMPT_IMAGE_INPUT_HEADER = \
        """전달 받은 이미지의 모든 음식을 인식하여, 아래 줄을 키로 하는 JSON 리스트 아이템으로 답변해줘.
답변에는 질문한 음식만 포함시키고, 한국어로 답변해줘. 
답변에는 다른 설명은 달지 말고, 오직 JSON형식으로만 답변해야 해. 
JSON 키는 모두 소문자로 전환해줘."""
    PROMPT_TEXT_INPUT_HEADER = "의 음식 정보를 알려줘. 아래 줄의 형식으로 답변해줘."
    PROMPT_COMMON_HEADER = \
"""너는 최고의 한국인 영양사야. 한국어로 답변해줘. 답변에는 오직 JSON형식으로만 답변해야 해.
아래 줄을 키로 하는 JSON 리스트 아이템으로만 답변해줘. JSON 키는 모두 소문자로 전환해줘.

JSON 키는 아래와 같아."""
    RESPONSE_JSON = {
            "name": "음식의 이름을 넣어줘. 만약 오타가 감지되면, 수정해줘.",
            "category": "이 음식에 대한 식약처 기준의 식품의 분류를 넣어줘.",
            "standard": """만약 음식이 가공식품이라면 standard는 낱개 포장단위로 넣어줘. 
만약 음식이 과일이나 채소류라면 standard는 100g로 넣어줘.
만약 음식이 위에 기술한 분류에 속하지 않으면 1인분으로 넣어줘. """,
        "standard_per_serving": """음식의 standard_per_serving을 넣어줘. 
만약 음식이 가공식품이라면 standard_per_serving 낱개 포장단위의 중량을 넣어줘.
만약 음식이 과일이나 채소류라면 standard_per_serving 100g로 넣어줘.
만약 음식이 위에 기술한 분류에 속하지 않으면 1인분당 제공 중량으로 넣어줘.""",
        "calorie": "단위는 빼고 숫자만 standard 칼로리를 넣어줘.",
        "primary_nutritional_component": """음식에 대한 주성분을 넣어줘.
만약 두개 이상의 주성분이 있다면 쉼표로 구분해서 넣어줘.""",
        "position_left_top": "음식의 이미지에서 픽셀 기준으로 음식의 이미지의 왼쪽 상단 위치를 넣어줘.",
        "position_right_buttom": "음식의 이미지에서 픽셀 기준으로 음식의 이미지의 오른쪽 하단 위치를 넣어줘."
    }
    def __init__(self, openai_model=OpenAIClient.GPT_MODEL_4O_MINI):
        super().__init__(openai_model)
        self._food_image_url = None
        self._food_name = None

    def _get_prompt(self) -> str:
        if self._food_image_url:
            prompt = self.PROMPT_IMAGE_INPUT_HEADER
        else:
            prompt = self._food_name + self.PROMPT_TEXT_INPUT_HEADER
        prompt += self.PROMPT_COMMON_HEADER
        prompt += ", ".join(self.RESPONSE_JSON.keys())
        prompt += "각 JSON 키에 대한 설명은 다음과 같아.\n"
        prompt += "\n".join([f"{key}: {value}" for key, value in self.RESPONSE_JSON.items()])
        return prompt

    @classmethod
    def _get_recommend_prompt(cls, lunch: list) -> str:
        prompt = "난 50대 여성이고, 무릎 관절염을 앓고 있어, 키는 160Cm이고 몸무게는 60Kg이야. 관절염을 치료하기 위해서 식단 조절이 필요해."
        prompt += "\n점심으로 먹은 음식은 아래와 같아."
        foods = [food["name"] for food in lunch]
        prompt += "\n"
        prompt += ', '.join(foods)
        prompt += "\n"
        prompt += "점심으로 먹은 음식을 기준으로, 저녁으로 먹을 음식을 추천하는 이유와 추천메뉴를 150자 이내로 알려줘."
        return prompt

    @classmethod
    def _to_json(cls, result: str) -> list:
        return json.loads(result.replace("```", "").replace("json\n", ""))

    def get_calorie(self, food_name: str=None, food_image_url: str=None) -> list:
        self._food_name = food_name
        self._food_image_url = food_image_url
        prompt = self._get_prompt()
        print(prompt)
        answer = self.simple_question(prompt, image_url=self._food_image_url)
        print(answer)
        return self._to_json(answer)

    def get_recommend_dinner(self, food_name: str=None, food_image_url: str=None) -> str:
        lunch: list = self.get_calorie(food_name=food_name, food_image_url=food_image_url)
        return self.simple_question(self._get_recommend_prompt(lunch))
