#import mysql.connector
#from mysql.connector import Error


def do_a_list():
    listOfQuestions=[]
    newList=[]
    #used to open and readfiles line by line everything will be stored in a list composed of lines
    def readFiles():
        listOfLines=[]
        with open('C:\\Users\\Dell\\PycharmProjects\\M1_project\\metanit\\hello\\questions.txt','r') as reader:
            for line in reader:
                listOfLines.append(line)
        return listOfLines

    #needed to find and remove the tags
    def find_specificStr(txt, str1, n):
        parts = txt.split(str1, n + 1)
        if len(parts) <= n + 1:
              return -1
        return len(txt) - len(parts[-1]) - len(str1)

    def compare(listOfLines):
        length = len(listOfLines)
        i=0
        tagQ="$!Q"
        tagEQ = "$!EQ"
        while(i<length):
            sup=""
            if(listOfLines[i].find(tagQ)!=-1):
                lines=[]
                lines.append(listOfLines[i])
                while(listOfLines[i].find(tagEQ)==-1):
                    i+=1
                    lines.append(listOfLines[i])

                for line in lines:
                    sup+=line
                listOfQuestions.append(sup)
            i+=1
        for question in listOfQuestions:
            question=question[find_specificStr(question, '$', 1)+1:]
            question=question.replace('$!EQ$','')
            newList.append(question)

    compare(readFiles())
    return newList


data=do_a_list()
print(data)
""" 

def databaseConnection(databaseName,username,password,hostName):
    connection = None
    try:
        connection = mysql.connectot.connect(
            host=hostName,
            user=username,
            passwd=password,
            database=databaseName
        )
    except Error as error:
        print(f"Error: '{error}'")
    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as error:
        print(f"Error: '{error}'")


"""