import os
import re
from datetime import datetime

from convertToASCII import to_ascii
from formatDate import formatDate
from generalHelperFunctions import create_key_and_value

# from indexResolver import IdentifierIndexResolver
from IndexSortInAscending import NewindexSortInAscending, indexSortInAscending
from logSaver import logSaver
from textLength import textLengthChecker
from usefulVariables.regex import RegexVariable

# Function to create key-value pairs in the metadata dictionary


async def MetadataProcessor(doc_path, text):
    metadata = {}
    courts = [
        "SUPREME COURT",
        "FEDERAL SUPREME COURT",
        "COURT OF APPEAL",
        "Court of Appeal",
        "FEDERAL HIGH COURT",
        "HIGH COURT",
        "COURT OF APPEAL, CIVIL DIVISION",
        "QUEEN'S BENCH",
        "QUEEN'S BENCH DIVISION",
        "APPEAL COURT DIVISION",
        "KING'S BENCH DIVISION",
        "KINGS COUNCIL",
        "APPEAL COURT",
        "HOUSE OF LORDS",
        "DIVISIONAL COURT",
        "PRIVY COUNCIL",
        "WACA",
        "CHANCERY",
    ]
    LexCitationRegex = r"LEX\s?.*\d\w?"
    # Extract CASE TITLE
    metadata["case_title"] = os.path.basename(doc_path).replace(
        os.path.splitext(doc_path)[1], ""
    )

    # PARTIES EXTRACTION
    PstartIndex = re.search(r"(?:BETWEEN)(?::)?", to_ascii(text))

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
        resolvedPIndex = NewindexSortInAscending(regexes, text, PstartIndex.start())
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
        resolvedPIndex = NewindexSortInAscending(indexes, text, PstartIndex.start())

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

    # Extract COURT
    LexCitationRegex = r"LEX\s?.*\d\w?"
    courtsIndexes = [LexCitationRegex, r"(OTHER )?CITATIONS?"]
    CourtEndIndex = NewindexSortInAscending(courtsIndexes, text)
    extractedCourt = text[: CourtEndIndex.pickedIndex]
    PickedCourt = []

    for regex in RegexVariable.courtsTypes:
        court = re.search(regex, extractedCourt)
        if court:
            PickedCourt = court.group()
            break
    metadata["court"] = (
        PickedCourt
        if PickedCourt
        else next((court for court in courts if court in text), "")
    )

    # Extract DATE and YEAR
    datesRegex = r"\b\d+(TH|ST|ND|RD)?.+(JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER).+\d{4}\b"
    datesMatches = re.search(datesRegex, text)
    dateString = datesMatches.group() if datesMatches else ""
    completeDate = formatDate(dateString, text)
    year = completeDate.split("-")[2] if "-" in completeDate else "No Year"
    metadata["date"] = completeDate
    metadata["year"] = year

    # SUIT NUMBER EXTRACTION
    regexesForSuitNoStop = [LexCitationRegex, r"(OTHER )?CITATIONS?", r"BEFORE"]
    SuitNoEndIndex = NewindexSortInAscending(regexesForSuitNoStop, text)
    extractedSuitNoText = text[: SuitNoEndIndex.pickedIndex]
    suitNumberRegex = (
        r"(M\/|CA|SC|S.C|HD\/|LD\/|(\(\d+\)))[.\/\w\s-]+\d\w?\b|^\[\d+\].+"
    )
    suitNumberMatch = re.search(suitNumberRegex, extractedSuitNoText)
    metadata["suit_number"] = suitNumberMatch.group() if suitNumberMatch else ""

    # Extract Citation
    citationMatch = re.search(LexCitationRegex, text)
    metadata["lex_citation"] = citationMatch.group() if citationMatch else ""

    # Other citation numbers
    otherCitstartIndex = re.search(r"(OTHER )?CITATIONS?", text)
    if otherCitstartIndex:
        regexothercitStop = [
            r"BEFORE THEIR LORDSHIPS?",
            r"BEFORE HIS LORDSHIP",
            r"BEFORE",
            r"BETWEEN",
            r"ORIGINATING COURT(\(S\))?",
        ]
        resolvedOtherCitStop = NewindexSortInAscending(
            regexothercitStop, text, otherCitstartIndex.start()
        )
        otherCittextFromIndex = text[
            otherCitstartIndex.start() : resolvedOtherCitStop.pickedIndex
        ]
        citeRegex = r"(?<=\n+)(.+)"
        listOfCitations = re.findall(citeRegex, otherCittextFromIndex)
        create_key_and_value("other_citations", listOfCitations, metadata)

    # Extract AREAS OF LAW
    areaRegexStart = [
        r"\bISSUE.+ OF ACTIONS?\b",
        r"\bMAIN ISSUES?\b",
        r"PRACTICE AND PROCEDURE ISSUES",
        r"SUBSTANTIVE LEGAL AND POLICY ISSUES?",
    ]
    arearesolvedIndex = NewindexSortInAscending(areaRegexStart, text)
    areaRegexStop = [r"CASE SUMMARY", r"MAI?N JUDGE?MENT"]
    arearesolvedIndexStop = NewindexSortInAscending(
        areaRegexStop, text, arearesolvedIndex.pickedIndex
    )
    textFromIndex = text[
        arearesolvedIndex.pickedIndex
        + textLengthChecker(
            re.search(areaRegexStart[arearesolvedIndex.regexPicked], text).group()
        ) : arearesolvedIndexStop.pickedIndex
    ]
    arearegex = r"(?<=\n+)[A-Z ]+(?=.+(?:-|:))"
    allMatches = re.findall(arearegex, textFromIndex)
    cleanAreasofLaw = [item.strip() for item in allMatches]
    UniqueAreasofLaw = list(set(cleanAreasofLaw))
    for index, value in enumerate(UniqueAreasofLaw):
        metadata[f"area_of_law_{index}"] = value

    # Semantic tags
    metadata["semantic_tags_0"] = "Caselaw"
    metadata["semantic_tags_1"] = "legal document"
    metadata["semantic_tags_2"] = "Case"
    if metadata["court"] == "SUPREME COURT":
        metadata["semantic-tags_3"] = "high_profile_case"

    # JUDGES EXTRACTIONS
    JstartRegex = [r"\bBEFORE.*(LORDSHIPS?:?|JUDGES?:?)\b", r"\bBEFORE:"]
    JstartIndex = NewindexSortInAscending(JstartRegex, text)
    Jregexes = [
        r"BETWEEN",
        r"REPRESENTATION",
        r"ORIGINATING COURT",
        r"\bISSUE.+ OF ACTION\b",
    ]
    JresolvedIndex = NewindexSortInAscending(Jregexes, text, JstartIndex.pickedIndex)
    cutText = text[
        JstartIndex.pickedIndex
        + textLengthChecker(
            re.search(JstartRegex[JstartIndex.regexPicked], text).group()
        ) : JresolvedIndex.pickedIndex
    ]
    judgesRegex = r"(\b[A-Z].+(SC|CA|S.C|C.A|N|J|LC)\b|\b(LORD|[A-Z]+).+[A-Z]{4,}\b)"
    matches = re.findall(judgesRegex, cutText)
    allJudges = [item.strip().split("\n")[0] for item in matches]
    create_key_and_value("judge", allJudges, metadata)

    # Extract LEGAL REPRESENTATION
    startRegexRep = [r"REPRESENTATIONS?", r"REPRESENTATIVE", r"Solicitor"]
    resolvedRepstart = NewindexSortInAscending(startRegexRep, text)
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
    resolvedRepstop = NewindexSortInAscending(
        regexreStopRep, text, resolvedRepstart.pickedIndex
    )
    reptextFromIndex = "Representation Not Found"
    if resolvedRepstop.pickedIndex != -1:
        reptextFromIndex = text[
            resolvedRepstart.pickedIndex
            + textLengthChecker(
                re.search(startRegexRep[resolvedRepstart.regexPicked], text).group()
            ) : resolvedRepstop.pickedIndex
        ].replace(
            r"\((?!with him\b)[^()]*\)|solicitors?|LAWYERS?|respondents?|Applicants|\bfor\b|\bthe\b|Barrister|Appellants?|\bwith\b",
            "",
        )
    ArrayOfReps = re.split(r"\bAND\b", reptextFromIndex)
    ArrayOfwordsToRemove = [
        "Esq",
        "Counsel",
        "No Legal Representation",
        "Plaintiff",
        "Defendants",
        "Defendant",
    ]
    wordsToRemoveInLowerCase = [item.lower() for item in ArrayOfwordsToRemove]

    def remove_item(word):
        return word.lower() not in wordsToRemoveInLowerCase

    reparearegex = r"\b[A-Z\s]*&[\sA-Z]+\b|\b([A-Z]\.\s?){0,4}([A-Z][a-z\s-]+)*([A-Z][a-z]+)(, (Esq|SAN|S.A.N))?\b|(\b[A-Z][A-Z.\s]+ [A-Z-.]+\b)|\b[A-Z]{4,}"
    repApp = [
        item for item in re.findall(reparearegex, ArrayOfReps[0]) if remove_item(item)
    ]
    repRes = (
        [item for item in re.findall(reparearegex, ArrayOfReps[1])]
        if len(ArrayOfReps) > 1
        else []
    )
    if repApp and repRes and resolvedRepstart.pickedIndex != -1:
        create_key_and_value("representation_appellant", repApp, metadata)
        create_key_and_value("representation_respondent", repRes, metadata)
    elif repApp and not repRes and resolvedRepstart.pickedIndex != -1:
        create_key_and_value("representation", repApp, metadata)

    # ORIGINATING COURTS
    startOriginating = re.search(r"ORIGINATING COURT(\(S\))?", text)
    regexOriginating = [
        r"REPRESENTATION",
        r"\bISSUE.+ OF ACTIONS?\b",
        r"MAIN ISSUES?",
        r"SUBSTANTIVE LEGAL AND POLICY ISSUES?",
    ]
    ResolvedStopOriginating = indexSortInAscending(regexOriginating, text)
    if startOriginating:
        textFromOriginating = text[
            startOriginating.start()
            + textLengthChecker(
                re.search(r"ORIGINATING COURT(\(S\))?", text).group()
            ) : ResolvedStopOriginating
        ]
        originatingregex = r"(?<=\d\.\t)(.+)"
        originatingregex2 = r"(.+)"
        originatingallMatches = re.findall(
            originatingregex, textFromOriginating
        ) or re.findall(originatingregex2, textFromOriginating)
        originatingCourts = [
            item.replace("-end!", "") for item in originatingallMatches
        ]
        create_key_and_value("originating_court", originatingCourts, metadata)

    # Generate unique doc_id
    metadata["doc_id"] = os.path.basename(doc_path).replace(
        os.path.splitext(doc_path)[1], ""
    )

    # Set doctype to "case"
    metadata["doctype"] = "case"

    return metadata
