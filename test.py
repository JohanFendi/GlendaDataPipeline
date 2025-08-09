from src.DocumentParsing.PDFParser import PDFParser



url = "https://www.gu.se/sites/default/files/2023-09/GU2023-1727_faststa%CC%88lld_utbildningsplan_N1SOF_220616_eng%5B2%5D.pdf"
parser = PDFParser()
res = parser.parse(url)

for item in res:
    print("\n")
    print(item)