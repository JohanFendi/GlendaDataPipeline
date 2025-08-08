from typing import override


from src.StringSectionParsing.StringSectionParser import StringSectionParser


class SectionSeparator(StringSectionParser):
    
    @override
    def get_sections(self, string:str, separator:str) -> list[str]: 
        return string.split(separator)