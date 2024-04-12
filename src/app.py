import wx
import os
import sys
#A single tab within the application; also used to create new tabs.
class Tab(wx.Panel):
    def __init__(self, parent):
        #Initializing a panel and creating the interface for the panel which will be used for each tab.
        wx.Panel.__init__(self, parent)
        textbox = wx.StaticBox(self, label="Text Editor")
        self.text_control = wx.TextCtrl(textbox, style=wx.TE_MULTILINE | wx.TE_PROCESS_TAB | wx.TE_NOHIDESEL | wx.HSCROLL | wx.VSCROLL)
        sizer = wx.StaticBoxSizer(textbox, wx.VERTICAL)
        sizer.Add(self.text_control, flag=wx.EXPAND | wx.ALL, proportion=1, border=5)
        self.SetSizer(sizer)
    #Function to get the text control of the tab.
    def getTextControl(self):
        return self.text_control
#The main window class
class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        #Initializing the parent class
        self.window = wx.Frame()
        self.window.__init__(parent, title=title, size=(200, 100))
        self.panel = wx.Panel(self.window)
        self.notebook = wx.Notebook(self.panel)
        #Initializing the main window user interface, and adding a event handler that changes the application title based on the tab title.
        self.current_file_paths = []
        self.initUI()
        self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onTabChange, self.notebook)
        self.window.Show(True)
    #function to initialize the user interface.
    def initUI(self):
        self.createMenuBar()
        self.window.CreateStatusBar()
        self.createTab()
    #Function to create a new tab.
    def createTab(self):
        tab = Tab(self.notebook)
        self.notebook.AddPage(tab, "Untitled")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.notebook, 1, wx.EXPAND)
        self.current_file_paths.append("")
        tab.getTextControl().SetFocus()
    #Function to set the window's title based on the title of the tab.
    def onTabChange(self, evt):
        title = self.notebook.GetPageText(self.notebook.GetSelection()) + " - Text Editor"
        self.window.SetTitle(title=title)
    #Function to retrieve the text control from the current selected tab
    def getTextControlFromTab(self):
        current_tab_index = self.notebook.GetSelection()
        current_tab = self.notebook.GetPage(current_tab_index)
        if isinstance(current_tab, Tab):
            return current_tab.getTextControl()
        return None
    #Creating the menu bar
    def createMenuBar(self):
        menu_bar = wx.MenuBar()
        FileMenu(self, menu_bar)
        self.window.SetMenuBar(menu_bar)
