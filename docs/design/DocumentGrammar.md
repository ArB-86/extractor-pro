# Extractor-Pro Document Grammar

## Document

Document
    := Chapter+

--------------------------------------------------

Chapter

Chapter
    := Section*

--------------------------------------------------

Section

Section
    := (
        Paragraph
      | Example
      | Exercise
      | Activity
      | FigureItOut
      | SampleQuestion
      )*

--------------------------------------------------

Exercise

Exercise
    := Question+

--------------------------------------------------

Question

Question
    := QuestionHeader
       QuestionBody
       SubQuestion*

--------------------------------------------------

QuestionHeader

QuestionHeader
    := NUMBER
     | STAR_NUMBER

--------------------------------------------------

SubQuestion

SubQuestion
    := RomanSubQuestion
     | AlphaSubQuestion

--------------------------------------------------

RomanSubQuestion

RomanSubQuestion
    := (i)
     | (ii)
     | (iii)
     | ...

--------------------------------------------------

AlphaSubQuestion

AlphaSubQuestion
    := (a)
     | (b)
     | (c)
     | ...

--------------------------------------------------

Paragraph

Paragraph
    := TEXT+

--------------------------------------------------

Example

Example
    := ExampleHeader
       Paragraph*

--------------------------------------------------

Activity

Activity
    := ActivityHeader
       Paragraph*

