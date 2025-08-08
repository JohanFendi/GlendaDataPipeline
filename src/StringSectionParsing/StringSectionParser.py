from abc import ABC, abstractmethod


class StringSectionParser(ABC):

    @abstractmethod
    def get_sections(self, string:str, separator:str) -> list[str]: 
        pass




