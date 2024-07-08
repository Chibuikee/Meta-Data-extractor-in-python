import re

from .extractMetaDataFromNestedTuples import extract_regex_match


def filtered_and_refined_words(
    sliced_text,
    array_of_words_to_remove,
    regex_applied,
    regex_for_words_first_deleted=None,
    # delete_words=False,
):
    # Apply the first regex
    # replacing unwanted words with "" resulted in 'PATRICK A DEVLIN    .\nG ST CLAIR PILCHER KC'
    # using "," result extra comma like in 'MUHAMMADU LAWAL UWAIS, CJN , '
    # so replace with "."
    result = sliced_text
    if regex_for_words_first_deleted:
        result = re.sub(
            regex_for_words_first_deleted, ".", sliced_text, flags=re.IGNORECASE
        )
    # print(f"words to removed{result}")
    # Convert words to remove to lowercase
    r_word = [item.lower() for item in array_of_words_to_remove]

    # Define the removeItem function
    def remove_item(word):
        # print(f"word to convert{word not in r_word}")
        return word.lower() not in r_word

    # Apply the second regex and filter the results
    matched_words = extract_regex_match(regex_applied, result)
    # print(f"word to convert{matched_words}")
    return list(set(filter(remove_item, matched_words)))


#  USAGE OF THE ABOVE FUNCTION
# text = """
# Solicitor for appellant: A. L. BRYDEN.
# Solicitors for respondent: ASHURST, MORRIS, CRISP & CO.
# ROBERT ASKE KC and PATRICK A DEVLIN (for A A MOCATTA on war service) for the Appellants.
# G ST CLAIR PILCHER KC and H G ROBERTSON (for CHARLES STEVENSON on war service) for the Respondents.
# Solicitor for appellant: A. L. BRYDEN. Solicitors for respondent: ASHURST, MORRIS, CRISP & CO. ROBERT ASKE KC and PATRICK A DEVLIN (for A A MOCATTA on war service) for the Appellants. G ST CLAIR PILCHER KC and H G ROBERTSON (for CHARLES STEVENSON on war service) for the Respondents. Solicitors:  HOLMAN FENWICK & WILLAN  -for the Appellants  PARKER GARRETT & CO - for the Respondents C St J NICHOLSON Esq - Barrister   PICKFORD, WARRINGTON, and SCRUTTON L.JJ.
# The claimant appeared in person.
# JEREMY CAREY (instructed by TAYLOR WALTON, LUTON) for the defendant.
# IAN DENHAM Barrister
# """
# ArrayOfwordsToRemove = ["Esq", "Counsel"]

# #  this is to remove certain words from the extracted text before matching it
# regexForWordsFirstDeleted = r"\([^()]*\)|solicitors?|Barrister?|respondents?|\bfor\b|\bthe\b|Appellants?|\bwith\b|Representations?"

# regexApplied = r"\b[A-Z\s]*&[\sA-Z]+\b|\b([A-Z]\.\s?){0,4}([A-Z][a-z\s-]+)*([A-Z][a-z]+)(, (Esq|SAN|S.A.N))?\b|(\b[A-Z][A-Z.\s]+ [A-Z-.]+\b)|\b[A-Z]{4,}"

# print(
#     filtered_and_refined_words(
#         text, ArrayOfwordsToRemove, regexForWordsFirstDeleted, regexApplied
#     )
# )
# for i in filtered_and_refined_words(
#     text, ArrayOfwordsToRemove, regexForWordsFirstDeleted, regexApplied
# ):
#     print(i)
