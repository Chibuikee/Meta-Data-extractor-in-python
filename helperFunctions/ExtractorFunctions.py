import re

from formatDate import format_date
from generalHelperFunctions import (
    create_key_and_value,
    index_sort_in_ascending,
    to_ascii,
)
from usefulVariables.regex import Lex_citation_regex, courts, courtsTypes


def parties_extractor(text, metadata={}):
    try:
        PstartIndex = re.search(r"(?:BETWEEN)(?::)?", to_ascii(text))
        # print(f"first: {PstartIndex}")
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
            resolvedPIndex = index_sort_in_ascending(regexes, text, PstartIndex.start())
            # print(f"first: {resolvedPIndex}")
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
            resolvedPIndex = index_sort_in_ascending(
                indexes, text, getattr(PstartIndex, "start", lambda: 0)()
            )
        # print(f"text now in: {resolvedPIndex}")

        PtextFromIndex = text[
            getattr(PstartIndex, "end", lambda: 0)() : resolvedPIndex["pickedIndex"]
        ]
        # print(f"text now in: {PtextFromIndex}")
        partiesRegex = r"\b[A-Z][A-Z .-]+\b"
        partiesMatch = re.findall(partiesRegex, PtextFromIndex)
        # print(f"text now in: {partiesMatch}")
        ex = [item.strip() for item in partiesMatch]

        if PstartIndex is None:
            regex = r"\b[A-Z]+.{3,}[A-Z]\b"
            partiesMatch = re.findall(regex, PtextFromIndex)
            # print(f"where the start index not found:{partiesMatch}")
            create_key_and_value("parties_0", [partiesMatch[0]], metadata)
            create_key_and_value("parties_1", [partiesMatch[1]], metadata)
        else:
            app = ex[: ex.index("AND")]
            res = ex[ex.index("AND") + 1 :]
            create_key_and_value("parties_0", app, metadata)
            create_key_and_value("parties_1", res, metadata)
        # print(f"meta data ready: {metadata}")

    except Exception as Err:
        print("Parties extraction failed", Err)
    finally:
        return metadata


def court_extraction(text, metadata={}):
    try:
        courtsIndexes = [Lex_citation_regex, r"(OTHER )?CITATIONS?"]
        CourtEndIndex = index_sort_in_ascending(courtsIndexes, text)
        # print(f"index for court slicing: {CourtEndIndex}")
        extractedCourt = text[: CourtEndIndex["pickedIndex"]]
        # print(f"court text extracted: {extractedCourt}")
        PickedCourt = []

        for regex in courtsTypes:
            court = re.search(regex, extractedCourt)
            # print(f"courts regex match: {court}")
            if court:
                PickedCourt = court.group()
                break
        metadata["court"] = (
            PickedCourt
            if PickedCourt
            else next((court for court in courts if court in text), "")
        )
    except Exception as Err:
        print(f"Court extraction failed: {Err}")
    # print(f"courts metadata: {metadata}")
    finally:
        return metadata


def year_of_judgement(text, metadata={}):
    try:
        datesRegex = r"\b\d+(TH|ST|ND|RD)?.+(JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER).+\d{4}\b"
        datesMatches = re.search(datesRegex, text)
        # print(f"date now: {datesMatches}")
        dateString = datesMatches.group() if datesMatches else ""
        completeDate = format_date(dateString, text)
        year = completeDate.split("-")[2] if "-" in completeDate else "No Year"
        metadata["date"] = completeDate
        metadata["year"] = year
    except Exception as Err:
        print(f"Date of judgement error: {Err}")
    finally:
        return metadata


def suit_number_extraction(text, metadata={}):
    try:
        regexesForSuitNoStop = [Lex_citation_regex, r"(OTHER )?CITATIONS?", r"BEFORE"]
        SuitNoEndIndex = index_sort_in_ascending(regexesForSuitNoStop, text)
        extractedSuitNoText = text[: SuitNoEndIndex["pickedIndex"]]
        suitNumberRegex = (
            r"(M\/|CA|SC|S.C|HD\/|LD\/|(\(\d+\)))[.\/\w\s-]+\d\w?\b|^\[\d+\].+"
        )
        suitNumberMatch = re.search(suitNumberRegex, extractedSuitNoText)
        metadata["suit_number"] = suitNumberMatch.group() if suitNumberMatch else ""

    except Exception as Err:
        print(f"Suit number extraction error: {Err}")
    finally:
        return metadata


def lex_citation_extraction(text, metadata={}):
    try:
        citationMatch = re.search(Lex_citation_regex, text)
        metadata["lex_citation"] = citationMatch.group() if citationMatch else ""

    except Exception as Err:
        print(f"Lex citation extraction failed: {Err}")
    finally:
        return metadata


text = """ATTORNEY GENERAL OF CROSS RIchibs STATE
V.
ATTORNEY GENERAL OF THE FEDERATION AND CHIBS
IN THE SUPREME COURT OF NIGERIA
24TH DAY OF JUNE, 2005
SC. 124/1999
LEX (2005) - SC. 124/1999

BEFORE THEIR LORDSHIPS
MUHAMMADU LAWAL UWAIS, CJN (Presided) 
ALOYSIUS IYORGYER KATSINA-ALU, JSC 
DAHIRU MUSDAPHER, JSC
DENNIS ONYEJIFE EDOZIE, JSC (Delivered the lead judgment)
IGNATIUS CHUKWUDI PATS-ACHOLONU, JSC 
GEORGE ADESOLA OGUNTADE, JSC 
SUNDAY AKINOLA AKINTAN, JSC

BETWEEN
A.G OF THE FEDERATION
THE ATTORNEY-GENERAL OF CROSS RIVER STATE
AND 
1. 	THE ATTORNEY-GENERAL OF THE FEDERATION
2. 	THE ATTORNEY-GENERAL OF AKWA-IBOM STATE

ISSUES FROM THE CAUSE(S) OF ACTION 
ADMINISTRATIVE AND GOVERNMENT LAW - BOUNDARY DISPUTE:- Determination of boundary disputes – Resolution of disputes as to which Local Government Area certain communities belong to – Relevance of Boundary map made and approved by the President of the Federation when boundary dispute was subjudice - Revision of map – Relevant considerations 
"""
# print(parties_extractor(text))
# print(court_extraction(text))
# print(year_of_judgement(text))
# print(suit_number_extraction(text))
# print(lex_citation_extraction(text))
# text[
#             getattr(start_index["pickedIndex"], "end", lambda: -1)()
#             # start_index["pickedIndex"].end()
#             # + text_length_checker(re.search(start_index["regexPicked"], text).group())
#             or 4 : getattr(end_index, "start", lambda: -1)()
#         ]
