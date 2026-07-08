from dataclasses import dataclass, field

@dataclass
class ValidationResult:

    question_id:str=""

    valid:bool=True

    confidence:float=0.0

    missing_text:list=field(default_factory=list)

    extra_text:list=field(default_factory=list)

    corrected_question:str=""

    remarks:str=""
