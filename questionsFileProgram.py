import sqlite3
import wx
from sqlite3 import Error


#IMPORT DATA FUNCTIONS


numChap=-1              #variable that indicates the number of chapters in a course -1
numQues=0               #variable that indicates the number of questions in a chapter 
listOfNameChapter=[]    #used to save the names of the chapters
listOfDescChapter=[]    #used to save the descriptions of the chapters
listOfQuestions=[]      #used to save the questions
nbQuestions=[]          #list where one object in the list correspond to the number of questions in one chapter



#This function reads the data in each line of the files and stores it in a list that is returned at the end
def do_a_list(file):
    newList=[]

    #used to open and readfiles line by line everything will be stored in a list composed of lines
    def readFiles():
        listOfLines=[]
        with open(file,'r') as reader:
            for line in reader:
                listOfLines.append(line)
        return listOfLines

    #this function finds and removes the tags
    def find_specificStr(txt, str1, n):
        parts = txt.split(str1, n + 1)
        if len(parts) <= n + 1:
              return -1
        return len(txt) - len(parts[-1]) - len(str1)

    #This function compares the line that needs to be sorted to different tags and save the lines to the correct list/string
    def findTag(listOfLines,i,opTag,clTag):
        global numChap,numQues
        temp=""
        if(listOfLines[i].find(opTag)!=-1):
            lines=[]
            lines.append(listOfLines[i])
            while(listOfLines[i].find(clTag)==-1):
                i+=1
                lines.append(listOfLines[i])

            for line in lines:
                temp+=line
                
            if(opTag=="$!NCH"): 
                listOfNameChapter.append(temp)
                numChap+=1
                nbQuestions.append(numQues)
            elif(opTag=="$!DCH"): listOfDescChapter.append(temp)
            elif(opTag=="$!Q"): 
                listOfQuestions.append(temp)
                numQues+=1
                nbQuestions[numChap]=numQues
        return i
            
    #This function takes all the data stored after the sorting function and remove all tags from the strings
    def removeTag():
        global numChap,numQues
        lenCh=len(listOfNameChapter)
        for i in range(lenCh):
            listOfNameChapter[i]=listOfNameChapter[i][find_specificStr(listOfNameChapter[i], '$', 1)+1:]
            listOfNameChapter[i]=listOfNameChapter[i].replace('$!ENCH$','')
            listOfDescChapter[i]=listOfDescChapter[i][find_specificStr(listOfDescChapter[i], '$', 1)+1:]
            listOfDescChapter[i]=listOfDescChapter[i].replace('$!EDCH$','')
        lenQ=len(listOfQuestions)
        for i in range(lenQ):
            listOfQuestions[i]=listOfQuestions[i][find_specificStr(listOfQuestions[i], '$', 1)+1:]
            listOfQuestions[i]=listOfQuestions[i].replace('$!EQ$','')
            
    #This is the main function that starts the sorting of the data and the removal of the tags
    def compare(listOfLines):
        global numChap,numQues
        length = len(listOfLines)
        i=0
        opTags=["$!NCH","$!DCH","$!Q"]
        clTags=["$!ENCH","$!EDCH","$!EQ"]
        while(i<length):
            i=findTag(listOfLines,i,opTags[0],clTags[0])
            i=findTag(listOfLines,i,opTags[1],clTags[1])
            i=findTag(listOfLines,i,opTags[2],clTags[2])
            i+=1
        removeTag()
        

    compare(readFiles())
    



#DATABASE'S FUNCTIONS


# This function creates and returns a connection to the database
def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(db_file)
    except Error as err:
        print(err)

    return connection


# This function verifies if the data from the question file that is being imported isn't already saved in the database 
def verify_data(connection,infos,id):
    if id == 0:         #This part verifies if the course is already imported
        title=infos[0]
        desc=infos[1]
        sql ="SELECT * from catalog_course where title ='%s' and description ='%s'" % (title, desc)
        cur= connection.cursor()
        cur.execute(sql)
        if len(cur.fetchall()) == 0:
            return True
        else:
            return False
    if id == 1:         #This part verifies if the chapter is already imported
        title=infos[0]
        desc=infos[1]
        sql ="SELECT * from catalog_chapter where title ='%s' and description ='%s'" % (title, desc)
        cur= connection.cursor()
        cur.execute(sql)
        if len(cur.fetchall()) == 0:
            return True
        else:
            return False
    
    if id == 2:         #This part verifies if the question is already imported
        title=infos[0]
        desc=infos[1]
        pts=infos[2]
        sql ="SELECT * from catalog_question where title ='%s' and question ='%s' and answer_points='%d'" % (title, desc, pts)
        cur= connection.cursor()
        cur.execute(sql)
        if len(cur.fetchall()) == 0:
            return True
        else:
            return False




#This function will save the chapter's data in the database if the verification function doesn't find it in the DB
def create_chapter(connection, chapter):
    sql = ''' INSERT INTO catalog_chapter(title,description)
              VALUES(?,?) '''
    cur = connection.cursor()
    verification = verify_data(connection,chapter,1)
    if verification==True:
        cur.execute(sql, chapter)
        connection.commit()
        return cur.lastrowid
    else:
        sql="SELECT id from catalog_chapter where title='%s' and description ='%s'" % (chapter[0],chapter[1])
        cur.execute(sql)
        connection.commit()
        fetchID=cur.fetchone()
        return fetchID[0]


#This function will save the question's data in the database if the verification function doesn't find it in the DB
def create_question(connection, question):
    sql = ''' INSERT INTO catalog_question(title, question, answer_points)
              VALUES(?,?,?) '''
    cur = connection.cursor()
    verification = verify_data(connection,question,2)
    if verification==True:
        cur.execute(sql, question)
        connection.commit()
        return cur.lastrowid
    else:
        sql="SELECT id from catalog_question where title='%s' and question ='%s' and answer_points='%d'" % (question[0],question[1],question[2])
        cur.execute(sql)
        fetchID=cur.fetchone()
        return fetchID[0]
    


#This function links the queston to the chapter it was written inside of.
def link_ChQ(connection,idCh,idQ):
    sql = ''' INSERT or REPLACE INTO catalog_question_chapters(question_id,chapter_id)
              VALUES(?,?) '''
    cur = connection.cursor()
    cur.execute(sql, (idQ,idCh))
    connection.commit()


#This is the main function to save the data in the DB, it will call every function seen before to import the data
def saveDB():
    database =r"C:\Users\alban\OneDrive\Bureau\project\locallibrary\db.sqlite3"
    connection = create_connection(database)
    print('OK')
    with connection:
        num =0

        for i in range(len(listOfNameChapter)):
            chapter=(listOfNameChapter[i],listOfDescChapter[i])
            idCh=create_chapter(connection,chapter)
            
            for m in range(num,nbQuestions[i]):
                question=(listOfQuestions[m],listOfQuestions[m],5)
                idQ=create_question(connection,question)
                if(idQ !=None):
                    link_ChQ(connection,idCh,idQ)
                num=nbQuestions[i]
    connection.close()




