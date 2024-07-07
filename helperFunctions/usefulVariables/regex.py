Lex_citation_regex = r"LEX\s?.*\d\w?"
courtsTypes = [
    r"SUPREME COURT OF NIGERIA",
    r"FEDERAL SUPREME COURT",
    r"SUPREME COURT",
    r"COURT OF APPEAL",
    # r"Court of Appeal",
    r"FEDERAL HIGH COURT",
    r"HIGH COURT",
    r"QUEEN'S BENCH",
    r"QUE.+ BENCH DIVISION",
    r"APPEAL COURT DIVISION",
    r"KING'S BENCH DIVISION",
    r"KINGS COUNCIL",
    r"APPEAL COURT",
    r"\bPROBATE.+ DIVISION\b",
    # r"HOUSE OF LORDS",
    # used because of potential spelling errors
    r"HOUSE OF L\w+DS?",
    r"DIVISIONAL COURT",
    r"PRIVY COUNCIL",
    r"WACA",
    r"CHANCERY",
]

courts = [
    "SUPREME COURT",
    "FEDERAL SUPREME COURT",
    "HOUSE OF LORDS",
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
    "DIVISIONAL COURT",
    "PRIVY COUNCIL",
    "WACA",
    "CHANCERY",
]


apex_courts = [
    "SUPREME COURT OF NIGERIA",
    "SUPREME COURT",
    "FEDERAL SUPREME COURT",
    "HOUSE OF LORDS",
    "PRIVY COUNCIL",
    "WACA",
]
