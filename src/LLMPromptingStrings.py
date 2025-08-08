section_task_explination_lambda = lambda separator: f"""
You will be given plain text.

1. Split the text into sections of 150–200 words.
2. Preserve basic structure cues: treat short standalone lines as headings and lines that look like list items as "- item".
3. Keep most text verbatim. Remove content only if it's clearly repetitive (exact duplicates) or clearly irrelevant navigation/technical noise (e.g., "Back to top", tracker IDs). Do NOT summarize or drop important sentences.
4. Prefer paragraph boundaries; if a paragraph exceeds 150–200 words, 
    split at the nearest earlier sentence boundary. Otherwise split at sentence or list-item boundaries. 
    Avoid leaving a heading alone.
5. Place exactly one occurrence of this separator between sections: '{separator}'

OUTPUT:
- Return only the sections in order, separated by the separator. No extra text.
- Begin immediately with the first section.
"""


# Single constant value
prompt_constant_single = lambda sections, key_name, key_explanation: f"""
You will be given multiple text sections.

TASK:
1. Identify and extract the single value for: "{key_name}".
2. Use the following explanation to guide your extraction: {key_explanation}
3. Consider all sections together to find the correct value.

OUTPUT RULES:
- Return only the extracted value, nothing else.
- Do not add explanations, notes, or formatting.
- If the section does not contain any occurrences of: "{key_name}", return an empty string.

SECTIONS:
{'\n'.join(sections)}
"""

# Multiple constant values
prompt_constant_multiple = lambda sections, key_name, key_explanation, separator: f"""
You will be given multiple text sections.

TASK:
1. Identify and extract all occurrences of: "{key_name}".
2. Use the following explanation to guide your extraction: {key_explanation}
3. Consider all sections together when extracting.

OUTPUT RULES:
- Return only the extracted values.
- Separate each value with exactly this symbol: {separator}
- Do not add explanations, notes, numbering, or extra whitespace.
- If the section does not contain any occurrences of: "{key_name}", return an empty string.

SECTIONS:
{'\n'.join(sections)}
"""

# Multiple varying values
prompt_varying_multiple = lambda section, key_name, key_explanation, separator: f"""
You will be given a single text section.

TASK:
1. Identify and extract all occurrences of: "{key_name}".
2. Use the following explanation to guide your extraction: {key_explanation}

OUTPUT RULES:
- Return only the extracted values.
- Separate each value with exactly this symbol: {separator}
- Do not add explanations, notes, numbering, or extra whitespace.
- If the section does not contain any occurrences of: "{key_name}", return an empty string.

SECTION:
{section}
"""

# Single varying value
prompt_varying_single = lambda section, key_name, key_explanation: f"""
You will be given a single text section.

TASK:
1. Identify and extract the single value for: "{key_name}".
2. Use the following explanation to guide your extraction: {key_explanation}

OUTPUT RULES:
- Return only the extracted value, nothing else.
- Do not add explanations, notes, or formatting.

SECTION:
{section}
"""
c = lambda key_name : f" If the section does not contain any occurrences of: {key_name}, return an empty string."
