from typing import Any, Literal, TypedDict

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientError


class CompletionOptions(TypedDict):
    stream: bool
    temperature: float
    maxTokens: str


class Message(TypedDict):
    role: Literal["system", "user"]
    text: str


class YaGPTPrompt(TypedDict):
    modelUri: str
    completionOptions: CompletionOptions
    messages: list[Message]


class GPTError(Exception):
    def __init__(self, *args: list[Any], text: str) -> None:
        super().__init__(*args)
        self.text = text

    def __str__(self) -> str:
        return f"API response: {self.text}"


API_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"


class YandexGPT:
    __slots__ = (
        "api_key",
        "folder_id",
        "http_session",
        "max_tokens",
        "model",
        "system_prompt",
        "temperature",
    )

    def __init__(
        self,
        http_session: ClientSession,
        api_key: str,
        folder_id: str,
        temperature: float = 0.6,
        max_tokens: int = 1024,
        model: Literal["yandexgpt", "yandexgpt-lite"] = "yandexgpt-lite",
        system_prompt: str | None = None,
    ) -> None:
        self.http_session = http_session
        self.api_key = api_key
        self.folder_id = folder_id
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.model = model
        self.system_prompt = system_prompt

    async def prompt(self, user_prompt: str) -> str:
        messages: list[Message] = []
        if self.system_prompt:
            messages.append(
                {
                    "role": "system",
                    "text": self.system_prompt,
                },
            )

        messages.append(
            {
                "role": "user",
                "text": user_prompt,
            },
        )

        payload: YaGPTPrompt = {
            "modelUri": f"gpt://{self.folder_id}/{self.model}",
            "completionOptions": {
                "maxTokens": str(self.max_tokens),
                "temperature": self.temperature,
                "stream": False,
            },
            "messages": messages,
        }

        try:
            async with self.http_session.post(
                url=API_URL,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Api-Key {self.api_key}",
                },
                json=payload,
            ) as response:
                if response.status != 200:  # noqa: PLR2004
                    raise GPTError(text=await response.text())
                json = await response.json()
                text_response: str = json["result"]["alternatives"][0]["message"]["text"]
        except ClientError as err:
            raise GPTError(text="Client error") from err

        return text_response


__all__ = [
    "GPTError",
    "YandexGPT",
]
