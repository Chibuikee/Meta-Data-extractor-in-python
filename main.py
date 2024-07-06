import json
import os

import win32com.client

# from helperFunctions.metadataExtractor import MetadataProcessor
from helperFunctions.docxTypeExtractor import doc_files_extractor

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
                try:
                    print(f"this is it{doc_path}")

                    file_text = await doc_files_extractor(doc_path, file)
                    # metadata = await MetadataProcessor(doc_path, file_text)
                    # save_metadata_as_json(metadata, output_dir)
                    print("i am waiting", len(file_text.split("\n")))
                    print(f"Metadata extracted and saved for: {file}")
                except Exception as err:
                    print(f"Error processing {file}: {err}")

            else:
                print(f"File type NOT FOUND FOR {file}")
    except Exception as err:
        print(f"Check Error at main.py try block {err}")


# Input and output paths
input_directory = "path/case"
output_directory = "path/to"
import asyncio

asyncio.run(process_documents(input_directory, output_directory))
# run to start a virtual environment
# .\.venv\Scripts\activate
# start new python project
#  python -m venv .venv
# create a django project
# pip install django
# pip install djangorestframework
# pip install django-cors-headers
# django-admin startproject chibs .
# python manage.py startapp EmployeeApp
# pip install python-dotenv
# start python "py", quit python "quit()"

# run server for the api
# python manage.py runserver


# database management
# pip install psycopg2-binary
# python manage.py makemigrations
# python manage.py migrate
# python manage.py createsuperuser
