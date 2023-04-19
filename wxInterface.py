import wx

import questionsFileProgram as qf
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
            qf.do_a_list(value)
            qf.saveDB()
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