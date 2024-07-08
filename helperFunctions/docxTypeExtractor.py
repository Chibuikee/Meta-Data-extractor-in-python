import os

from docx import Document


def extract_docx(file_path: str) -> str:
    document = Document(file_path)
    text = [paragraph.text for paragraph in document.paragraphs]

    return "\n".join(text)


def extract_doc(file_path, word):
    #  Get the current working directory
    cwd = os.getcwd()
    # print("Current working directory:", cwd)
    # Get the absolute path of the file
    full_file_path = os.path.join(cwd, file_path)
    # print("Full path of the file:", full_file_path)
    # .abspath reconfigures the path to be computer complient
    absolute_path = os.path.abspath(full_file_path)
    # print("Absolute path of the file reworked:", absolute_path)
    try:
        # word = CDispath
        doc = word.Documents.Open(absolute_path)
        content = doc.Content.text
        # print(f"check out windows: {Content}")
        doc.Close(False)
        # this contains old formating, which causes bugs such as
        # absence of \n and presence of \r etc
        return content.replace("\r\n", "\n").replace("\r", "\n")
        # return content
    except Exception as err:
        print(f"Error processing {file_path}: {err}")
        return None


async def doc_files_extractor(doc_path, file, CDispath):

    try:
        # doc_path = os.path.join(input_dir)
        if file.lower().endswith(".docx"):
            return extract_docx(doc_path)
        elif file.lower().endswith(".doc"):
            return extract_doc(doc_path, CDispath)
            # print("ends with doc")
        else:
            print(f"Unsupported file type: {file}")
            # return None
    except Exception as err:
        print(f"Error processing {file}: {err}")
        return None


# Example usage
# result = doc_files_extractor("path/to/dir", "example.doc")
# print(result)
# import asyncio
