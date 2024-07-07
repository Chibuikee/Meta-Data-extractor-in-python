import re

from .filterOutWord import filtered_and_refined_words
from .formatDate import format_date
from .generalHelperFunctions import (
    create_key_and_value,
    index_sort_in_ascending,
    to_ascii,
)
from .logger import loggerToFile
from .usefulVariables.regex import Lex_citation_regex, courts, courtsTypes


def parties_extractor(text, metadata={}):
    try:
        PstartIndex = re.search(r"(?:BETWEEN)(?::)?", text)
        # PstartIndex = re.search(r"(?:BETWEEN)(?::)?", to_ascii(text))
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
        # loggerToFile(PtextFromIndex)
        # print(f"text now in : {PtextFromIndex}")
        partiesRegex = r"\b[A-Z][A-Z .-]+\b"
        partiesMatch = re.findall(partiesRegex, PtextFromIndex)
        # print(f"text now in: {partiesMatch}")
        ex = [item.strip() for item in partiesMatch]

        if PstartIndex is None:
            regex = r"\b[A-Z]+.{3,}[A-Z]\b"
            partiesMatch = re.findall(regex, PtextFromIndex)
            parties_array = partiesMatch[0].split()

            filtered_parties = [
                i for i in parties_array if i not in ["V", "V.", "v", "v."]
            ]
            print(f"Parties filtered:{filtered_parties}")
            create_key_and_value("parties_0", [filtered_parties[0]], metadata)
            create_key_and_value("parties_1", [filtered_parties[1]], metadata)
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
        # lex_CitstartIndex = re.search(r"(OTHER )?CITATIONS?", text)

        regexlex_citStop = [
            r"(OTHER )?CITATIONS?",
            r"BEFORE THEIR LORDSHIPS?",
            r"BEFORE HIS LORDSHIP",
            r"BEFORE",
            r"BETWEEN",
            r"ORIGINATING COURT(\(S\))?",
        ]
        # lex_CitstartIndex = lex_CitstartIndex.end() if lex_CitstartIndex else 0
        resolvedlex_CitStop = index_sort_in_ascending(
            regexlex_citStop,
            text,
            # lex_CitstartIndex,
        )
        lex_CittextFromIndex = text[
            # lex_CitstartIndex : resolvedlex_CitStop["pickedIndex"]
            0 : resolvedlex_CitStop["pickedIndex"]
        ]
        citationMatch = re.search(Lex_citation_regex, lex_CittextFromIndex)
        metadata["lex_citation"] = citationMatch.group() if citationMatch else ""

    except Exception as Err:
        print(f"Lex citation extraction failed: {Err}")
    finally:
        return metadata


def other_citations_extraction(text, metadata={}):
    try:
        otherCitstartIndex = re.search(r"(OTHER )?CITATIONS?", text)

        regexothercitStop = [
            r"BEFORE THEIR LORDSHIPS?",
            r"BEFORE HIS LORDSHIP",
            r"BEFORE",
            r"BETWEEN",
            r"ORIGINATING COURT(\(S\))?",
        ]
        otherCitstartIndex = otherCitstartIndex.end() if otherCitstartIndex else 0
        resolvedOtherCitStop = index_sort_in_ascending(
            regexothercitStop,
            text,
            otherCitstartIndex,
        )
        otherCittextFromIndex = text[
            otherCitstartIndex : resolvedOtherCitStop["pickedIndex"]
        ]
        citeRegex = r"(?<=\n)\n*(.+)"
        # don't use this it results in
        # this error "look-behind requires fixed-width pattern"
        # citeRegex = r"(?<=\n+)(.+)"
        listOfCitations = re.findall(citeRegex, otherCittextFromIndex)
        create_key_and_value("other_citations", listOfCitations, metadata)

    except Exception as Err:
        print(f"Other citations extraction failed: {Err}")
    finally:
        return metadata


