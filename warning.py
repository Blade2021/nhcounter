from tkinter import *

root = Tk()
countingLabel = Label(root, text="Time to Count:0", background='blue', foreground='white', font='Times 20', relief='groove', borderwidth=3)
countingLabel.grid(row=0, column=1)
theCountValue = 0


def begin_count():
    global theCountValue, countingLabel
    theCountValue = theCountValue + 1
    countingLabel.configure(text = "Count:" + str(theCountValue))


incrementButton = Button(root,text="Increment",command=begin_count)
incrementButton.grid(row=0, column=0)

mainloop()