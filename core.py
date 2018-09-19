import sys
import configparser

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# Initialise arrays for parsing
# Array sizes will be increased as needed
countVariable = 0
countInterval = 0
countstring=""

# Main Window
root = tk.Tk()
root.title("Pad Print Counter - By Matt W.")
root.resizable(width=False, height=False)  # Disable resizing

changecountlabel = tk.Label(root, text=("Count Variable"), font='Times 20')
changecountlabel.grid(row=1,column=3,columnspan=3, pady=13)
changecountvariable = tk.Label(root, text=(countstring), font='Times 20')
changecountvariable.grid(row=1,column=6,columnspan=2, pady=13)
currentcountlabel = tk.Label(root, text=("Current Count"), font='Times 20', borderwidth=3, width=12)
currentcountlabel.grid(row=2, column=0)
distplaycountvariable = tk.Label(root, text=("89"), font='Times 20', borderwidth=3, width=12)
distplaycountvariable.grid(row=3, column=0)
# Grab tool amount from file


def numFunction(id):
    print("You pressed: " + str(id))
    global countstring
    countstring += str(id)
    changecountvariable.config(text=countstring)

def clear():
    global countstring
    countstring = ""
    changecountvariable.config(text="")

enterbutton = tk.Button(root, text='Enter', width=6, font='Times 26')
enterbutton.grid(row=5,column=6)

clearbutton = tk.Button(root, text='Clear', width=6, font='Times 26', command=clear)
clearbutton.grid(row=5,column=4)
numbuttonarray = [0,1,3,4,5,6,7,8,9,0]
x=1
rowcomp=0
colcomp=0
while(x<10):
    if (x > 3) and (x <= 6):
        rowcomp=1
    if (x > 6):
        rowcomp=2
    numbuttonarray[x] = tk.Button(root, text=x, width=3, height=1, font='Times 30', command=lambda c=x: numFunction(numbuttonarray[c].cget("text")))
    numbuttonarray[x].grid(row=(2+rowcomp), column=(4+colcomp))
    colcomp+=1
    if(colcomp >= 3):
        colcomp=0
    x+=1

tk.mainloop()
