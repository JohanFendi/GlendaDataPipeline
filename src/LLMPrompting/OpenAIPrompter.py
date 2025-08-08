from openai import AsyncOpenAI


class OpenAIPrompter(): 
    """Compatible with Akash chat and Deepseek api"""
    
    def __init__(self, model:str, api_key:str, url:str) -> None: 
        self._model = model
        self._client = AsyncOpenAI(
            api_key=api_key, 
            base_url=url
        )
    
    
    async def prompt(self, prompt:str) -> str: 
        response = await self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "user", "content":prompt},
            ], 
            stream = False
        )
        return response.choices[0].message.content