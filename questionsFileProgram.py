import sqlite3
import wx
from sqlite3 import Error


#IMPORT DATA FUNCTIONS



nameCourse=''           #used to save the course's name
descCourse=''           #used to save the course's description
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
        global nameCourse
        global descCourse
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
                
            if(opTag=="$!NCO"): 
                nameCourse = temp
            elif(opTag=="$!DCO"): descCourse = temp
            elif(opTag=="$!NCH"): 
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
        global nameCourse
        global descCourse
        global numChap,numQues
        nameCourse=nameCourse[find_specificStr(nameCourse, '$', 1)+1:]
        nameCourse=nameCourse.replace("$!ENCO$",'')
        descCourse=descCourse[find_specificStr(descCourse, '$', 1)+1:]
        descCourse=descCourse.replace("$!EDCO$",'')
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
        global nameCourse
        global descCourse
        global numChap,numQues
        length = len(listOfLines)
        i=0
        opTags=["$!NCO","$!DCO","$!NCH","$!DCH","$!Q"]
        clTags=["$!ENCO","$!EDCO","$!ENCH","$!EDCH","$!EQ"]
        while(i<length):
            i=findTag(listOfLines,i,opTags[0],clTags[0])
            i=findTag(listOfLines,i,opTags[1],clTags[1])
            i=findTag(listOfLines,i,opTags[2],clTags[2])
            i=findTag(listOfLines,i,opTags[3],clTags[3])
            i=findTag(listOfLines,i,opTags[4],clTags[4])
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



#This function will save the course's data in the database if the verification function doesn't find it in the DB        
def create_course(connection, course):
    sql = ''' INSERT INTO catalog_course(title,description)
              VALUES(?,?) '''
    cur = connection.cursor()
    verification = verify_data(connection, course,0)
    if verification==True:
        cur.execute(sql, course)
        connection.commit()



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

    with connection:
        num =0
        course=(nameCourse,descCourse)
        create_course(connection,course)

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




#INTERFACE'S FUNCTIONS


#Class that creates the main menu interface
class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        self.dirname=''

        # A "-1" in the size parameter instructs wxWidgets to use the default size.
        # In this case, we select 200px width and the default height.
        wx.Frame.__init__(self, parent, title=title, size=(800,800))
        panel = wx.Panel(self)        
        my_sizer = wx.BoxSizer(wx.VERTICAL)  
        self.StaticText = wx.StaticText(panel,label='EASY LEARNING')      
        my_sizer.Add(self.StaticText, 0, wx.ALL | wx.CENTER, 5)           
        btn_file = wx.Button(panel, label='Open the server')
        btn_file.Bind(wx.EVT_BUTTON, self.on_press_choose)
        my_sizer.Add(btn_file, 0, wx.ALL | wx.CENTER, 5) 
        my_btn = wx.Button(panel, label='Import the file')
        my_btn.Bind(wx.EVT_BUTTON, self.OnImport)
        my_sizer.Add(my_btn, 0, wx.ALL | wx.CENTER, 5)
         
        panel.SetSizer(my_sizer) 
       
        self.Show()

    def on_press_choose(self,event):
        self.Close(True)


    def OnExit(self,e):
        self.Close(True)  # Close the frame.

    def OnImport(self,e):
        frame=FrameAddFile(self,MainWindow)


#Class corresponding to the "adding a file" page
class FrameAddFile(wx.Frame):    
    def __init__(self,parent,title):
        self.dirname=''

        # A "-1" in the size parameter instructs wxWidgets to use the default size.
        # In this case, we select 200px width and the default height.
        wx.Frame.__init__(self, parent, title="Import a file", size=(800,800))
        panel = wx.Panel(self)        
        my_sizer = wx.BoxSizer(wx.VERTICAL)  
        self.StaticText = wx.StaticText(panel,label='Write the location of the question file or search it by clicking on the "Choose a file" button')      
        my_sizer.Add(self.StaticText, 0, wx.ALL | wx.CENTER, 5)
        self.text_ctrl = wx.TextCtrl(panel)
        my_sizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND, 5)               
        btn_file = wx.Button(panel, label='Choose a file')
        btn_file.Bind(wx.EVT_BUTTON, self.on_press_choose)
        my_sizer.Add(btn_file, 0, wx.ALL | wx.CENTER, 5) 
        my_btn = wx.Button(panel, label='Import the file')
        my_btn.Bind(wx.EVT_BUTTON, self.on_press)
        my_sizer.Add(my_btn, 0, wx.ALL | wx.CENTER, 5)
        btn_close = wx.Button(panel, label='Close')
        btn_close.Bind(wx.EVT_BUTTON, self.on_press_close)
        my_sizer.Add(btn_close, 0, wx.ALL | wx.CENTER, 5)
        panel.SetSizer(my_sizer) 
        self.Show()  # Show the frame.

    def on_press(self, event):
        value = self.text_ctrl.GetValue()
        if not value:
            print("You didn't enter anything!")
        else:
            do_a_list(value)
            saveDB()
            frame=FrameImportFinish(self,FrameAddFile)

    def on_press_choose(self,event):
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            self.text_ctrl.AppendText(self.dirname+"\\"+self.filename)
        dlg.Destroy()

    def on_press_close(self, event):
        self.Close(True)

#Class corresponding to the message written at the end of the importation
class FrameImportFinish(wx.Frame):    
    def __init__(self,parent,title):
        self.dirname=''

        # A "-1" in the size parameter instructs wxWidgets to use the default size.
        # In this case, we select 200px width and the default height.
        wx.Frame.__init__(self, parent, title="Importation finished", size=(800,800))
        panel = wx.Panel(self)        
        my_sizer = wx.BoxSizer(wx.VERTICAL)  
        self.StaticText = wx.StaticText(panel,label='The file has successfully been implemented !')      
        my_sizer.Add(self.StaticText, 0, wx.ALL | wx.CENTER, 5)            
        btn_file = wx.Button(panel, label='Close')
        btn_file.Bind(wx.EVT_BUTTON, self.on_press)
        my_sizer.Add(btn_file, 0, wx.ALL | wx.CENTER, 5) 
        panel.SetSizer(my_sizer) 
        self.Show()  # Show the frame.

    def on_press(self, event):
        self.Close(True)



#function that creates the application where all classes can be used to create windows
def interface():
    app = wx.App()   # Create a new app
    frame = MainWindow(None,"Main menu") # A Frame is a top-level window
    app.MainLoop() #start the application's MainLoop whose role is to handle the events.


def start():
    interface()

start()