def legal_representation_extraction(text, metadata={}):
    try:
        startRegexRep = [r"REPRESENTATIONS?", r"REPRESENTATIVE", r"Solicitor"]
        resolvedRepstart = index_sort_in_ascending(startRegexRep, text)
        regexreStopRep = [
            r"PRACTICE AND PROCEDURE ISSUES",
            r"\bISSUE.+ OF ACTIONS?\b",
            r"BEFORE",
            r"MAI?N JUDGE?MENT",
            r"MAIN ISSUES?",
            r"ORIGINATING COURT",
            r"ISSUES FOR DETERMINATION",
            r"SUBSTANTIVE LEGAL AND POLICY ISSUES",
            r"ISSUES? FROM  CAUSE",
        ]
        resolvedRepstop = index_sort_in_ascending(
            regexreStopRep, text, resolvedRepstart["pickedIndex"]
        )
        reptextFromIndex = "Representation Not Found"
        if resolvedRepstop["pickedIndex"]:
            reptextFromIndex = re.sub(
                r"\((?!with him\b)[^()]*\)|solicitors?|LAWYERS?|respondents?|Applicants|\bfor\b|\bthe\b|Barrister|Appellants?|\bwith\b",
                ",",
                text[resolvedRepstart["end"] : resolvedRepstop["pickedIndex"]],
                flags=re.IGNORECASE,
            )

        ArrayOfReps = re.split(r"\bAND\b", reptextFromIndex)
        #    words that where mistakenly matched but not wanted
        ArrayOfwordsToRemove = [
            "Esq",
            "Counsel",
            "No Legal Representation",
            "Plaintiff",
            "Defendants",
            "Defendant",
        ]

        reparearegex = r"\b[A-Z\s]*&[\sA-Z]+\b|\b([A-Z]\.\s?){0,4}([A-Z][a-z\s-]+)*([A-Z][a-z]+)(, (Esq|SAN|S.A.N))?\b|(\b[A-Z][A-Z.\s]+ [A-Z-.]+\b)|\b[A-Z]{4,}"

        repApp = filtered_and_refined_words(
            ArrayOfReps[0], ArrayOfwordsToRemove, reparearegex
        )
        repRes = (
            filtered_and_refined_words(ArrayOfReps[1], reparearegex, reparearegex)
            if len(ArrayOfReps) > 1
            else []
        )

        if repApp and repRes and resolvedRepstart["pickedIndex"]:
            create_key_and_value("representation_appellant", repApp, metadata)
            create_key_and_value("representation_respondent", repRes, metadata)
        elif repApp and not repRes and resolvedRepstart["pickedIndex"]:
            create_key_and_value("representation", repApp, metadata)

    except Exception as Err:
        print(f"Legal representation extraction failed: {Err}")
    finally:
        return metadata


def originating_court_extraction(text, metadata={}):
    try:
        startOriginating = re.search(r"ORIGINATING( COURT)?(\(S\))?", text)
        regexOriginating = [
            r"REPRESENTATION",
            r"\bISSUE.+ OF ACTIONS?\b",
            r"MAIN ISSUES?",
            r"SUBSTANTIVE LEGAL AND POLICY ISSUES?",
        ]
        ResolvedStopOriginating = index_sort_in_ascending(regexOriginating, text)

        textFromOriginating = text[
            (
                startOriginating.end() if startOriginating else -1
            ) : ResolvedStopOriginating["pickedIndex"]
        ]
        originatingregex = r"(?<=\d\.\t)(.+)"
        originatingregex2 = r"(.+)"
        originatingallMatches = re.findall(
            originatingregex, textFromOriginating
        ) or re.findall(originatingregex2, textFromOriginating)
        originatingCourts = [
            item.replace("-end!", "") for item in originatingallMatches
        ]
        if startOriginating:
            create_key_and_value("originating_court", originatingCourts, metadata)

    except Exception as Err:
        print(f"originating court extraction failed: {Err}")
    finally:
        return metadata


