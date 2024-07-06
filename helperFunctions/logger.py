def loggerToFile(newtext):
    with open("./output/extracttext.txt", "w") as wf:
        # with open("./output/extracttext.txt", "w", encoding="utf-8") as wf:
        wf.write(newtext)
