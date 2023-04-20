# import sqlite3
# import wx
# from sqlite3 import Error

# IMPORT DATA FUNCTIONS


numChap = -1  # variable that indicates the number of chapters in a course -1
numQues = 0  # variable that indicates the number of questions in a chapter
listOfNameQuestion = []  # used to save the names of the questions
listOfDescQuestion = []  # used to save the descriptions of the questions
listOfChapters = []  # used to save the chapters
nbChapters = []  # list where one object in the list correspond to the number of chapters in one question


# This function reads the data in each line of the files and stores it in a list that is returned at the end
def do_a_list(file):
    newList = []

    # used to open and readfiles line by line everything will be stored in a list composed of lines
    def readFiles():
        listOfLines = []
        with open(file, 'r') as reader:
            for line in reader:
                listOfLines.append(line)
        return listOfLines

    # this function finds and removes the tags
    def find_specificStr(txt, str1, n):
        parts = txt.split(str1, n + 1)
        if len(parts) <= n + 1:
            return -1
        return len(txt) - len(parts[-1]) - len(str1)

    # This function compares the line that needs to be sorted to different tags and save the lines to the correct list/string
    def findTag(listOfLines, i, opTag, clTag):
        global numChap, numQues
        temp = ""
        if (listOfLines[i].find(opTag) != -1):
            lines = []
            lines.append(listOfLines[i])
            while (listOfLines[i].find(clTag) == -1):
                i += 1
                lines.append(listOfLines[i])

            for line in lines:
                temp += line

            if (opTag == "$!NQ"):
                listOfNameQuestion.append(temp)
                numChap += 1
                nbChapters.append(numQues)
            elif (opTag == "$!DQ"):
                listOfDescQuestion.append(temp)
            elif (opTag == "$!CH"):
                listOfChapters.append(temp)
                numQues += 1
                nbChapters[numChap] = numQues
        return i

    # This function takes all the data stored after the sorting function and remove all tags from the strings
    def removeTag():
        global numChap, numQues
        lenCh = len(listOfNameQuestion)
        for i in range(lenCh):
            listOfNameQuestion[i] = listOfNameQuestion[i][find_specificStr(listOfNameQuestion[i], '$', 1) + 1:]
            listOfNameQuestion[i] = listOfNameQuestion[i].replace('$!ENQ$', '')
            listOfDescQuestion[i] = listOfDescQuestion[i][find_specificStr(listOfDescQuestion[i], '$', 1) + 1:]
            listOfDescQuestion[i] = listOfDescQuestion[i].replace('$!EDQ$', '')
            listOfDescQuestion[i] = listOfDescQuestion[i].replace("\n", '')
            listOfDescQuestion[i] = listOfDescQuestion[i].strip()
            listOfNameQuestion[i] = listOfNameQuestion[i].replace("\n", '')
            listOfNameQuestion[i] = listOfNameQuestion[i].strip()
        lenQ = len(listOfChapters)
        for i in range(lenQ):
            listOfChapters[i] = listOfChapters[i][find_specificStr(listOfChapters[i], '$', 1) + 1:]
            listOfChapters[i] = listOfChapters[i].replace('$!ECH$', '')
            listOfChapters[i] = listOfChapters[i].replace("\n", '')
            listOfChapters[i] = listOfChapters[i].strip()

    # This is the main function that starts the sorting of the data and the removal of the tags
    def compare(listOfLines):
        global numChap, numQues
        length = len(listOfLines)
        i = 0
        opTags = ["$!NQ", "$!DQ", "$!CH"]
        clTags = ["$!ENQ", "$!EDQ", "$!ECH"]
        while (i < length):
            i = findTag(listOfLines, i, opTags[0], clTags[0])
            i = findTag(listOfLines, i, opTags[1], clTags[1])
            i = findTag(listOfLines, i, opTags[2], clTags[2])
            i += 1
        removeTag()

    compare(readFiles())
    return listOfNameQuestion, listOfDescQuestion, listOfChapters, nbChapters

