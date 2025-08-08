

# Glenda Data Pipeline

A Python pipeline for extracting, parsing, and structuring document data (currently HTML) using LLMs and custom parsers. Outputs structured data to JSONL files for further analysis.

## Features

- Fetches and parses remote HTML documents.
- Splits text into logical sections using LLM prompts.
- Extracts constant and varying fields (tags, external links, etc.) from each section.
- Outputs structured data to a database folder in JSONL format.
- Easily configurable for new document types and fields.

## Requirements

- Python 3.10+
- Install dependencies:
  ```
  pip install -r requirements.txt
  ```
  Required packages: `beautifulsoup4`, `requests`, `openai`, `python-dotenv`

## Configuration

1. **API Key**  
    Add your Akash API key to `.env`:
    ```
    AKASH_API_KEY=your_key_here
    ```

2. **Edit `src/config.py`**  
    - Set `DATABASE_FOLDER_PATH` (default: `database`)
    - Set `CSV_FILE_NAME` (default: `remoteDocs.csv`)
    - Configure field explanations and mappings as needed.
    - Explination of Constant vs. Varying Data:
        Constant data refers to information that remains the same across all sections of a document. For example, the document title or common tags that apply to the entire document.
        Varying data is information that can change from one section to another. For example, the main text content, section-specific tags, or external links found in each section.
        Single vs. Multiple Data:

        Single means only one value is expected for a field (e.g., the document name).
        Multiple means a list of values is expected for a field (e.g., a list of tags or external links).
        Examples:

        Constant Single: Document title (one value for the whole document)
        Constant Multiple: Common tags (a list of tags for the whole document)
        Varying Single: Section text (one main text per section)
        Varying Multiple: Section tags or links (a list of tags/links per section)
        This structure helps organize and extract both global and section-specific information from documents.

3. **Prepare your CSV file**  
    - First row should be:  link,doctype,document,database
    - Then enter your data. Example row:
      ```
      link,doctype,document,database
      "https://www.gu.se/en/study-gothenburg/data-management-dit034/syllabus/89ef0bbb-32ec-11ef-8651-fc591a704454",HTML,"Data Management DIT034","se_DIT034.jsonl"
      ```

## Usage

1. Make sure your configuration and CSV are set up.
2. Run the pipeline:
    ```
    python main.py
    ```
3. Output will be written to the specified JSONL file in the `database` folder.

## Supported Document Types

- Currently: `HTML`
- See `src/customTypes.py` and `src/DocumentParsing/` for how to add support for other types (e.g., PDF).

## Project Structure

- `main.py` — Entry point, runs the pipeline.
- `src/config.py` — Configuration and mappings.
- `src/DocumentParsing/` — Parsers for different document types.
- `src/FieldGetting/` — Field extraction logic using LLMs.
- `src/LLMPrompting/` — LLM prompt interfaces.
- `database/` — Output folder for JSONL files.

## Limitations

- Only remote HTML parsing is supported out of the box.
- Requires Akash API key for LLM operations.
- CSV must be properly formatted.

## Extending

- To add new document types, implement a parser in `src/DocumentParsing/` and update mappings in `config.py`.
- To extract new fields, add explanations in `config.py`.



