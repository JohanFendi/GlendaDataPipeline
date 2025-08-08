from typing import override

from src.FieldGetting.FieldGetter import FieldGetter      
from src.LLMPrompting.LLMPrompter import LLMPrompter 
from src.LLMPromptingStrings import (
    prompt_constant_single,
    prompt_constant_multiple,
    prompt_varying_single,
    prompt_varying_multiple
)


class RegularFieldGetter(FieldGetter):


    def __init__(self, llm_prompter: LLMPrompter):
        self._llm_prompter = llm_prompter


    @override
    async def get_constant_single(self, sections: list[str], key_name: str, key_explination: str) -> str:
        prompt = prompt_constant_single(sections, key_name, key_explination)
        response = await self._llm_prompter.prompt(prompt)
        if response is None:
            return ""
        return response
    

    @override
    async def get_constant_multiple(self, sections: list[str], key_name: str, key_explination: str, separator: str) -> list[str]:
        prompt = prompt_constant_multiple(sections, key_name, key_explination, separator)
        string = await self._llm_prompter.prompt(prompt)
        if string is None: 
            return []
        return string.split(separator)
    

    @override
    async def get_varying_multiple(self, section: str, key_name: str, key_explination: str, separator: str) -> list[str]:
        prompt = prompt_varying_multiple(section, key_name, key_explination, separator)
        string = await self._llm_prompter.prompt(prompt)
        
        if string is None:
            return []
        return string.split(separator)
    

    @override
    async def get_varying_single(self, section: str, key_name: str, key_explination: str) -> str:
        prompt = prompt_varying_single(section, key_name, key_explination)
        response = await self._llm_prompter.prompt(prompt)
        if response is None:
            return ""
        return response
