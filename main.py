import json
import os
from pathlib import Path

import win32com.client

# from helperFunctions.metadataExtractor import MetadataProcessor
from helperFunctions.docxTypeExtractor import doc_files_extractor
from helperFunctions.metadataExtractor import MetadataProcessor

# from helperFunctions.docTypeExtractor import docFilesExtractor
# from helperFunctions.logSaver import logSaver


# Function to save metadata as JSON
def save_metadata_as_json(metadata, output_dir):
    output_filename = os.path.join(output_dir, "metadata.json")

    json_data = {}
    if os.path.exists(output_filename):
        with open(output_filename, "r", encoding="utf-8") as file:
            existing_data = file.read()
            json_data = json.loads(existing_data)

    json_data[metadata["doc_id"]] = metadata

    with open(output_filename, "w", encoding="utf-8") as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)
    print(f"Meta data saved for {metadata["doc_id"]}")


# Function to process documents in a directory
async def process_documents(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    files = os.listdir(input_dir)
    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        for file in files:
            doc_path = os.path.join(input_dir, file)
            # print(f"All documents{doc_path}")

            if file.endswith(".docx") or file.endswith(".doc"):
                # does not check a file for it's extension but checks a folder for files with a particular extension
                # if Path("/Pongo/").glob("*.docx") or Path("/Pongo/").glob("*.doc"):
                try:
                    # print(f"Script running for: {file}")

                    file_text = await doc_files_extractor(doc_path, file, word)
                    metadata = await MetadataProcessor(doc_path, file_text)
                    save_metadata_as_json(metadata, output_dir)
                    # print("i am waiting", len(file_text.split("\n")))
                    # print(f"Metadata extracted and saved for: {file}")
                except Exception as err:
                    print(f"Error processing {file}: {err}")

            else:
                print(f"File type NOT FOUND FOR {file}")
    except Exception as err:
        print(f"Check Error at main.py try block {err}")

    finally:
        word.Quit()


# Input and output paths
# input_directory = "path/documentsToProcess/case"
# input_directory = "path/documentsToProcess/A - DELIVERED"
# input_directory = "path/documentsToProcess/Processed_for_entity_extraction_Russell"
# input_directory = "path/documentsToProcess/B - FULL"
# input_directory = "path/documentsToProcess/C - MINUS _CASE SUMMARY"
# input_directory = "path/documentsToProcess/COMPLETE-F"
# input_directory = "path/documentsToProcess/WITHOUT CASE SUMMARY-F"
# input_directory = "path/documentsToProcess/COMPLETE D"
# input_directory = "path/documentsToProcess/COMPLETE E"
# input_directory = "path/documentsToProcess/WITHOUT CASE SUMMARY D"
# input_directory = "path/documentsToProcess/WITHOUT CASE SUMMARY E"
input_directory = "path/documentsToProcess/G"
output_directory = "path/to"
import asyncio

# print(f"{os.path.abspath(__file__)}")
asyncio.run(process_documents(input_directory, output_directory))
# start new python project
#  python -m venv .venv
# run to start a virtual environment
# .\.venv\Scripts\activate
