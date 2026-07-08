import re

QUESTION = re.compile(r'^\d+\.\s')

SUBQUESTION = re.compile(r'^\(([ivxlcdm]+|[a-z])\)', re.I)

OPTION = re.compile(r'^\([A-D]\)', re.I)

EXERCISE = re.compile(r'^(EXERCISE|Miscellaneous Exercise)', re.I)

SECTION = re.compile(r'^\d+\.\d+\s+[A-Z]', re.I)

FIGURE = re.compile(r'^(Fig|Figure)', re.I)

PAGE = re.compile(r'^Reprint', re.I)

SUMMARY = re.compile(r'^\d+\.\d+\s+Summary', re.I)

ROMAN = re.compile(r'^\([ivxlcdm]+\)', re.I)
