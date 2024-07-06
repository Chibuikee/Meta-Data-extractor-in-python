import re


def new_index_sort_in_ascending(regexes, text, first_index=0):
    # List to hold all matching indexes
    indexes_array = []
    regex_array = []

    # Iterate over each regex to find its index in the text
    for regex in regexes:
        match = re.search(regex, text)
        if match:
            index = match.start()
            indexes_array.append(index)
            regex_array.append((index, regex))

    # Sort the list of indexes in ascending order
    sorted_indexes = sorted(indexes_array)

    # Find the first index greater than first_index
    picked_index = sorted_indexes[0] if sorted_indexes else None
    if picked_index is not None and first_index > picked_index:
        picked_index = next(
            (item for item in sorted_indexes if item > first_index), None
        )

    regex_picked = None
    for item in regex_array:
        if item[0] == picked_index:
            regex_picked = item[1]
            break

    # Return the picked index or -1 if no valid index is found
    if picked_index is not None:
        return {"pickedIndex": picked_index, "regexPicked": regex_picked}
    else:
        return {"pickedIndex": -1, "regexPicked": None}