def judges_extraction(text, metadata={}):
    try:
        JstartRegex = [r"\bBEFORE.*(LORDSHIPS?:?|JUDGES?:?)\b", r"\bBEFORE:"]
        JstartIndex = index_sort_in_ascending(JstartRegex, text)
        Jregexes = [
            r"BETWEEN",
            r"REPRESENTATION",
            r"ORIGINATING COURT",
            r"\bISSUE.+ OF ACTION\b",
        ]
        JresolvedIndex = index_sort_in_ascending(
            Jregexes, text, JstartIndex["pickedIndex"]
        )
        cutText = text[JstartIndex["end"] : JresolvedIndex["pickedIndex"]]
        judgesRegex = (
            r"(\b[A-Z].+(SC|CA|S.C|C.A|N|J|LC)\b|\b(LORD|[A-Z]+).+[A-Z]{4,}\b)"
        )
        words_to_remove = ["cutText"]
        allJudges = filtered_and_refined_words(cutText, words_to_remove, judgesRegex)
        # matches = re.findall(judgesRegex, cutText)
        # allJudges = [item.strip().split("\n")[0] for item in matches]
        create_key_and_value("judge", allJudges, metadata)

    except Exception as Err:
        print(f" Judges extraction failed: {Err}")
    finally:
        return metadata


def areas_of_law_extraction(text, metadata={}):
    try:
        areaRegexStart = [
            r"\bISSUE.+ OF ACTIONS?\b",
            r"\bMAIN ISSUES?\b",
            r"PRACTICE AND PROCEDURE ISSUES",
            r"SUBSTANTIVE LEGAL AND POLICY ISSUES?",
        ]
        arearesolvedIndex = index_sort_in_ascending(areaRegexStart, text)
        areaRegexStop = [r"CASE SUMMARY", r"MAI?N JUDGE?MENT"]
        arearesolvedIndexStop = index_sort_in_ascending(
            areaRegexStop, text, arearesolvedIndex["pickedIndex"]
        )
        textFromIndex = text[
            arearesolvedIndex["end"] : arearesolvedIndexStop["pickedIndex"]
        ]
        arearegex = r"(?<=\n)\n*[A-Z ]+(?=.+(?:-|:))"
        allMatches = re.findall(arearegex, textFromIndex)
        cleanAreasofLaw = [item.strip() for item in allMatches]
        UniqueAreasofLaw = list(set(cleanAreasofLaw))
        create_key_and_value("area_of_law", UniqueAreasofLaw, metadata)
        # for index, value in enumerate(UniqueAreasofLaw):
        #     metadata[f"area_of_law_{index}"] = value

    except Exception as Err:
        print(f" extraction failed: {Err}")
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

ORIGINATING COURT
HIGH COURT, MAIDUGURI (Hague J. Presiding)

REPRESENTATION
AKINSANYA for COLE, Applicants, LAWYERS - for the Appellant AND
LIBERTY, Senior State Counsel - for the Respondent

ISSUES FROM THE CAUSE(S) OF ACTION 
ADMINISTRATIVE AND GOVERNMENT LAW - BOUNDARY DISPUTE:- Determination of boundary disputes – Resolution of disputes as to which Local Government Area certain communities belong to – Relevance of Boundary map made and approved by the President of the Federation when boundary dispute was subjudice - Revision of map – Relevant considerations 
CHILDREN AND WOMEN LAW:- 
HEALTHCARE AND LAW:- Medical emergency services – Availability and access to – Dispensary Attendant as the 
RELIGION AND LAW - SHARIA LAW:- Matrimonial complaints disclosing sensitive issue between man and 
CRIMINAL LAW AND PROCEDURE: - Evidence – Extra-judicial statement made to Police officer – Failure to take 
"""
# print(parties_extractor(text))
# print(court_extraction(text))
# print(year_of_judgement(text))
# print(suit_number_extraction(text))
# print(lex_citation_extraction(text))
# print(other_citations_extraction(text))
# print(legal_representation_extraction(text))
# print(areas_of_law_extraction(text))
# print(judges_extraction(text))
# print(originating_court_extraction(text))
# text[
#             getattr(start_index["pickedIndex"], "end", lambda: -1)()
#             # start_index["pickedIndex"].end()
#             # + text_length_checker(re.search(start_index["regexPicked"], text).group())
#             or 4 : getattr(end_index, "start", lambda: -1)()
#         ]
