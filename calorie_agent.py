import json

from openai_client import OpenAIClient


class CalorieAgent(OpenAIClient):
    def __init__(self):
        super().__init__()
        self._prompt_role = \
"""아래 줄을 키로 하는 JSON 단일 아이템으로만 답변해줘. JSONB 키는 모두 소문자로 전환해줘.
NAME, CATEGORY, STANDARD, STANDARD_PER_SERVING, CALORIE, PRIMARY_NUTRITIONAL_COMPONENT
답변에는 질문한 음식만 포함시키고, 한국어로 답변해줘.
NAME: 음식의 이름을 넣어줘.
CATEGORY: 이 음식에 대한 식약처 기준의 식품의 분류를 넣어줘.

STANDARD: 만약 음식이 가공식품이라면 standard는 낱개 포장단위로 넣어줘. 
만약 음식이 과일이나 채소류라면 standard는 100g로 넣어줘.
만약 음식이 위에 기술한 분류에 속하지 않으면 1인분으로 넣어줘. 

STANDARD_PER_SERVING: 이 음식의 standard_per_serving을 넣어줘. 
만약 음식이 가공식품이라면 standard_per_serving 낱개 포장단위의 중량을 넣어줘.
만약 음식이 과일이나 채소류라면 standard_per_serving 100g로 넣어줘.
만약 음식이 위에 기술한 분류에 속하지 않으면 1인분당 제공 중량으로 넣어줘.

CALORIE: standard 칼로리를 넣어줘.

PRIMARY_NUTRITIONAL_COMPONENT: 음식에 대한 주성분을 넣어줘.
만약 두개 이상의 주성분이 있다면 쉼표로 구분해서 넣어줘.
"""
        self._food_image_url = None
        self._food_name = None

    def _get_prompt(self) -> str:
        if self._food_image_url:
            return "전달된 이미지를 보고 다음과 같이 답변해줘." + self._prompt_role
        else:
            return self._food_name + "에 대해 다음과 같이 답변해줘." + self._prompt_role

    @classmethod
    def _to_json(cls, result: str) -> str:
        return json.loads(result.replace("```", "").replace("json\n", ""))

    def get_calorie(self, food_name: str=None, food_image_url: str=None) -> str:
        self._food_name = food_name
        self._food_image_url = food_image_url
        prompt = self._get_prompt()
        return self._to_json(self.simple_question(prompt, image_url=self._food_image_url))
