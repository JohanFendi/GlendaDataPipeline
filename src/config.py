from src.customTypes import DocType, JsonFieldType
from src.DocumentParsing.HTMLParser import RemoteHTMLParser
from src.LLMPromptingStrings import section_task_explination_lambda

#Maps doctype to document parser, if doctument is not stored locally
REMOTE_DOCTYPE_PARSER_MAP = {
    DocType.HTML.value: RemoteHTMLParser
}

#Maps doctype to document parser, if doctument is stored locally
LOCAL_DOCTYPE_PARSER_MAP = {}

#Maps doctype to lambda for task description for Section getter LLM
DOCTYPE_TASK_DESCRIPTION_MAP = {
    DocType.HTML.value: section_task_explination_lambda #Takes separator
}

#Maps doctype to example of section getting result for section getter LLm
DOCTYPE_EXAMPLE_MAP = {}


CONSTANT_SINGLES_EXPLINATIONS:dict[str, str] = {
    #"document": "Get the name of the document, example: 'Course Syllabus for CS101, Programming'" #Already done in csv
}


CONSTANT_MULTIPLES_EXPLINATIONS:dict[str, str] = {
    "common_tags":"""A common tag is a keyword or term descriptive of all sections. 
                     Good candidates include the document title, 
                    main topics, and key terms. Get a maximum of 10 common tags.""",
}


VARYING_SINGLES_EXPLINATIONS:dict[str, str] = {
    #"text": "Get the ALL of the textcontent of the seciton", # Already done via section splitting
    #"heading": "The heading of the section, or a generated one if none exists." #not used in current structure
}

VARYING_MULTIPLES_EXPLINATIONS:dict[str, str] = {
    "external_links": "Get external links from the section, such as emails, urls, etc.", 
    "tags": "A tag is a keyword or term descriptive of the section. Get a maximum of 10 tags."
}

DATABASE_FOLDER_PATH = "database"
CSV_FILE_NAME = "remoteDocs.csv"