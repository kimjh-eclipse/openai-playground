import array
from typing import Any

from openai.types.chat import ChatCompletion, ChatCompletionChunk

from settings.env import env_manager

from openai import OpenAI, Stream


class OpenAIClient:
    GPT_MODEL_4O = "gpt-4o"
    GPT_MODEL_4O_MINI = "gpt-4o-mini"
    GPT_MODEL_3_5_TURBO = "gpt-3.5-turbo"
    ROLE_USER = "user"
    ROLE_SYSTEM = "system"
    ROLE_ASSISTANT = "assistant"

    def __init__(self, openai_model=GPT_MODEL_4O_MINI):
        self._client = OpenAI(
            organization=env_manager.get("OPENAI_ORGANIZATION_ID"),
            project=env_manager.get("OPENAI_PROJECT_ID"),
            api_key=env_manager.get("OPENAI_API_KEY"),
        )
        self._model = openai_model
        self._prompt_tokens = 0
        self._completion_tokens = 0

    def get_token(self) -> int:
        return self._prompt_tokens + self._completion_tokens

    @classmethod
    def _get_message(cls, role: str, content: list) -> dict:
        return {
            "role": role,
            "content": content
        }

    @classmethod
    def _get_content(cls, content_type: str, content: dict) -> dict:
        return {
            "type": content_type,
            content_type: content
        }

    @classmethod
    def _get_text_content(cls, text: str) -> dict:
        return {
            "type": "text",
            "text": text
        }

    @classmethod
    def _get_image_url_content(cls, image_url: str) -> dict:
        return {
            "type": "image_url",
            "image_url": {
                "url": image_url
            }
        }

    @classmethod
    def _get_simple_question_messages(cls, question: str) -> array:
        return [{
            "role": cls.ROLE_USER,
            "content": [cls._get_text_content(question)]
        }]

    @classmethod
    def _get_simple_question_messages_with_image(cls, question: str, image_url: str) -> array:
        return [
            cls._get_message(cls.ROLE_USER, [
                cls._get_text_content(question),
                cls._get_image_url_content(image_url)
            ])
        ]

    def completions(self, messages: Any) -> ChatCompletion | None:
        try:
            response = self._client.chat.completions.create(
                messages=messages, model=self._model, temperature=0.0, n=1
            )
            self._prompt_tokens += response.usage.prompt_tokens
            self._completion_tokens += response.usage.completion_tokens
        except Exception as e:
            print(e)
            return None
        return response

    def simple_completion(self, messages: Any) -> str | None:
        result = self.completions(messages)
        if isinstance(result, ChatCompletion):
            return result.choices[0].message.content
        return None

    def simple_question_without_image(self, question: str) -> str | None:
        return self.simple_completion(self._get_simple_question_messages(question))

    def simple_question_with_image(self, question: str, image_url: str) -> str | None:
        return self.simple_completion(self._get_simple_question_messages_with_image(question, image_url))

    def simple_question(self, question: str, image_url: str=None) -> str | None:
        if image_url:
            return self.simple_question_with_image(question, image_url)
        return self.simple_question_without_image(question)
