from tkinter import *
from tkinter import font, filedialog
from tkinter import messagebox as mbox
import json

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.myfont = font.Font(family="Helvetica", size=14)
        self.theJson = dict()
        self.theFileName = None
        self.init_window()

    def init_window(self):
        self.master.title("record mouse moves")
        self.pack()
        label = Label(self, text="name:")
        label.pack(side=LEFT)
        self.nameInput = Entry(self, width="10", font=self.myfont)
        self.nameInput.pack(side=LEFT)
        #self.nameInput.pack(fill=BOTH, expand=1, side=LEFT)
        self.nameInput.bind("<<Modified>>", self.onInputChange)
        label = Label(self, text="x:")
        label.pack(side=LEFT)
        self.xCoordInput = Entry(self, width="5", font=self.myfont)
        self.xCoordInput.pack(side=LEFT)
        self.xCoordInput.bind("<<Modified>>", self.onInputChange)
        label = Label(self, text="y:")
        label.pack(side=LEFT)
        self.yCoordInput = Entry(self, width="5", font=self.myfont)
        self.yCoordInput.pack(side=LEFT)
        self.yCoordInput.bind("<<Modified>>", self.onInputChange)
        self.addButton = Button(self, text="add",
                                command=self.addEntry)
        self.addButton.pack(side=LEFT)
        self.outputbox = Label(self)
        self.outputbox.pack(side=BOTTOM)
        self.mainmenu = Menu(self)
        self.filemenu = Menu(self.mainmenu)
        self.filemenu.add_command(label="Open", command=self.openfile)
        self.filemenu.add_command(label="Save", command=self.savefile)
        self.filemenu.add_command(label="Save as", command=self.saveas)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.quit)
        self.mainmenu.add_cascade(label="File", menu=self.filemenu)
        self.master.config(menu=self.mainmenu)

    def addEntry(self):
        name = self.nameInput.get()
        xCoord = self.xCoordInput.get()
        yCoord = self.yCoordInput.get()
        self.theJson[name] = (xCoord, yCoord)

    def onInputChange(self, event):
        self.xCoordInput.edit_modified(0)
        # self.outputbox.set_html(md2html.convert(self.inputeditor.get("1.0" , END)))
        theText = self.xCoordInput.get("1.0", END)
        self.outputbox.set(theText)

    def openfile(self):
        openfilename = filedialog.askopenfilename(filetypes=(("JSON File", "*.json"),
                                                             ("Text File", "*.txt"),
                                                             ("All Files", "*.*")))
        if openfilename:
            try:
                with open(openfilename) as f:
                    self.theJson = json.load(f)
                self.theFileName = openfilename
            except:
                # print("Cannot Open File!")
                mbox.showerror("Error Opening Selected File",
                               "Oops!, The file you selected : {} can not be opened!".format(openfilename))

    def savefile(self):
        self.save()

    def saveas(self):
        savefilename = filedialog.asksaveasfilename(filetypes=(("JSON File", "*.json"),
                                                               ("Text File", "*.txt")), title="Save JSON File")
        if savefilename:
            self.theFileName = savefilename
            self.save()

    def save(self):
        filedata = str(self.theJson)
        if self.theFileName:
            try:
                f = open(self.theFileName, "w")
                f.write(filedata)
            except:
                mbox.showerror("Error Saving File", "Oops!, The File : {} can not be saved!".format(savefilename))

root = Tk()
#root.geometry("500x600")
app = Window(root)
app.mainloop()