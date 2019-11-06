from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import tkinter.font as Font
 
def fileDialog():
    global canv, filename
    filename = filedialog.askopenfilename(initialdir =  folder_path, title = "Select A File", filetype =
    (("jpeg files","*.jpg"),("all files","*.*")) )
    photo = ImageTk.PhotoImage(Image.open(filename))
    canv = Canvas(root,height=300,width=300)
    canv.grid(columnspan=2, row = 2)
    canv.create_image(20,20,anchor='nw', image=photo)
    canv.image = photo


class HoverButton(Button):
    def __init__(self, master, **kw):
        Button.__init__(self,master=master,**kw)
        self.defaultBackground = self["background"]
        self.defaultForeground = self['foreground']
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']
        self['foreground'] = self['activeforeground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground
        self['foreground'] = self.defaultForeground

def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)

root = Tk()
root.title('Face Recognition Program')

customFont = Font.Font(family="cambria",size=12,slant="italic")
Font1 = Font.Font(family="Tahoma",size=10)
Font2 = Font.Font(family="cambria",size = 12)


folder_path = StringVar()

welcome = Label(root, text='Face Recognition Program\nLangkah-langkah:\nKlik Browse Datasets Directory, kemudian pilih directory datasets.',font=customFont)
welcome.grid(row=0,columnspan=3,sticky='new')
welcome['font'] = customFont

browsebutton = Button(root, text="Browse Datasets Directory", bg="yellow",command=browse_button, font = Font1)
browsebutton.grid(row=1,sticky='nsew')

browse_file_button = Button(root, text = "Browse A File",bg='orange',command = fileDialog,font=Font1)
browse_file_button.grid(column = 1, row = 1,sticky='nsew')

tulisan_image = Label(root, text = 'Image File',font=Font2)
tulisan_image.grid(row=2, columnspan=2)

run_button = HoverButton(root, text ='Run Program', activebackground = 'silver', command = '',font=Font1)
run_button.grid(row=3, sticky='sew')

close_btn = HoverButton(root, text = "Close", activeforeground='white',activebackground = 'maroon',command = root.quit, font = Font1) # closing the 'window' when you click the button
close_btn.grid(row=3,column=1,sticky='sew')

about = Label(root, text = 'Program Face Recognition ini dibuat oleh:\n Kusuma-Istimewa', font= customFont)
about.grid(row=4, columnspan=2)

root.rowconfigure(2,weight=1)
root.columnconfigure(1,weight=1)
root.columnconfigure(0,weight=1)

root.mainloop()