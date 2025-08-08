from abc import ABC, abstractmethod


class LLMPrompter(ABC): 

    @abstractmethod
    async def prompt(self, prompt:str) -> str: 
        pass
