import csv
import asyncio
import pprint
import json
import sys
from pathlib import Path
from logging import INFO
from colorama import Fore


from src.Logging.CustomLogging import get_logger
from src.DocumentParsing.Parser import Parser
from src.customTypes import DocType
from src.StringSectionParsing.SectionSeparator import SectionSeparator
from src.FieldGetting.RegularFieldGetter import RegularFieldGetter
from src.LLMPrompting.AkashPrompter import AkashPrompter
from src.DocumentParsing.HTMLParser import RemoteHTMLParser
from src.DocumentParsing.PDFParser import PDFParser
from src.Exceptions import NoParserFoundError, TagObjectNotFoundError, APIKeyNotFoundError
from src.config import (REMOTE_DOCTYPE_PARSER_MAP, 
                        DOCTYPE_TASK_DESCRIPTION_MAP,
                        CONSTANT_MULTIPLES_EXPLINATIONS, 
                        CONSTANT_SINGLES_EXPLINATIONS, 
                        VARYING_MULTIPLES_EXPLINATIONS, 
                        VARYING_SINGLES_EXPLINATIONS, 
                        DATABASE_FOLDER_PATH, 
                        CSV_FILE_NAME)


def load_links_and_doc_types(csv_file_name: str) -> list[tuple[str, str, str, str]]:
    link_doctypes = []
    with open(csv_file_name, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            link = row["link"]
            doctype = row["doctype"]
            doc_name = row["document"]
            database = row["database"]
            link_doctypes.append((link, doctype, doc_name, database))
    return link_doctypes


def get_parser(doctype: str, doctype_parser_map: dict[str, Parser]) -> Parser:
    parser = doctype_parser_map.get(doctype)

    if parser is None:
        raise NoParserFoundError(f"No parser found for doctype: {doctype}")
    
    if issubclass(parser, RemoteHTMLParser):
        tags_to_extract = ["main"]
        tags_to_remove = ["nav", "footer", "header", "script", "svg", "button", "style"]
        parser_type = "html.parser"
        return RemoteHTMLParser(tags_to_extract, tags_to_remove, parser_type)
    elif issubclass(parser, PDFParser):
        return PDFParser()
    
    else:
        raise NoParserFoundError(f"No parser found for doctype: {doctype}")
    

def get_sectioning_task_prompt(doctype: str, separator:str, doctype_task_description_map: dict[str, str]) -> str:
    task_description_lambda = doctype_task_description_map.get(doctype)
    if not task_description_lambda:
        raise ValueError(f"No task description found for doctype: {doctype}")
    task_description = task_description_lambda(separator)
    return task_description


async def get_constant_data(field_getter: RegularFieldGetter,
                            sections: list[str], 
                            separator: str, 
                            constant_singles_explinations: dict[str, str], 
                            constant_multiples_explinations: dict[str, str], 
                            doc_name: str) -> dict[str, str]:
    constant_data = {}

    constant_data["document"] = doc_name  # Add document name directly
    for key, explination in constant_singles_explinations.items():
        value = await field_getter.get_constant_single(sections, key, explination)
        constant_data[key] = value

    for key, explination in constant_multiples_explinations.items():
        value = await field_getter.get_constant_multiple(sections, key, explination, separator)
        constant_data[key] = value

    return constant_data


async def get_varying_data(field_getter: RegularFieldGetter, 
                           section: str, 
                           separator: str, 
                           varying_singles_explinations: dict[str, str], 
                           varying_multiples_explinations: dict[str, str]) -> dict[str, list[str]]:
    varying_data = {}

    varying_data["text"] = section  # Add the text content of the section directly
    for key, explination in varying_singles_explinations.items():
        value = await field_getter.get_varying_single(section, key, explination)
        varying_data[key] = value

    for key, explination in varying_multiples_explinations.items():
        value = await field_getter.get_varying_multiple(section, key, explination, separator)
        varying_data[key] = value

    return varying_data


def init_database(database_folder_path:str, database_file_name:str) -> Path: 
    folder_path = Path(database_folder_path)
    folder_path.mkdir(parents=True, exist_ok=True)
    file_path = folder_path / database_file_name
    file_path.touch()
    return file_path


def write_to_database(file_path: Path, data_points: list[dict[str, any]]) -> None:
    with file_path.open("a") as f:
        for data in data_points:
            json.dump(data, f)
            f.write("\n")  # Ensure each entry is on a new line

        
async def main():
    try: 
        llm_prompter = AkashPrompter("Meta-Llama-3-3-70B-Instruct")
    except APIKeyNotFoundError as e:
        logger.exception(f"API key not found for link: {link}, doctype: {doctype}, doc_name: {doc_name}")
        sys.exit()

    csv_file_name = CSV_FILE_NAME
    link_doctypes = load_links_and_doc_types(csv_file_name)
    separator = "||"
    section_separator = SectionSeparator()
    logger = get_logger("%(asctime)s - %(name)s - %(levelname)s - %(message)s", "GlendaDataPipeline", "Error.log", INFO)
    field_getter = RegularFieldGetter(llm_prompter)

    print_sectioning = False
    print_data_points = True
    for link, doctype, doc_name, database_file_name in link_doctypes:
        if doctype not in ["HTML", "PDF"]: 
            print(Fore.RED + f"Skipping document: {doc_name}, because it is not of a supported doc_type. It is of type: {doctype}.")
            continue
        try: 
            print(Fore.YELLOW + f"\nProcessing link: {link}, doctype: {doctype}, doc_name: {doc_name}\n")
            parser = get_parser(doctype, REMOTE_DOCTYPE_PARSER_MAP)
            string = parser.parse(link)
            llm_task_description = get_sectioning_task_prompt(doctype, separator, DOCTYPE_TASK_DESCRIPTION_MAP)
            llm_prompt = f"**Task description**:\n{llm_task_description}\n**Text**:\n{string}"
            response = await llm_prompter.prompt(llm_prompt)
            sections = section_separator.get_sections(response, separator)

            if print_sectioning: 
                print(Fore.WHITE + f"LLM prompt: {llm_prompt}\n\n")
                print(Fore.WHITE + f"Number of sections found: {len(sections)}\n\n")
                for i, section in enumerate(sections):
                    print(Fore.WHITE + f"======Section {i}======\n{section}\n\n")

            constant_data = await get_constant_data(field_getter, sections, separator, 
                                                    CONSTANT_SINGLES_EXPLINATIONS, 
                                                    CONSTANT_MULTIPLES_EXPLINATIONS,
                                                    doc_name)
            data_points = []

            for section in sections: 
                section_data = {}
                section_data.update(constant_data)
                varying_data = await get_varying_data(field_getter, section, separator, 
                                                    VARYING_SINGLES_EXPLINATIONS, VARYING_MULTIPLES_EXPLINATIONS)
                section_data.update(varying_data)
                data_points.append(section_data)

            if print_data_points:
                print(Fore.GREEN + f"\nData points for {doc_name}:\n")
                for i, elem in enumerate(data_points):
                    print(Fore.WHITE + f"\nData point {i}:\n")
                    pprint.pprint(elem, indent=2)

            file_path = init_database(DATABASE_FOLDER_PATH, database_file_name)
            write_to_database(file_path, data_points)
            print(Fore.GREEN + f"\nData points for {doc_name} written to {file_path}.\n")

        except NoParserFoundError as e:
            logger.exception(f"No parser found for link: {link}, doctype: {doctype}, doc_name: {doc_name}")
            sys.exit()
        except TagObjectNotFoundError as e:
            logger.exception(f"Tag object not found during parsing for link: {link}, doctype: {doctype}, doc_name: {doc_name}.")
        except Exception as e:
            logger.exception(f"Unexpected error for link: {link}, doctype: {doctype}, doc_name: {doc_name}")

        


if __name__ == "__main__":  
    asyncio.run(main())