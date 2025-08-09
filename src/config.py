from src.customTypes import DocType
from src.DocumentParsing.HTMLParser import RemoteHTMLParser
from src.LLMPromptingStrings import section_task_explination_lambda
from src.DocumentParsing.PDFParser import PDFParser

#Maps doctype to document parser, if doctument is not stored locally
REMOTE_DOCTYPE_PARSER_MAP = {
    DocType.HTML.value: RemoteHTMLParser, 
    DocType.PDF.value: PDFParser
}

#Maps doctype to document parser, if doctument is stored locally
LOCAL_DOCTYPE_PARSER_MAP = {}

#Maps doctype to lambda for task description for Section getter LLM
DOCTYPE_TASK_DESCRIPTION_MAP = {
    DocType.HTML.value: section_task_explination_lambda, #Takes separator
    DocType.PDF.value: section_task_explination_lambda #Takes separator
}

#Maps doctype to example of section getting result for section getter LLm
DOCTYPE_EXAMPLE_MAP = {}


CONSTANT_SINGLES_EXPLINATIONS:dict[str, str] = {
    #"document": "Get the name of the document, example: 'Course Syllabus for CS101, Programming'" #Already done in csv
}


CONSTANT_MULTIPLES_EXPLINATIONS:dict[str, str] = {
    "common_tags":"""A common tag is a keyword or short phrase that describes the 
                    overall content shared by all sections in the document.
                    The tag does not have to appear verbatim in the text.
                    Good examples include the document title, author, main topics, or key terms that appear throughout.
                    Extract up to 10 common tags."""
}


VARYING_SINGLES_EXPLINATIONS:dict[str, str] = {
    #"text": "Get the ALL of the textcontent of the seciton", # Already done via section splitting
    #"heading": "The heading of the section, or a generated one if none exists." #not used in current structure
}

VARYING_MULTIPLES_EXPLINATIONS:dict[str, str] = {
    "external_links": "Get external links from the section, such as emails, urls, etc.", 
    "tags": """A tag is a keyword or short phrase that describes the content or theme of the text section. 
             The tag does not have to appear verbatim in the text. For example, if the section lists several course names,
             a suitable tag could be 'course names'. Please extract up to 10 relevant tags per section."""
}

DATABASE_FOLDER_PATH = "database"
CSV_FILE_NAME = "se.csv"