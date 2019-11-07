from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, ImageEnhance, Image
import tkinter.font as Font
import math
import inti
import os

#Returns an image with reduced opacity.
def ReduceOpacity(im, opacity):
    """
    Taken from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/362879
    """
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im
 
#procedure to browse file and dereference filename
def fileDialog():
    global filename
    filename = filedialog.askopenfilename(initialdir =  folder_path, title = "Select A File", filetype =
    (("jpeg files","*.jpg"),("png files","*.png"), ("all files","*.*")) )
    photo = ImageTk.PhotoImage(Image.open(filename))
    label_photo = Label(frame_inner_center_right,height=300,width=300, image = photo)
    label_photo.grid(columnspan=2, row = 0)
    label_photo.image = photo

#procedure to show result if euclid button is clicked
def run_program_euclid():
    global names,numOfPhotos
    if (entry_numOfPhotos.get() == '' or filename == ' '):
        messagebox.showinfo("Error", "Masukkan tidak valid.")
    else:
        numOfPhotos = int(entry_numOfPhotos.get())
        root.withdraw()
        names = inti.run_euclid(filename, numOfPhotos)
        window_result_euclid()

#procedure to show result if cosine button is clicked
def run_program_cosine():
    global names,match,numOfPhotos
    if (entry_numOfPhotos.get() == '' or filename == ' '):
        messagebox.showinfo("Error", "Masukkan tidak valid.")
    else:
        numOfPhotos = int(entry_numOfPhotos.get())
        root.withdraw()
        names,match = inti.run_cosine(filename, numOfPhotos)
        window_result_cosine()

#procedure back to main menu from result window
def back():
    result.destroy()
    root.deiconify()

