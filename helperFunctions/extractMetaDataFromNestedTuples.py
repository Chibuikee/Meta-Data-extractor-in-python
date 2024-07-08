import re

from .convertToASCII import to_ascii
from .generalHelperFunctions import flatten_a_2D_list


def extract_regex_match(regex_pattern, text):
    # Compile the regex pattern
    pattern = re.compile(regex_pattern)
    # pattern = regex_pattern

    # Find all matches in the text
    # matches = pattern.findall(text)
    # matches = ['MUHAMMADU LAWAL UWAIS, CJN (Presided) ', 'ALOYSIUS IYORGYER KATSINA-ALU, JSC ', 'DAHIRU MUSDAPHER, JSC', 'DENNIS ONYEJIFE EDOZIE, JSC (Delivered the lead judgment)', 'IGNATIUS CHUKWUDI PATS-ACHOLONU, JSC ', 'GEORGE ADESOLA OGUNTADE, JSC ', 'SUNDAY AKINOLA AKINTAN, JSC']
    matches = pattern.finditer(to_ascii(text))
    # print(f"from first {[ i.group().strip() for i in matches]}")
    # print(f"from first {flatten_a_2D_list([re.split(r"\r",i.group())  for i in matches])}")
    # Process the matches
    # extracted_names = extract_regex_match_from_nested_tuples(matches)

    # return extracted_names
    extracted_items = flatten_a_2D_list(
        [re.split(r"\r", i.group().strip()) for i in matches]
    )
    return extracted_items


def extract_regex_match_from_nested_tuples(match_object):
    # Process the matches
    extracted_names = []
    for match in match_object:
        # If the match is a tuple, join non-empty strings
        if isinstance(match, tuple):
            name = " ".join(filter(bool, match))
        else:
            name = match

        # Remove leading/trailing whitespace and add to list if non-empty
        name = name.strip()
        if name:
            extracted_names.append(name)

    return extracted_names
