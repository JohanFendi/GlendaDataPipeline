from abc import ABC, abstractmethod


class Parser(ABC):

    @abstractmethod
    def parse(self, link: str) -> dict:
        pass