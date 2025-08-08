from typing import override

from src.ApiKey import load_api_key
from src.LLMPrompting.LLMPrompter import LLMPrompter
from src.LLMPrompting.OpenAIPrompter import OpenAIPrompter


class AkashPrompter(LLMPrompter): 

    def __init__(self, model:str) -> None:  
        key = load_api_key("AKASH_API_KEY")
        url = "https://chatapi.akash.network/api/v1"
        self._open_ai_prompter = OpenAIPrompter(model, key, url)


    @override
    async def prompt(self, prompt) -> str:
        return await self._open_ai_prompter.prompt(prompt)