class FileMenu(wx.Menu, MainWindow):
    def __init__(self, main_window : MainWindow, menu_bar : wx.MenuBar):
        wx.Menu.__init__(self)
        self.menu_bar = menu_bar
        self.main_window = main_window
        file_menu_new_tab = self.Append(wx.ID_ANY, "New Tab", "Opens a new tab.")
        self.AppendSeparator()
        file_menu_new_window = self.Append(wx.ID_ANY, "New Window", "Opens a new window.")
        self.AppendSeparator()
        file_menu_open = self.Append(wx.ID_OPEN, "&Open", "Opens a file.")
        self.AppendSeparator()
        file_menu_save = self.Append(wx.ID_SAVE, "&Save", "Saves the current file",)
        self.AppendSeparator()
        file_menu_save_as = self.Append(wx.ID_SAVEAS, "&Save As", "Saves a new file")
        self.AppendSeparator()
        file_menu_print = self.Append(wx.ID_PRINT, "Print", "Prints the file")
        self.AppendSeparator()
        file_menu_exit = self.Append(wx.ID_EXIT, "E&xit", "Closes the application.")
        self.menu_bar.Append(self, "&File")
        self.main_window.window.Bind(wx.EVT_MENU, self.onNewTab, file_menu_new_tab)
        self.main_window.window.Bind(wx.EVT_MENU, self.onNewWindow, file_menu_new_window)
        self.main_window.window.Bind(wx.EVT_MENU, self.onOpen, file_menu_open)
        self.main_window.window.Bind(wx.EVT_MENU, self.onSave, file_menu_save)
        self.main_window.window.Bind(wx.EVT_MENU, self.onSaveAs, file_menu_save_as)
        self.main_window.window.Bind(wx.EVT_MENU, self.onPrint, file_menu_print)
        self.main_window.window.Bind(wx.EVT_MENU, self.onExit, file_menu_exit)
    #Function that creates a new tab.
    def onNewTab(self, evt):
        self.main_window.createTab()
    #Function that creates a new instance of the window.
    def onNewWindow(self, evt):
        new_window = WindowInstance()
        new_window.MainLoop()
    #For the open file menu item; also changes the window title depending on the name of the file.
    def onOpen(self, evt):
        wildcard = "Text documents (*.txt)|*.txt|All files (*.*)|*.*"
        style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        dlg = wx.FileDialog(self.main_window.window, "Open", wildcard= wildcard, style=style)
        if (dlg.ShowModal() == wx.ID_OK):
            file_path = dlg.GetPath()
            self.main_window.current_file_paths[self.main_window.notebook.GetSelection()] = file_path
        with open(file_path, 'r') as file:
            contents = file.read()
            self.main_window.getTextControlFromTab().SetValue(contents)
        dlg.Destroy()
        self.main_window.notebook.SetPageText(self.main_window.notebook.GetSelection(), os.path.basename(self.main_window.current_file_paths[self.main_window.notebook.GetSelection()]))
        self.main_window.onTabChange(evt=evt)
    #Function to save the current file; if file exists, will override the contents with the new contents; if the file does not exist, will create and open the save as dialogue box and change the window title to include the file name.
    def onSave(self, evt):
        if self.main_window.current_file_paths[self.main_window.notebook.GetSelection()]:
            with open(self.main_window.current_file_paths[self.main_window.notebook.GetSelection()], 'w') as file:
                file.write(self.main_window.getTextControlFromTab().GetValue())
        else:
            wildcard = "Text documents(*.txt)|*.txt|All files(*.*)|*.*"
            style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
            dlg = wx.FileDialog(self.main_window.window, "Save as", wildcard=wildcard, style=style)
            if (dlg.ShowModal() == wx.ID_OK):
                file_path = dlg.GetPath()
                self.main_window.current_file_paths[self.main_window.notebook.GetSelection()] = file_path
            with open(file_path, 'w') as file:
                file.write(self.main_window.getTextControlFromTab().GetValue())
            dlg.Destroy()
            self.main_window.notebook.SetPageText(self.main_window.notebook.GetSelection(), os.path.basename(self.main_window.current_file_paths[self.main_window.notebook.GetSelection()]))
        self.main_window.onTabChange(evt=evt)
    #For the save as function which creates a new file or saves the same file with a new different file name, and changes the window title with the new file name.
    def onSaveAs(self, evt):
        wildcard = "Text documents(*.txt)|*.txt|All files(*.*)|*.*"
        style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        dlg = wx.FileDialog(self.main_window.window, "Save as", wildcard=wildcard, style=style)
        if (dlg.ShowModal() == wx.ID_OK):
            file_path = dlg.GetPath()
            self.main_window.current_file_paths[self.main_window.notebook.GetSelection()] = file_path
        with open(file_path, 'w') as file:
            file.write(self.main_window.getTextControlFromTab().GetValue())
        dlg.Destroy()
        self.main_window.notebook.SetPageText(self.main_window.notebook.GetSelection(), os.path.basename(self.main_window.current_file_paths[self.main_window.notebook.GetSelection()]))
        self.main_window.onTabChange(evt=evt)
    #Function that prints the text using a printer
    def onPrint(self, evt):
        printer = wx.Printer()
        print_dlg = wx.PrintDialog(self.main_window.window)
        if print_dlg.ShowModal() == wx.ID_OK:
            print_data = print_dlg.GetPrintData()
            printout = TextPrintout(self.main_window.getTextControlFromTab().GetValue())
            printer.Print(parent=self.main_window.window, printout=printout)
            printout.Destroy()
        print_dlg.Destroy()
    #For the exit menu item of the file menu which closes the window; in addition, the function checks if there have been changes to the file and asks user to save or not saved and also checks if there is text but no file name and will ask user to save or not save.
    def onExit(self, evt):
        if self.main_window.current_file_paths[self.main_window.notebook.GetSelection()] != "":
            with open(self.main_window.current_file_paths[self.main_window.notebook.GetSelection()], 'r') as file:
                current_contents = file.read()
            if current_contents != self.main_window.getTextControlFromTab().GetValue():
                dlg = wx.MessageDialog(parent=self.main_window.window, caption="Save Changes", message="Do you want to save changes to " + os.path.basename(self.current_file_path) + "?", style=wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION)
                result = dlg.ShowModal()
                if result == wx.ID_YES:
                    self.onSave(evt)
                    self.main_window.window.Close(True)
                elif result == wx.ID_NO:
                    self.main_window.Close(True)
                else:
                    dlg.Destroy()
                    return
        else:
            if self.main_window.getTextControlFromTab().GetValue():
                dlg = wx.MessageDialog(parent=self.main_window.window, caption="Save Changes", message="Do you want to save changes to Untitled?", style=wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION)
                result = dlg.ShowModal()
                if result == wx.ID_YES:
                    self.onSave(evt)
                    self.main_window.window.Close(True)
                elif result == wx.ID_NO:
                    self.main_window.window.Close(True)
                else:
                    dlg.Destroy()
                    return
            else:
                self.main_window.window.Close(True)

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
class WindowInstance(wx.App):
    def OnInit(self):
        MainWindow(parent=None, title="Untitled - Text Editor")
        return True

window_instance = WindowInstance()
window_instance.MainLoop()