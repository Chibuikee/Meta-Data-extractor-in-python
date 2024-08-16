import json
import os
import re
import uuid

# Updated array of judge titles
JUDGE_TITLES = ["JCA", "JSC", "CJN", "CJ", "FJ", "JJ", "LJ", "AG", "J"]


def improved_title_case(s):
    exceptions = {
        "a",
        "an",
        "and",
        "as",
        "at",
        "but",
        "by",
        "for",
        "if",
        "in",
        "of",
        "on",
        "or",
        "the",
        "to",
        "with",
    }
    words = s.split()
    return " ".join(
        word.capitalize() if word.lower() not in exceptions or i == 0 else word.lower()
        for i, word in enumerate(words)
    )


def capitalize_after_dash(s):
    return re.sub(r"-([a-z]| [a-z])", lambda m: "-" + m.group(1).upper(), s)
    # return re.sub(r"-([a-z])", lambda m: "-" + m.group(1).upper(), s)


def capitalize_abbreviations(s):
    def replace_abbr(match):
        return match.group(0).upper()

    # Handle periods separately
    s = re.sub(r"\b[A-Za-z]\.([A-Za-z]\.)+", replace_abbr, s)

    # Handle common titles
    s = re.sub(r"\b(mr|mrs|ms|dr)\b", replace_abbr, s, flags=re.IGNORECASE)

    return s


def process_value(value):
    if isinstance(value, str):
        value = value.replace("_", " ").rstrip("-").strip()
        value = improved_title_case(value)
        value = capitalize_abbreviations(value)
        return value
    elif isinstance(value, list):
        return [process_value(item) for item in value]
    elif isinstance(value, dict):
        return {k: process_value(v) for k, v in value.items()}
    else:
        return value


def capitalize_and_remove_spaces(value):
    if isinstance(value, str):
        return re.sub(r"\s+", "", value.upper())
    elif isinstance(value, list):
        return [capitalize_and_remove_spaces(item) for item in value]
    else:
        return value


def standardize_judge_title(name):
    pattern = r",?\s*(" + "|".join(JUDGE_TITLES) + r")\b"

    def replace_title(match):
        return " " + match.group(1).upper()

    name = re.sub(r"\s*\.\s*", "", name)
    name = re.sub(r"\s+", " ", name.strip())
    name = re.sub(pattern, replace_title, name, flags=re.IGNORECASE)
    name = capitalize_after_dash(name)

    return name.strip()


def consolidate_keys(data):
    consolidated = {}
    party_keys = []

    for key, value in data.items():
        normalized_key = key.replace("-", "_")
        base_key = re.sub(r"_\d+$", "", normalized_key)

        if base_key.startswith("parties"):
            party_keys.append(key)
        else:
            if base_key not in consolidated:
                consolidated[base_key] = []

            if isinstance(value, list):
                consolidated[base_key].extend(value)
            else:
                consolidated[base_key].append(value)

    consolidated["parties"] = []
    for key in party_keys:
        value = data[key]
        if isinstance(value, list):
            consolidated["parties"].extend(value)
        else:
            consolidated["parties"].append(value)

    for key in consolidated:
        if key == "parties":
            flattened = [
                item.strip()
                for sublist in consolidated[key]
                for item in (sublist if isinstance(sublist, list) else [sublist])
                if item
            ]
            consolidated[key] = [process_value(v) for v in flattened if v]
        elif len(consolidated[key]) == 1:
            consolidated[key] = process_value(consolidated[key][0])
        else:
            consolidated[key] = [process_value(v) for v in consolidated[key] if v]

    return consolidated


def process_json(input_file, output_folder):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for case_title, case_data in data.items():
        new_case_data = consolidate_keys(case_data)
        new_case_title = process_value(case_title)
        new_case_title = re.sub(
            r"\bV[Ss]?\.?\s", "v. ", new_case_title, flags=re.IGNORECASE
        )
        new_case_title = capitalize_abbreviations(new_case_title)

        for key, value in new_case_data.items():
            if key in ["suit_number", "lex_citation", "other_citations"]:
                new_case_data[key] = capitalize_and_remove_spaces(value)
            elif key == "judge":
                if isinstance(value, list):
                    new_case_data[key] = [
                        standardize_judge_title(judge) for judge in value
                    ]
                else:
                    new_case_data[key] = standardize_judge_title(value)
            else:
                new_case_data[key] = process_value(value)

        new_case_data["case_title"] = new_case_title
        new_case_data["doc_id"] = str(uuid.uuid4())

        output_file = os.path.join(output_folder, f"{new_case_title}.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(new_case_data, f, indent=2, ensure_ascii=False)
        print(f"Processed: {new_case_title}")


def main():
    # FOR CHIBUIKE
    input_folder = (
        # r"C:\chibs\Desktop\chibscodes\python\path\documentsToProcess\A - DELIVERED"
        # r"C:\chibs\Desktop\chibscodes\python\path\documentsToProcess\Processed_for_entity_extraction_Russell"
        # r"C:\chibs\Desktop\chibscodes\python\path\documentsToProcess\B - FULL"
        # r"C:\chibs\Desktop\chibscodes\python\path\documentsToProcess\C - MINUS _CASE SUMMARY"
        r"C:\chibs\Desktop\chibscodes\python\path\documentsToProcess\Processed_for_entity_extraction_Russell"
    )
    output_folder = r"C:\chibs\Desktop\chibscodes\python\path\ready_to_injest\Processed_for_entity_extraction_Russell"
    # FOR RUSSLE
    # input_folder = r"C:\Users\Russell\Desktop\Second\in_TEST"
    # output_folder = r"C:\Users\Russell\Desktop\Second\out_TEST"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            input_file = os.path.join(input_folder, filename)
            process_json(input_file, output_folder)


if __name__ == "__main__":
    main()


# print(f"String supplied hmm: {capitalize_after_dash("MARY UKAEGO PETER-odILI, JSC")}")
# python case_metadata_preprocessor.py
