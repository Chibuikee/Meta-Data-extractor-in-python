import os
import win32com.client



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

file_path = 'path/case'
print(read_doc("C:\chibs\Desktop\chibscodes\python\path\case\A.G OF CROSS RIVER STATE V A.G OF THE FEDERATION.doc"))
# print(read_doc(os.path.join(file_path, "A.G OF CROSS RIVER STATE V A.G OF THE FEDERATION.doc")))
# C:\chibs\Desktop\chibscodes\python\path\case\MORGAN V SMALLY.doc
