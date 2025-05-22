# import os
# import re

# import win32com.client

# # this is for testing and debugging


# #  Get the current working directory
# cwd = os.getcwd()
# print("Current working directory:", cwd)

# # Construct the relative path to the file
# relative_path = "path/case/MORGAN V SMALLY.doc"

# # Get the absolute path of the file
# file_path = os.path.join(cwd, relative_path)
# print("Absolute path of the file:", file_path)

# # .abspath reconfigures the path to be computer complient
# absolute_path = os.path.abspath(file_path)
# print("Absolute path of the file reworked:", absolute_path)


# def read_doc(file_path):
#     word = win32com.client.Dispatch("Word.Application")
#     word.Visible = False
#     doc = word.Documents.Open(file_path)
#     content = doc.Content.Text
#     doc.Close(False)
#     word.Quit()
#     return content


# file_path = "path/case"
# # print(
# #     read_doc(
# #         "C:\chibs\Desktop\chibscodes\python\path\case\A.G OF CROSS RIVER STATE V A.G OF THE FEDERATION.doc"
# #     )
# # )
# # print(read_doc(os.path.join(file_path, "A.G OF CROSS RIVER STATE V A.G OF THE FEDERATION.doc")))
# # C:\chibs\Desktop\chibscodes\python\path\case\MORGAN V SMALLY.doc
# citation_regex1 = r"LEX\s?.*\d\w?"
# # citation_regex1 = r"LEX\s.*?(-|–).*?\d+\b"
# text1 = """MORGAN
#     V
#     SMALLY
#     COURT OF APPEAL, CIVIL DIVISION
#     23 JANUARY 2004
#     [2002] ALL ER (D) 107 (NOV)
#     LEX (2002) – ALL E.R 107

#     OTHER CITATIONS
#     3PLR/2004/69 (SC)
#     BEFORE: WARD, MUMMERY AND RIX LJJ
#     """
# citation_match = re.search(citation_regex1, text1, re.ASCII)
# # citation_match = re.findall(citation_regex1, to_ascii(text1), flags=re.UNICODE)
# print(f"answer:{ citation_match}")
# # print(f"answer:{[i for i in citation_match]}")
name = "Emmanuel"


# sentence1 = f"my name is {name}"
# sentence2 = f"my name is {name}"
# sentence3 = f"my name is {name}"
# print("my name is Emmanuel")
# print("my name is Emmanuel")
# print("my name is Emmanuel")
# print("my name is Emmanuel")

# import redis
import redis

client = redis.Redis(host="localhost", port=6379, db=0)
print(client.ping())  # Should return True if connected


# async def test_redis():
#     client = redis.from_url("redis://localhost:6379")
#     await client.ping()
#     print("Connected to Redis!")


# test_redis()
# import asyncio

# asyncio.run(test_redis())

import json
import os``
from pathlib import Path


def process_files(input_folder, output_folder):
    """
    Process files from input folder and create JSON files in output folder.

    Args:
        input_folder (str): Path to input folder
        output_folder (str): Path to output folder
    """
    try:
        # Check if input folder exists
        folder = Path(input_folder)
        if not folder.exists():
            # if not os.path.exists(input_folder):
            raise FileNotFoundError(f"Input folder '{input_folder}' does not exist")

        # Get list of files in input folder
        files = folder.iterdir()
        # files = os.listdir(input_folder)
        if not files:
            print(f"No files found in '{input_folder}'")
            return

        # Create output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            print(f"Created output folder: {output_folder}")

        # Process each file
        for file in files:
            # Get filename without extension
            # lists all the parts of the path
            filename = file.stem
            # filename = file.parts[-1]
            # filename = os.path.splitext(file)[0]
            # print(filename)
            # Create output JSON path
            # json_path = os.path.join(output_folder, f"{filename}.json")
            # join path and create file path without writing to it
            json_path = Path().joinpath(output_folder, f"{filename}.json").touch()
            # print(json_path)
            # Create empty JSON data (you can modify this based on your needs)
            # json_data = {
            #     "original_filename": file,
            #     "filename_no_ext": filename,
            #     # Add more data as needed
            # }

            # Write JSON file
            # with open(json_path, "w") as f:

            #     json.dump(json_data, f, indent=4)

            # print(f"Created JSON file: {json_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
        # print(f"An error occurred: {str(e)}")


# Example usage
# if _name_ == "_main_":
# Replace these with your actual folder paths
input_folder = "path/case_md_batch2"
output_folder = "path/case_md_batch2_extracted"


# process_files(input_folder, output_folder)
go = [1, 3, 6, 9]
foo = iter(go)
# print(next(foo))


def gi(hi, a):
    aa = hi + a
    yield aa


asa = gi(5, 10)
le = [i for i in asa]
# print(le)
