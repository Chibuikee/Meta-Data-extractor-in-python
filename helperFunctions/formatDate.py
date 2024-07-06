import re

from generalHelperFunctions import index_sort_in_ascending

# from textLength import text_length_checker

courts = [
    r"SUPREME COURT",
    r"FEDERAL SUPREME COURT",
    r"COURT OF APPEAL",
    r"FEDERAL HIGH COURT",
    r"HIGH COURT",
    r"QUEEN'S BENCH",
    r"QUEEN'S BENCH DIVISION",
    r"APPEAL COURT DIVISION",
    r"KING'S BENCH DIVISION",
    r"KINGS COUNCIL",
    r"APPEAL COURT",
    r"\bPROBATE.+ DIVISION\b",
    r"HOUSE OF L\w+DS?",
    r"DIVISIONAL COURT",
    r"PRIVY COUNCIL",
    r"WACA",
    r"CHANCERY",
]


def format_date(input_date, text):
    regex = r"(\d+)(?:TH|ST|ND|RD)?.+(\w+).+(\d{4})"
    match = re.search(regex, input_date, re.IGNORECASE)
    # print(f"the extracted date String is: {match}")
    if not match:
        start_index = index_sort_in_ascending(courts, text)
        # end_index = text.find("LEX")
        end_date_regexes = [r"LEX\s.*\d+\b"]
        end_index = index_sort_in_ascending(end_date_regexes, text)
        if end_index == None:
            end_index = -1
        extracted_date = text[
            start_index["end"]
            # start_index["pickedIndex"].end()
            # + text_length_checker(re.search(start_index["regexPicked"], text).group())
            or 4 : end_index["pickedIndex"]
        ]
        if extracted_date:
            input_date = extracted_date
        else:
            return "Invalid date format"

    day_match = re.search(r"\b\d{1,2}(?=TH|ST|ND|RD)?", input_date)
    month_match = re.search(
        r"(JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)",
        input_date,
        re.IGNORECASE,
    )
    year_match = re.search(r"(\d{4})", input_date)

    month_map = {
        "JANUARY": 1,
        "FEBRUARY": 2,
        "MARCH": 3,
        "APRIL": 4,
        "MAY": 5,
        "JUNE": 6,
        "JULY": 7,
        "AUGUST": 8,
        "SEPTEMBER": 9,
        "OCTOBER": 10,
        "NOVEMBER": 11,
        "DECEMBER": 12,
    }

    day = day_match.group() if day_match else None
    month = month_map.get(month_match.group().upper()) if month_match else "invalid"
    year = year_match.group() if year_match else None

    formatted_date = f"{day}-{month}-{year}"
    # (
    #     f"{day}-{month}-{year}" if all([day, month, year]) else "Invalid date format"
    # )

    return formatted_date


# new_word = """ MORGAN
# V
# SMALLY
# COURT OF APPEAL, CIVIL DIVISION
# 23 JANUARY 2004
# [2002] ALL ER (D) 107 (NOV)
# LEX (2002) – ALL E.R 107

# OTHER CITATIONS
# 3PLR/2004/69 (SC)
# BEFORE: WARD, MUMMERY AND RIX LJJ
# """

# print(format_date("23 JANUARY 2004", new_word))
