import json

from calorie_agent import CalorieAgent
from news_bot_with_prompt_role import NewBot
from openai_client import OpenAIClient


def test_openai_client():
    openai_client = OpenAIClient()
    answer = openai_client.simple_question("오늘의 날씨는 어떤가요?")
    print(answer)
    print("Total tokens:", openai_client.get_token())

def test_news_bot():
    news_bot = NewBot()
    answer = news_bot.assist_journalist(["오늘은 미세먼지가 많음", "날씨가 따뜻함"], "따뜻하게", "100자", "블로그")
    print(answer)

def test_news_bot2():
    news_bot = NewBot()
    answer2 = news_bot.simple_journalist(["오늘은 미세먼지가 많음", "날씨가 따뜻함"])
    print(answer2)

def test_calorie_agent():
    calorie_agent = CalorieAgent()
    # answer = calorie_agent.get_calorie(image_url="https://acl-deploy.s3.ap-northeast-2.amazonaws.com/local/file/food/japcha2.jpeg")
    # answer = calorie_agent.get_calorie(image_url="https://acl-deploy.s3.ap-northeast-2.amazonaws.com/local/file/food/plate.jpeg")
    # answer = calorie_agent.get_calorie(image_url="https://sitem.ssgcdn.com/47/82/92/item/1000047928247_i2_750.jpg")
    # answer = calorie_agent.get_calorie(image_url="https://acl-deploy.s3.ap-northeast-2.amazonaws.com/local/file/food/japcha2.jpeg")
    answer = calorie_agent.get_calorie(food_name="밥")
    print(answer)

# test_openai_client()
# test_news_bot()
# test_news_bot2()
test_calorie_agent()
