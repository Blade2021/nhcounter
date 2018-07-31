from tkinter import *
root = Tk()
counter = 20


def makeSomething(value):
    global counter
    counter = value


def printVariable():
    print(counter)


root.title("NAHA")
root.geometry('350x200')
txt = Entry(root, width=10)
txt.grid(column=1, row=0)


def error():
    messagebox.showerror('Machine Error', 'Good job you just broke something.')


def up():
    makeSomething(counter+1)
    printVariable()
    lbl.configure(text=str(counter))


def down():
    makeSomething(counter-1)
    printVariable()
    lbl.configure(text=str(counter))


lbl = Label(root, text="This is a test")
lbl.grid(column=0, row=0)
btn = Button(root, text="Click Me", command=error)
btn.grid(column=2, row=0)
upbtn = Button(root, text="Up", command=up())
upbtn.grid(column=5, row=5)
downbtn = Button(root, text="Down", command=down())
downbtn.grid(column=6, row=5)

root.mainloop()
