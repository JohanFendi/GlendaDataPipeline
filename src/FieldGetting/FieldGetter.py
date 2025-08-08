from abc import ABC, abstractmethod


class FieldGetter(ABC): 

    @abstractmethod
    def get_constant_single(self, sections:list[str], key_name:str, key_explination:str) ->  str:
        """key_explination: how to get the 'key_name' from the sections. 
            Returns dict mapping key_names to the parsed value."""
        pass


    @abstractmethod
    def get_constant_multiple(self, sections:list[str], key_name:str, key_explination:str, separator:str) -> list[str]: 
        """key_explination: how to get the 'key_name' from the sections"""
        pass


    @abstractmethod
    def get_varying_multiple(self, section:str, key_name:str, key_explination:str, separator:str) -> list[str]: 
        """key_explination: how to get the 'key_name' from the sections"""
        pass


    @abstractmethod
    def get_varying_single(self, section:str, key_name:str, key_explination:str) -> str: 
        """key_explination: how to get the 'key_name' from the sections"""
        pass