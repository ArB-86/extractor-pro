from dataclasses import dataclass, field

@dataclass
class DatasetRecord:

    question_id:str=""

    board:str="CBSE"
    publisher:str="NCERT"
    edition:str="2026"

    class_no:int=0
    subject:str="Mathematics"

    chapter:str=""
    section:str=""
    exercise:str=""

    question_no:str=""
    sub_question:str=""

    page_start:int=0
    page_end:int=0

    question:str=""

    options:dict=field(default_factory=dict)

    answer:str=""
    solution:str=""

    figures:list=field(default_factory=list)
    tables:list=field(default_factory=list)
    formulae:list=field(default_factory=list)

    keywords:list=field(default_factory=list)
    concepts:list=field(default_factory=list)

    difficulty:str="unknown"

    source:str=""

    content_hash:str=""

    parser_version:str="3"

    verified:bool=True

    metadata:dict=field(default_factory=dict)
