import wx
import os
import sys
#The main window class
class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        #Initializing the parent class
        wx.Frame.__init__(self, parent, title=title, size=(200, 100))
        #Initializing the main window user interface.
        self.current_file_path = ""
        self.initUI()
        self.Show(True)
    #function to initialize the user interface.
    def initUI(self):
        self.createMenuBar()
        self.createTextBox()
        self.CreateStatusBar()
    #Creating the menu bar
    def createMenuBar(self):
        menu_bar = wx.MenuBar()
        self.fileMenu(menu_bar)
        self.SetMenuBar(menu_bar)
    #The function to create the file menu within the menubar, and the event handling for the file menu items.
    def fileMenu(self, menu_bar: wx.MenuBar):
        file_menu = wx.Menu()
        file_menu_open = file_menu.Append(wx.ID_OPEN, "&Open", "Opens a file.")
        file_menu.AppendSeparator()
        file_menu_save = file_menu.Append(wx.ID_SAVE, "&Save", "Saves the current file",)
        file_menu.AppendSeparator()
        file_menu_save_as = file_menu.Append(wx.ID_SAVEAS, "&Save As", "Saves a new file")
        file_menu.AppendSeparator()
        file_menu_exit = file_menu.Append(wx.ID_EXIT, "E&xit", "Closes the application.")
        menu_bar.Append(file_menu, "&File")
        self.Bind(wx.EVT_MENU, self.onOpen, file_menu_open)
        self.Bind(wx.EVT_MENU, self.onSave, file_menu_save)
        self.Bind(wx.EVT_MENU, self.onSaveAs, file_menu_save_as)
        self.Bind(wx.EVT_MENU, self.onExit, file_menu_exit)
    #Creating the textbox and the wrapping
    def createTextBox(self):
        textbox = wx.StaticBox(self, label="Text Editor")
        self.text_control = wx.TextCtrl(textbox, style=wx.TE_MULTILINE | wx.TE_PROCESS_TAB | wx.TE_NOHIDESEL | wx.HSCROLL | wx.VSCROLL)
        sizer = wx.StaticBoxSizer(textbox, wx.VERTICAL)
        sizer.Add(self.text_control, flag=wx.EXPAND | wx.ALL, proportion=1, border=5)
        self.SetSizer(sizer)
    #File menu functions.
    #For the open file menu item; also changes the window title depending on the name of the file.
    def onOpen(self, evt):
        wildcard = "Text documents (*.txt)|*.txt|All files (*.*)|*.*"
        style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        dlg = wx.FileDialog(self, "Open", wildcard= wildcard, style=style)
        if (dlg.ShowModal() == wx.ID_OK):
            file_path = dlg.GetPath()
            self.current_file_path = file_path
        with open(file_path, 'r') as file:
            contents = file.read()
            self.text_control.SetValue(contents)
        dlg.Destroy()
        self.SetTitle(os.path.basename(self.current_file_path) + "- Text Editor")
    #Function to save the current file; if file exists, will override the contents with the new contents; if the file does not exist, will create and open the save as dialogue box and change the window title to include the file name.
    def onSave(self, evt):
        if self.current_file_path:
            with open(self.current_file_path, 'w') as file:
                file.write(self.text_control.GetValue())
        else:
            wildcard = "Text documents(*.txt)|*.txt|All files(*.*)|*.*"
            style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
            dlg = wx.FileDialog(self, "Save as", wildcard=wildcard, style=style)
            if (dlg.ShowModal() == wx.ID_OK):
                file_path = dlg.GetPath()
                self.current_file_path = file_path
            with open(file_path, 'w') as file:
                file.write(self.text_control.GetValue())
            dlg.Destroy()
            self.SetTitle(os.path.basename(self.current_file_path) + "- Text Editor")
    #For the save as function which creates a new file or saves the same file with a new different file name, and changes the window title with the new file name.
    def onSaveAs(self, evt):
        wildcard = "Text documents(*.txt)|*.txt|All files(*.*)|*.*"
        style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        dlg = wx.FileDialog(self, "Save as", wildcard=wildcard, style=style)
        if (dlg.ShowModal() == wx.ID_OK):
            file_path = dlg.GetPath()
            self.current_file_path = file_path
        with open(file_path, 'w') as file:
            file.write(self.text_control.GetValue())
        dlg.Destroy()
        self.SetTitle(os.path.basename(self.current_file_path) + "- Text Editor")
    #For the exit menu item of the file menu which closes the window.
    def onExit(self, evt):
        self.Close(True)
        sys.exit()
    #Keyboard-based events
#Creating the window and running the main loop.
app = wx.App(False)
window = MainWindow(None, "Untitled - Text Editor")
app.MainLoop()