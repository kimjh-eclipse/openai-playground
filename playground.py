from calorie_agent import CalorieAgent
from news_bot_with_prompt_role import NewBot
from openai_client import OpenAIClient

def test_openai_client():
    # OpenAIClient 인스턴스를 생성하고 간단한 질문을 던져 응답을 출력합니다.
    openai_client = OpenAIClient()
    answer = openai_client.simple_question("오늘의 날씨는 어떤가요?")
    print(answer)
    print("Total tokens:", openai_client.get_token())

def test_news_bot():
    # NewBot 인스턴스를 생성하고 assist_journalist 메서드를 호출하여 응답을 출력합니다.
    news_bot = NewBot()
    answer = news_bot.assist_journalist(["오늘은 미세먼지가 많음", "날씨가 따뜻함"], "따뜻하게", "100자", "블로그")
    print(answer)

def test_news_bot2():
    # NewBot 인스턴스를 생성하고 simple_journalist 메서드를 호출하여 응답을 출력합니다.
    news_bot = NewBot()
    answer2 = news_bot.simple_journalist(["오늘은 미세먼지가 많음", "날씨가 따뜻함"])
    print(answer2)

def test_calorie_agent():
    # CalorieAgent 인스턴스를 생성하고 get_calorie 메서드를 호출하여 응답을 출력합니다.
    # 다양한 음식 이미지 URL을 주석 처리하여 테스트할 수 있습니다.
    calorie_agent = CalorieAgent()
    # answer = calorie_agent.get_calorie(food_image_url="https://acl-deploy.s3.ap-northeast-2.amazonaws.com/local/file/food/japcha2.jpeg")
    # answer = calorie_agent.get_calorie(food_image_url="https://acl-deploy.s3.ap-northeast-2.amazonaws.com/local/file/food/plate.jpeg")
    # answer = calorie_agent.get_calorie(food_image_url="https://acl-deploy.s3.ap-northeast-2.amazonaws.com/local/file/food/lunch3.jpg")
    # answer = calorie_agent.get_calorie(food_image_url="https://acl-deploy.s3.ap-northeast-2.amazonaws.com/local/file/food/lunch9.jpg")
    # answer = calorie_agent.get_calorie(food_image_url="https://acl-deploy.s3.ap-northeast-2.amazonaws.com/local/file/food/japcha2.jpeg")
    answer = calorie_agent.get_calorie(food_name="김치찌게")
    # answer = calorie_agent.get_recommend_dinner(food_image_url="https://acl-deploy.s3.ap-northeast-2.amazonaws.com/local/file/food/lunch3.jpg")
    print(answer)

# test_openai_client()
# test_news_bot()
# test_news_bot2()
test_calorie_agent()