from tkinter import *
from tkinter import messagebox

root = Tk()
countingLabel = Label(root, text="Time to Count:0", background='blue', foreground='white', font='Times 28',
                      relief='groove', borderwidth=3)
countingLabel.grid(row=0, column=1)
theCountValue = 0
maxValue = 0
txtEntry = Entry(root, width=15)
txtEntry.grid(column=10, row=10)
root.title("NAHA Counting Machine")
root.geometry('350x200')


def grabMax(txtEntry):
    value = txtEntry.get()
    try:
        return int(value)
    except ValueError:
        return None


def begin_count():
    global theCountValue, countingLabel
    if theCountValue > maxValue:
        reset_count()
        return
    theCountValue = theCountValue + 1
    countingLabel.configure(text="Count:" + str(theCountValue))


def lower_count():
    global theCountValue, countingLabel
    theCountValue = theCountValue - 1
    countingLabel.configure(text="Count:" + str(theCountValue))


def reset_count():
    global theCountValue, countingLabel
    theCountValue = 0
    countingLabel.configure(text="Count:0")


incrementButton = Button(root, text="Increment", width=10, command=begin_count)
incrementButton.grid(row=0, column=0)

decrementButton = Button(root, text="Decrement", width=10, command=lower_count)
decrementButton.grid(row=1, column=0)

resetButton = Button(root, text="Reset", width=10, command=reset_count)
resetButton.grid(row=2, column=0)

grabMaxButton = Button(root, text="Enter", width=10, command=grabMax)
grabMaxButton.grid(row=3, column=0)

mainloop()
