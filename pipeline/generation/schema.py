from dataclasses import dataclass, field

@dataclass
class GeneratedQuestion:

    question:str=""

    answer:str=""

    solution:str=""

    difficulty:str="medium"

    bloom:str=""

    topic:str=""

    subtopic:str=""

    question_type:str=""

    marks:int=0

    estimated_time:int=0

    concepts:list=field(default_factory=list)

    keywords:list=field(default_factory=list)