#result window config to show the result image
def window_result_euclid():
    global result
    result = Toplevel(root)
    result.geometry("430x650+400+0")
    result.resizable(0,0)

    
    #self.canvas.focus_set()
    def bind_mouse_scroll(parent, mode):
        #~~ Windows only
        parent.bind("<MouseWheel>", mode)
        #~~ Unix only        
        parent.bind("<Button-4>", mode)
        parent.bind("<Button-5>", mode)
 
    def yscroll(event):
        if event.num == 5 or event.delta < 0:
            canvas.yview_scroll(1, "unit")
        elif event.num == 4 or event.delta > 0:
            canvas.yview_scroll(-1, "unit")
    
    def update(event):
        if canvas.bbox('all') != None:
            region = canvas.bbox('all')
            canvas.config(scrollregion=region)

    canvas=Canvas(result)
    frame=Frame(canvas)
    myscrollbar=Scrollbar(result,orient="vertical",command=canvas.yview)
    canvas.configure(yscrollcommand=myscrollbar.set)

    myscrollbar.pack(side="right",fill="y",expand=0)
    canvas.pack(fill='both',expand=1)
    canvas.create_window((0,0),window=frame,anchor='nw')

    r=0
    c=0
    for i in range(numOfPhotos):
        image = Image.open(names[i])
        image = image.resize((200, 200), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        label_photo = Label(frame,height=200,width=200, image = photo)
        label_photo.grid(row = r,column=c)
        label_photo.image = photo

        label_file_name = Label(frame, text = str(os.path.basename(names[i])))
        label_file_name.grid(row=r+1,column=c)

        bind_mouse_scroll(label_photo, yscroll)
        bind_mouse_scroll(label_file_name, yscroll)

        if (c == 1):
            c = 0
            r += 2
        else :
            c += 1

    button_back = HoverButton(frame,text='back', activebackground = 'silver',command = back)
    button_back.grid(row= r +2,columnspan=2)

    canvas.bind('<Configure>', update)
    bind_mouse_scroll(canvas, yscroll)
    bind_mouse_scroll(myscrollbar, yscroll)
    bind_mouse_scroll(frame, yscroll)
        
#procedure to config window_result when cosine button is clicked
def window_result_cosine():
    global result
    result = Toplevel(root)
    result.title('Result')
    result.geometry("430x650+400+0")
    result.resizable(0,0)

    
    #self.canvas.focus_set()
    def bind_mouse_scroll(parent, mode):
        #~~ Windows only
        parent.bind("<MouseWheel>", mode)
        #~~ Unix only        
        parent.bind("<Button-4>", mode)
        parent.bind("<Button-5>", mode)
 
    def yscroll(event):
        if event.num == 5 or event.delta < 0:
            canvas.yview_scroll(1, "unit")
        elif event.num == 4 or event.delta > 0:
            canvas.yview_scroll(-1, "unit")

    def update(event):
        if canvas.bbox('all') != None:
            region = canvas.bbox('all')
            canvas.config(scrollregion=region)

    canvas=Canvas(result)
    frame=Frame(canvas)
    myscrollbar=Scrollbar(result,orient="vertical",command=canvas.yview)
    canvas.configure(yscrollcommand=myscrollbar.set)

    myscrollbar.pack(side="right",fill="y",expand=0)
    canvas.pack(fill='both',expand=1)
    canvas.create_window((0,0),window=frame,anchor='nw')

    r=0
    c=0
    for i in range(numOfPhotos):
        image = Image.open(names[i])
        image = image.resize((200, 200), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        label_photo = Label(frame,height=200,width=200, image = photo)
        label_photo.grid(row = r,column=c,pady=(10,0))
        label_photo.image = photo

        label_file_name = Label(frame, text = str(os.path.basename(names[i])))
        label_file_name.grid(row=r+1,column=c,pady=0)

        label_persen = Label(frame, text = 'Tingkat kemiripan : ' + str(round(match[i]*-100,2)) + ' %', font = Font2)
        label_persen.grid(row=r+2,column=c,sticky='n',pady=(0,10))

        bind_mouse_scroll(label_photo, yscroll)
        bind_mouse_scroll(label_file_name, yscroll)
        bind_mouse_scroll(label_persen, yscroll)

        if (c == 1):
            c = 0
            r += 3
        else :
            c += 1

    button_back = HoverButton(frame,text='back', activebackground = 'silver',command = back)
    button_back.grid(row= r +3,columnspan=2)

    canvas.bind('<Configure>', update)
    bind_mouse_scroll(canvas, yscroll)
    bind_mouse_scroll(myscrollbar, yscroll)
    bind_mouse_scroll(frame, yscroll)

#Button class that can change color when mouse hover
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

root = Tk()
root.title('Face Recognition Program')
root.configure(background='#edf5d3')
root.resizable(0,0)
root.geometry("+350+100")

#menu bar
menubar = Menu(root)
root.config(menu=menubar)

fileMenu = Menu(menubar,tearoff=0)

submenu = Menu(fileMenu)

fileMenu.add_command(label="Exit", underline=0, command=root.quit)
menubar.add_cascade(label="File", underline=0, menu=fileMenu)

Font2 = Font.Font(family="arial",size = 10, weight ='bold')
thisfont = Font.Font(family='Intro Rust G Base 2 Line')

folder_path = StringVar()
filename = ' '
numOfPhotos = 0

frame_top = Frame(root,background='#edf5d3')
frame_top.grid(row=0,pady=10)

frame_center = Frame(root,background='#edf5d3')
frame_center.grid(row=1,pady=5,padx=5)


frame_inner_center_left = Frame(frame_center,background='#edf5d3')
frame_inner_center_left.grid(row=0,sticky='n')

frame_inner_center_left.grid_rowconfigure(0,weight=1)
frame_inner_center_left.grid_columnconfigure(0,weight=1)
frame_inner_center_left.grid_columnconfigure(1,weight=1)

frame_top_inner_center_left = Frame(frame_inner_center_left,background='#edf5d3')
frame_top_inner_center_left.grid(row = 0,pady=10)

frame_bottom_inner_center_left = Frame(frame_inner_center_left,background='#edf5d3')
frame_bottom_inner_center_left.grid(row=1,pady=30)

frame_inner_center_right = Frame(frame_center,background='#edf5d3')
frame_inner_center_right.grid(row=0,column=1,sticky='n',padx=3,pady=3)
frame_inner_center_right.grid_columnconfigure(0,weight=1)

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = r"icon\icon.png"
abs_file_path = os.path.join(script_dir, rel_path)
temp = Image.open(abs_file_path)
temp = temp.resize((400, 100), Image.ANTIALIAS)
icon = ImageTk.PhotoImage(temp)

welcome = Label(frame_top, image = icon,background='#edf5d3')
welcome.image = icon
welcome.grid(row=0,columnspan=3,sticky='n')


rel_path = r"icon\browse_image2.png"
abs_file_path = os.path.join(script_dir, rel_path)
temp = Image.open(abs_file_path)
temp = temp.resize((70, 70), Image.ANTIALIAS)
browse_file_icon = ImageTk.PhotoImage(temp)
browse_file_button = HoverButton(frame_top_inner_center_left, image=browse_file_icon,command = fileDialog,activebackground='silver',background='#edf5d3')
browse_file_button.image = browse_file_icon
browse_file_button.grid(row=0, column=0,columnspan=2)

rel_path = r"icon\image-placeholder-icon.jpg"
abs_file_path = os.path.join(script_dir, rel_path)
temp = Image.open(abs_file_path)
temp = temp.resize((200, 200), Image.ANTIALIAS)
temp = ReduceOpacity(temp,0.5)
gambar_image = ImageTk.PhotoImage(temp)
tulisan_image = Label(frame_inner_center_right, image = gambar_image, height=300,width=300,padx=3,pady=3,background='#edf5d3')
tulisan_image.grid(row=0, columnspan=2)

label_numOfPhotos = Label(frame_bottom_inner_center_left ,text = 'Masukkan banyaknya foto mirip\nyang ingin ditampilkan ',background='#edf5d3',font=thisfont)
label_numOfPhotos.grid(row=3,padx=5,pady=20)

entry_numOfPhotos = Entry(frame_bottom_inner_center_left)
entry_numOfPhotos.grid(row=3,column=1,sticky='ew')

rel_path = r"icon\button_euclidean.png"
abs_file_path = os.path.join(script_dir, rel_path)
temp = Image.open(abs_file_path)
temp = temp.resize((150, 70), Image.ANTIALIAS)
gambar_button_euclid = ImageTk.PhotoImage(temp)
button_run_euclid = HoverButton(frame_bottom_inner_center_left, image=gambar_button_euclid, activebackground = 'silver', command = run_program_euclid,background='#edf5d3',border=0)
button_run_euclid.grid(row=4)
button_run_euclid.image=gambar_button_euclid

rel_path = r"icon\button_cosine.png"
abs_file_path = os.path.join(script_dir, rel_path)
temp = Image.open(abs_file_path)
temp = temp.resize((150, 70), Image.ANTIALIAS)
gambar_button_cosine = ImageTk.PhotoImage(temp)
button_run_cosine = HoverButton(frame_bottom_inner_center_left, image=gambar_button_cosine, activebackground = 'silver', command = run_program_cosine,background='#edf5d3',border=0)
button_run_cosine.grid(row=4,column=1, sticky='sew')

root.rowconfigure(2,weight=1)
root.columnconfigure(1,weight=1)
root.columnconfigure(0,weight=1)

root.mainloop()