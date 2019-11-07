from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import tkinter.font as Font
import copas
 
def fileDialog():
    global filename
    filename = filedialog.askopenfilename(initialdir =  folder_path, title = "Select A File", filetype =
    (("jpeg files","*.jpg"),("all files","*.*")) )
    photo = ImageTk.PhotoImage(Image.open(filename))
    label_photo = Label(frame_inner_center_right,height=300,width=300, image = photo)
    label_photo.grid(columnspan=2, row = 0)
    label_photo.image = photo


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
    temp = filedialog.askdirectory()
    folder_path.set(temp)

def run_program_euclid():
    global names
    numOfPhotos = int(entry_numOfPhotos.get())
    root.withdraw()
    names = copas.run_euclid(filename, int(numOfPhotos))
    window_result()

def run_program_cosine():
    root.withdraw()
    #copas.run_cosine(filename, numOfPhotos)
    window_result()

def window_result():
    global result
    result = Toplevel(root)
    button_back = HoverButton(result,text='back', command = back)
    button_back.grid()

    j=1
    for i in range(int(numOfPhotos)//2 + 1):
        photo = ImageTk.PhotoImage(Image.open(names[i]))
        label_photo = Label(result,height=300,width=300, image = photo)
        label_photo.grid(row = i,column=j)
        label_photo.image = photo
        if (j == 2):
            j = 1
        else :
            j += 1


def back():
    result.destroy()
    root.deiconify()
'''
def get_numOfPhotos():
    global numOfPhotos
    numOfPhotos = entry_numOfPhotos.get()
'''
root = Tk()
root.title('Face Recognition Program')
root.resizable(0,0)

#menu bar
menubar = Menu(root)
root.config(menu=menubar)

fileMenu = Menu(menubar,tearoff=0)

submenu = Menu(fileMenu)

fileMenu.add_command(label="Exit", underline=0, command=root.quit)
menubar.add_cascade(label="File", underline=0, menu=fileMenu)

customFont = Font.Font(family="cambria",size=12,slant="italic")
Font1 = Font.Font(family="Tahoma",size=10)
Font2 = Font.Font(family="cambria",size = 12)


folder_path = StringVar()
filename = StringVar()
numOfPhotos = IntVar()

frame_top = Frame(root)
frame_top.grid(row=0,sticky='n')

frame_center = Frame(root)
frame_center.grid(row=1)
#frame_center.grid_columnconfigure(0,weight=1)
#frame_center.grid_rowconfigure(0,weight=1)

frame_inner_center_left = Frame(frame_center)
frame_inner_center_left.grid(row=0,sticky='n')

frame_inner_center_left.grid_rowconfigure(0,weight=1)
frame_inner_center_left.grid_columnconfigure(0,weight=1)
frame_inner_center_left.grid_columnconfigure(1,weight=1)

frame_inner_center_right = Frame(frame_center)
frame_inner_center_right.grid(row=0,column=1,sticky='n')
frame_inner_center_right.grid_columnconfigure(0,weight=1)

frame_bottom = Frame(root)
frame_bottom.grid(row=2)


welcome = Label(frame_top, text='Face Recognition Program',font=customFont,bg ='silver')
welcome.grid(row=0,columnspan=3,sticky='nsew')
welcome['font'] = customFont

browsebutton = Button(frame_inner_center_left, text="Browse Datasets Directory", bg="yellow",command=browse_button, font = Font1)
browsebutton.grid(row=0,column=0, columnspan=2,sticky='ew')

browse_file_button = Button(frame_inner_center_left, text = "Choose an image",bg='orange',command = fileDialog,font=Font1)
browse_file_button.grid(row=1, column=0,columnspan=2,sticky='ew')

tulisan_image = Label(frame_inner_center_right, text = 'Image File',font=Font2, height=20, width=50)
tulisan_image.grid(row=0, columnspan=2)


label_numOfPhotos = Label(frame_inner_center_left ,text = 'Masukkan banyaknya foto mirip yang akan ditampilkan ')
label_numOfPhotos.grid(row=3)

entry_numOfPhotos = Entry(frame_inner_center_left)
entry_numOfPhotos.grid(row=3,column=1,sticky='nswe')

button_run_euclid = HoverButton(frame_inner_center_left, text ='metode euclidean', activebackground = 'silver', command = run_program_euclid,font=Font1)
button_run_euclid.grid(row=4, sticky='sew')

button_run_cosine = HoverButton(frame_inner_center_left, text ='metode cosine', activebackground = 'silver', command = run_program_cosine,font=Font1)
button_run_cosine.grid(row=4,column=1, sticky='sew')


#button_save_numofphotos = Button(frame_inner_center_left, text = 'save', command = get_numOfPhotos)
#button_save_numofphotos.grid(row=3,column=1)


#close_btn = HoverButton(frame_inner_center_left, text = "Close", activeforeground='white',activebackground = 'maroon',command = root.quit, font = Font1) # closing the 'window' when you click the button
#close_btn.grid(row=4,column=1,sticky='sew')

about = Label(frame_bottom, text = 'Program Face Recognition ini dibuat oleh:\n Kusuma-Istimewa', font= customFont)
about.grid(row=4, columnspan=2)

root.rowconfigure(2,weight=1)
root.columnconfigure(1,weight=1)
root.columnconfigure(0,weight=1)

root.mainloop()