import copy
import re

_ROMAN = re.compile(r'^\(([ivxlcdm]+)\)', re.I)
_ALPHA = re.compile(r'^\(([a-z])\)', re.I)


class SubQuestionExpander:

    def expand(self, questions):

        out=[]

        for q in questions:

            lines=q.question.splitlines()

            current=None
            groups=[]

            for line in lines:

                t=line.strip()

                if _ROMAN.match(t) or _ALPHA.match(t):

                    if current:
                        groups.append(current)

                    current=[t]

                    continue

                if current is not None:
                    current.append(t)

            if current:
                groups.append(current)

            if not groups:

                out.append(q)
                continue

            parent=copy.deepcopy(q)

            parent.sub_question=""

            out.append(parent)

            for g in groups:

                child=copy.deepcopy(q)

                child.sub_question=g[0][1:g[0].index(")")]

                child.question="\n".join(g)

                out.append(child)

        return out
