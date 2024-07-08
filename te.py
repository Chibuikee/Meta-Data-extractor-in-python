import os
import re

import win32com.client

# this is for testing and debugging


#  Get the current working directory
cwd = os.getcwd()
print("Current working directory:", cwd)

# Construct the relative path to the file
relative_path = "path/case/MORGAN V SMALLY.doc"

# Get the absolute path of the file
file_path = os.path.join(cwd, relative_path)
print("Absolute path of the file:", file_path)

# .abspath reconfigures the path to be computer complient
absolute_path = os.path.abspath(file_path)
print("Absolute path of the file reworked:", absolute_path)


def read_doc(file_path):
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    doc = word.Documents.Open(file_path)
    content = doc.Content.Text
    doc.Close(False)
    word.Quit()
    return content


file_path = "path/case"
# print(
#     read_doc(
#         "C:\chibs\Desktop\chibscodes\python\path\case\A.G OF CROSS RIVER STATE V A.G OF THE FEDERATION.doc"
#     )
# )
# print(read_doc(os.path.join(file_path, "A.G OF CROSS RIVER STATE V A.G OF THE FEDERATION.doc")))
# C:\chibs\Desktop\chibscodes\python\path\case\MORGAN V SMALLY.doc
citation_regex1 = r"LEX\s?.*\d\w?"
# citation_regex1 = r"LEX\s.*?(-|–).*?\d+\b"
text1 = """MORGAN
    V
    SMALLY
    COURT OF APPEAL, CIVIL DIVISION
    23 JANUARY 2004
    [2002] ALL ER (D) 107 (NOV)
    LEX (2002) – ALL E.R 107

    OTHER CITATIONS
    3PLR/2004/69 (SC)
    BEFORE: WARD, MUMMERY AND RIX LJJ
    """
citation_match = re.search(citation_regex1, text1, re.ASCII)
# citation_match = re.findall(citation_regex1, to_ascii(text1), flags=re.UNICODE)
print(f"answer:{ citation_match}")
# print(f"answer:{[i for i in citation_match]}")
