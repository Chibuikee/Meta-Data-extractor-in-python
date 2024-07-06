import json
import os
import re
from pathlib import Path

import win32com.client
from convertToASCII import to_ascii
from docxTypeExtractor import doc_files_extractor
from logger import loggerToFile


async def quick_metadata_processor(json_data, doc_path, text):
    case_name = Path(doc_path).stem
    each_case = json_data.get(case_name, {})
    newtext = text[9:190]

    loggerToFile(to_ascii(newtext))
    # print(f"hey{newtext}")
    # Extract Citation
    # The character U+2013 "–" could be confused with the ASCII character U+002d "-", which is more common in source code
    citation_regex = r"LEX\s.*?-.*?\d+\b"
    # text = """MORGAN
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
    citation_match = re.search(citation_regex, to_ascii(text))
    # loggerToFile(citation_match.group())
    # print(f"yup: {citation_match}")
    updated_case = {
        **each_case,
        "lex_citation": citation_match.group() if citation_match else "",
    }

    return updated_case


# "MORGAN V SMALLY": {
#         "doc_id": "MORGAN V SMALLY"
#     }
async def quick_save_metadata_as_json(metadata, output_dir):
    output_filename = Path(output_dir) / "metadata.json"

    json_data = {}
    if output_filename.exists():
        existing_data = output_filename.read_text(encoding="utf-8")
        json_data = json.loads(existing_data)
        # print(f"check out: {metadata["doc_id"]}")
    json_data[metadata["doc_id"]] = metadata
    output_filename.write_text(json.dumps(json_data, indent=4), encoding="utf-8")
    print(f"meta data saved for: {metadata["doc_id"]}")


async def quick_fix(input_dir, output_dir, json_path):
    try:
        input_dir = Path(input_dir)
        output_dir = Path(output_dir)
        json_path = Path(json_path)
        # print(f"test n{input_dir}")

        files = os.listdir(input_dir)
        json_data = json.loads(json_path.read_text(encoding="utf-8"))
        # print(f"now showing{json_data}")
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        for file in files:
            doc_path = input_dir / file
            try:
                file_text = await doc_files_extractor(doc_path, file, word)
                # with open("./output/extracttext.txt", "w") as tf:
                #     tf.write(file_text)

                # print(f"here it is: {file_text}")
                if file_text:
                    metadata = await quick_metadata_processor(
                        json_data, doc_path, file_text
                    )
                    # print(f"meta started: {metadata}")
                    await quick_save_metadata_as_json(metadata, output_dir)
            except Exception as err:
                print(f" from quickfix func Error processing {file}: {err}")

    except Exception as error:
        print("Error:", error)
    finally:
        word.Quit()


# Example usage
import asyncio

if __name__ == "__main__":
    asyncio.run(quick_fix("../path/case", "../path/to", "../path/to/metadata.json"))
