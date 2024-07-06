import re

from generalHelperFunctions import (
    create_key_and_value,
    new_index_sort_in_ascending,
    to_ascii,
)


def parties_extractor(text, metadata={}):
    PstartIndex = re.search(r"(?:BETWEEN)(?::)?", to_ascii(text))
    # print(f"first: {PstartIndex.end()}")
    regexes = [
        r"BEFORE THEIR LORDSHIP",
        r"ORIGINATING COURT",
        r"ORIGINATING",
        r"REPRESENTATION",
        r"REPRESENTATIVE",
        r"\bISSUE.+ OF ACTION\b",
        r"Solicitor",
    ]

    resolvedPIndex = -1
    if PstartIndex:
        resolvedPIndex = new_index_sort_in_ascending(regexes, text, PstartIndex.start())
        print(f"first: {resolvedPIndex}")
    else:
        indexes = [
            r"IN THE ",
            r"COURT OF APPEAL",
            r"SUPREME COURT",
            r"PRIVY COUNCIL",
            r"HOUSE OF LORDS",
            r"HOUSE OF L\w+DS?",
            r"REPRESENTATION",
        ]
        resolvedPIndex = new_index_sort_in_ascending(indexes, text, PstartIndex.start())

    if PstartIndex:
        PtextFromIndex = text[PstartIndex.start() + 7 : resolvedPIndex.pickedIndex]
        partiesRegex = r"\b[A-Z][A-Z .-]+\b"
        partiesMatch = re.findall(partiesRegex, PtextFromIndex)
        ex = [item.strip() for item in partiesMatch]

        if PstartIndex == -1:
            regex = r"\b[A-Z]+.{3,}[A-Z]\b"
            partiesMatch = re.findall(regex, PtextFromIndex)
            create_key_and_value("parties_0", [partiesMatch[0]], metadata)
            create_key_and_value("parties_1", [partiesMatch[1]], metadata)
        else:
            app = ex[: ex.index("AND")]
            res = ex[ex.index("AND") + 1 :]
            create_key_and_value("parties_0", app, metadata)
            create_key_and_value("parties_1", res, metadata)


text = """BEFORE THEIR LORDSHIPS
MUHAMMADU LAWAL UWAIS, CJN (Presided) 
ALOYSIUS IYORGYER KATSINA-ALU, JSC 
DAHIRU MUSDAPHER, JSC
DENNIS ONYEJIFE EDOZIE, JSC (Delivered the lead judgment)
IGNATIUS CHUKWUDI PATS-ACHOLONU, JSC 
GEORGE ADESOLA OGUNTADE, JSC 
SUNDAY AKINOLA AKINTAN, JSC

BETWEEN
A.G OF CROSS RIVER STATE V A.G OF THE FEDERATION
THE ATTORNEY-GENERAL OF CROSS RIVER STATE
AND 
1. 	THE ATTORNEY-GENERAL OF THE FEDERATION
2. 	THE ATTORNEY-GENERAL OF AKWA-IBOM STATE

ISSUES FROM THE CAUSE(S) OF ACTION 
ADMINISTRATIVE AND GOVERNMENT LAW - BOUNDARY DISPUTE:- Determination of boundary disputes – Resolution of disputes as to which Local Government Area certain communities belong to – Relevance of Boundary map made and approved by the President of the Federation when boundary dispute was subjudice - Revision of map – Relevant considerations 
"""
parties_extractor(text)
# text[
#             getattr(start_index["pickedIndex"], "end", lambda: -1)()
#             # start_index["pickedIndex"].end()
#             # + text_length_checker(re.search(start_index["regexPicked"], text).group())
#             or 4 : getattr(end_index, "start", lambda: -1)()
#         ]
