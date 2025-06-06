import re
import unicodedata


def flatten_a_2D_list(list):
    flat_list = []
    for row in list:
        flat_list.extend(row)
    return flat_list


def create_key_and_value(key, data_array, metadata):
    if data_array is not None:
        for index, value in enumerate(data_array):
            metadata[f"{key}_{index}"] = value.rstrip().rstrip("-").rstrip()


# this is just to filter out words only
# don't confuse with filtered_and_refined_words which does more than filtering out words
def filter_out_some_words(matched_words, array_of_words_to_remove):
    r_words = [item.lower() for item in array_of_words_to_remove]

    # Define the removeItem function
    def remove_item(word):
        # print(f"word to convert{word not in r_word}")
        return word.lower() not in r_words

    return list(set(filter(remove_item, matched_words)))


def index_sort_in_ascending(regexes, text, first_index=0):
    # List to hold all matching indexes
    indexes_array = []
    regex_array = []

    # Iterate over each regex to find its index in the text
    for regex in regexes:
        match = re.search(regex, text)
        if match:
            index = match.start()
            indexes_array.append(index)
            regex_array.append((index, regex, match.end()))

    # Sort the list of indexes in ascending order
    sorted_indexes = sorted(indexes_array)

    # Find the first index greater than first_index
    picked_index = sorted_indexes[0] if sorted_indexes else None
    if picked_index is not None and first_index > picked_index:
        picked_index = next(
            (item for item in sorted_indexes if item > first_index), None
        )

    regex_picked = None
    end_Index = None
    for item in regex_array:
        if item[0] == picked_index:
            regex_picked = item[1]
            end_Index = item[2]
            break

    # Return the picked index or -1 if no valid index is found
    if picked_index is not None:
        return {
            "pickedIndex": picked_index,
            # "start": picked_index.start(),
            "end": end_Index,
            "regexPicked": regex_picked,
        }
    else:
        return {"pickedIndex": None, "end": None, "regexPicked": None}


def to_ascii(text):

    # Additional replacements for common characters
    replacements = {
        "–": "-",  # en dash
        # "–": "-",  # en dash
        "—": "-",  # em dash
        '"': '"',  # curly double quote left
        '"': '"',  # curly double quote right
        "'": "'",  # curly single quote
        "…": "...",  # ellipsis
        "€": "EUR",  # euro sign
        "£": "GBP",  # pound sign
        "©": "(c)",  # copyright sign
        "®": "(R)",  # registered trademark sign
        "™": "(TM)",  # trademark sign
        "“": '"',
        "”": '"',
        "’": "'",
    }

    # First, replace known characters
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)

    # Then, normalize and convert remaining characters
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = "".join(c for c in normalized if ord(c) < 128)

    return ascii_text


# Test the function
# test_strings = [
#     "Café au lait",
#     "Résumé",
#     "Niño",
#     "Größe",
#     "こんにちは",
#     "Привет",
#     "The em dash — is longer than the en dash –",
#     "Ellipsis… and © ® ™ symbols",
#     "€10 and £20",
# ]

# for string in test_strings:
#     print(f"Original: {string}")
#     print(f"ASCII:    {to_ascii(string)}")
#     print()
