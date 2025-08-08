from enum import Enum


class DocType(str, Enum): 
    PDF = "PDF"
    HTML = "HTML"


class JsonFieldType(str, Enum): 
    CONSTANT_SINGLE = "constant single"
    CONSTANT_MULTIPLE = "constant_multiple"
    VARYING_SINGLE = "varying_single"
    VARYING_MULTIPLE = "varying_multiple"