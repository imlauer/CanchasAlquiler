#!/usr/bin/env python3
import npyscreen

class App(npyscreen.StandardApp):
    def onStart(self):
        self.addForm("MAIN", MainForm, name="Hello Medium!")

class MainForm(npyscreen.FormBaseNew):
    def create(self):
        # Get the space used by the form
        y, x = self.useable_space()
        self.add(npyscreen.TitleDateCombo, name="Date:", max_width=x // 2)
        self.add(npyscreen.TitleMultiSelect, relx=x // 2 + 1, rely=2, value=[1, 2], name="Pick Several", values=["Option1", "Option2", "Option3"], scroll_exit=True)
        # You can use the negative coordinates
        self.add(npyscreen.TitleFilename, name="Filename:", rely=-5)

MyApp = App()
MyApp.run()
