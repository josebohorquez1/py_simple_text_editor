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
        file_menu_print = file_menu.Append(wx.ID_PRINT, "Print", "Prints the file")
        file_menu.AppendSeparator()
        file_menu_exit = file_menu.Append(wx.ID_EXIT, "E&xit", "Closes the application.")
        menu_bar.Append(file_menu, "&File")
        self.Bind(wx.EVT_MENU, self.onOpen, file_menu_open)
        self.Bind(wx.EVT_MENU, self.onSave, file_menu_save)
        self.Bind(wx.EVT_MENU, self.onSaveAs, file_menu_save_as)
        self.Bind(wx.EVT_MENU, self.onPrint, file_menu_print)
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
    #Function that prints the text using a printer
    def onPrint(self, evt):
        printer = wx.Printer()
        print_dlg = wx.PrintDialog(self)
        if print_dlg.ShowModal() == wx.ID_OK:
            print_data = print_dlg.GetPrintData()
            printout = TextPrintout(self.text_control.GetValue())
            printer.Print(parent=self, printout=printout)
            printout.Destroy()
        print_dlg.Destroy()
    #For the exit menu item of the file menu which closes the window; in addition, the function checks if there have been changes to the file and asks user to save or not saved and also checks if there is text but no file name and will ask user to save or not save.
    def onExit(self, evt):
        if self.current_file_path != "":
            with open(self.current_file_path, 'r') as file:
                current_contents = file.read()
            if current_contents != self.text_control.GetValue():
                dlg = wx.MessageDialog(parent=self, caption="Save Changes", message="Do you want to save changes to " + os.path.basename(self.current_file_path) + "?", style=wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION)
                result = dlg.ShowModal()
                if result == wx.ID_YES:
                    self.onSave(evt)
                    self.Close(True)
                    sys.exit()
                elif result == wx.ID_NO:
                    self.Close(True)
                    sys.exit()
                else:
                    dlg.Destroy()
                    return
        else:
            if self.text_control.GetValue():
                dlg = wx.MessageDialog(parent=self, caption="Save Changes", message="Do you want to save changes to Untitled?", style=wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION)
                result = dlg.ShowModal()
                if result == wx.ID_YES:
                    self.onSave(evt)
                    self.Close(True)
                    sys.exit()
                elif result == wx.ID_NO:
                    self.Close(True)
                    sys.exit()
                else:
                    dlg.Destroy()
                    return
            else:
                self.Close(True)
                sys.exit()
    #Keyboard-based events
class TextPrintout(wx.Printout):
    def __init__(self, text):
        wx.Printout.__init__(self)
        self.text = text
        self.page_text = ""
        self.line = []
    def OnPreparePrinting(self):
        dc = self.GetDC()
        dc.SetFont(self.GetFont())
        w, h, = dc.GetSize()
        line_height = dc.getCharHeight()
        lines_per_page = int(h / line_height)
        self.lines = self.text.split('\n')
        self.page_text = '\n'.join[: lines_per_page]
        return True
    def hasPages(self, page):
        return page <= len(self.lines)
    def OnPrintPage(self, page):
        dc = self.GetDC()
        dc.SetFont(self.GetFont())
        margin_x = 20
        margin_y = 20
        _, page_height = dc.GetSize()
        printing_area_height = page_height - 2 * margin_y
        line_height = dc.GetCharHeight()
        lines_per_page = int(printing_area_height / line_height)
        start_line = (page - 1) * lines_per_page
        y = margin_y
        end_line = min(start_line + lines_per_page, len(self.lines))
        for line in self.lines[start_line:end_line]:
            dc.DrawText(line, margin_x, y)
            y += line_height
        return True
    #Creating the window and running the main loop.
app = wx.App(False)
window = MainWindow(None, "Untitled - Text Editor")
app.MainLoop()