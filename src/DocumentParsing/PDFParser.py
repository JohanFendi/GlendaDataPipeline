import fitz
from typing import override

import requests



from src.DocumentParsing.Parser import Parser


class PDFParser(Parser):

    def _get_blocks(self, link: str) -> list[str]:
        response = requests.get(link)
        response.raise_for_status()
        doc = fitz.open(stream=response.content, filetype="pdf")

        blocks = []  
        seen_blocks = set()  # To track unique blocks
        for page_num in range(doc.page_count):
            page = doc[page_num]
            page_blocks = page.get_text("blocks")
            
            # Extract and clean text blocks per page
            for block in page_blocks:
                text = block[4].strip()
                if text and text not in seen_blocks:
                    seen_blocks.add(text)
                    blocks.append(text)
                    
        return blocks

    @override
    def parse(self, link: str) -> str:
        blocks = self._get_blocks(link)
        return "\n".join(blocks)
