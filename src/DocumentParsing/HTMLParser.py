import requests
from bs4 import BeautifulSoup, Tag
from typing import override


from src.Exceptions import TagObjectNotFoundError
from src.DocumentParsing.Parser import Parser


class RemoteHTMLParser(Parser):

    def __init__(self, 
                tags_to_extract:list[str], 
                tags_to_remove:list[str],
                parser:str) -> None:
        self._tags_to_extract = tags_to_extract
        self._tags_to_remove = tags_to_remove
        self._parser = parser


    @override
    def parse(self,
              url:str) -> str:

        resp = requests.get(url,timeout=10)
        resp.raise_for_status()     
        html = resp.text    

        uncleaned_soup = BeautifulSoup(html, self._parser) 
        tag_objects = self._extract_tags(self._tags_to_extract, uncleaned_soup)
        cleaned_soup = self._combine_tags_as_soup(tag_objects, self._parser)
        self._remove_tags(self._tags_to_remove, cleaned_soup)

        return cleaned_soup.get_text(separator="\n", strip=True)


    def _remove_tag(self, tag_name:str, soup:BeautifulSoup) -> None: 
        for tag in soup.find_all(tag_name): 
            tag.decompose()


    def _remove_tags(self, tag_names:list[str], soup:BeautifulSoup) -> None: 
        for tag in tag_names:
            self._remove_tag(tag, soup)


    def _extract_tag(self, tag_name:str, soup:BeautifulSoup) -> list[Tag]:
        return list(soup.find_all(tag_name)) 


    def _extract_tags(self, tag_names:list[str], soup:BeautifulSoup) -> list[Tag]: 
        tag_objects:list[Tag] = []

        for tag in tag_names: 
            ts = self._extract_tag(tag, soup)
            for tag_object in ts: 
                tag_objects.append(tag_object)

        if len(tag_objects) == 0: 
            raise TagObjectNotFoundError(f"Tags {tag_objects} not found in soup.") 
        
        return tag_objects


    def _combine_tags_as_soup(self, tag_objects:list[Tag], parser:str) -> BeautifulSoup: 
        string = ""
        for tag_object in tag_objects: 
            string += str(tag_object)

        return BeautifulSoup(string, parser)


