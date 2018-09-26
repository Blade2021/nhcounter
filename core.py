import tkinter as tk
import serial

ser = serial.Serial('/dev/ttyUSB0', 19200)


# Initialise arrays for parsing
# Array sizes will be increased as needed
countVariable = 100
countInterval = 0
countstring=""

# Main Window
root = tk.Tk()
root.title("Pad Print Counter - By Matt W.")
root.resizable(width=False, height=False)  # Disable resizing

changecountlabel = tk.Label(root, text=("Count Change"), font='Times 20')
changecountlabel.grid(row=1,column=3,columnspan=3, pady=13)
changecountvariable = tk.Label(root, text=(countstring), font='Times 20', width=7, bd=1, relief='groove')
changecountvariable.grid(row=1,column=6,columnspan=2, pady=13)
currentcountlabel = tk.Label(root, text=("Current Count"), font='Times 20', borderwidth=3, width=12)
currentcountlabel.grid(row=2, column=0)
displaycountvariable = tk.Label(root, text=("0"), font='Times 20', borderwidth=3, width=12, bd=1, relief='groove', anchor='s')
displaycountvariable.grid(row=3, column=0)
countvariable = tk.Label(root, text='Counter:', font='Times 20')
countvariable.grid(row=1, column=0)
# Grab tool amount from file
def startCounter():
    #set flag to low
    #set pin to input
    #reset count

def partCounter():
    #set flag to low
    #set pin to input
    #read out count+1

def counterStop():
    #set relay to LOW

def setcount():
    global countInterval
    countInterval +=1
    if countInterval >= countVariable:
        countreset()
    displaycountvariable.config(text=countInterval)

def setInterval():
    global countVariable
    countVariable = int(countstring)
    countvariable.config(text=('Counter: ' + countstring))
    clear()

def countreset():
    displaycountvariable.config(text="0")
    global countInterval
    countInterval = 0

def numFunction(id):
    print("You pressed: " + str(id))
    global countstring
    countstring += str(id)
    changecountvariable.config(text=countstring)

def clear():
    global countstring
    countstring = ""
    changecountvariable.config(text="")

def run():
    global countVariable
    countVariable = 0
    ser.write("Test")


enterbutton = tk.Button(root, text='Enter', width=6, font='Times 26', command=setInterval)
enterbutton.grid(row=5,column=6)

clearbutton = tk.Button(root, text='Clear', width=6, font='Times 26', command=clear)
clearbutton.grid(row=5,column=4)

runbutton = tk.Button(root, text='Run', width=10, font='Times 26', command=setcount)
runbutton.grid(row=4,column=0)

resetbutton = tk.Button(root, text='Reset', width=10, font='Times 26', command=countreset)
resetbutton.grid(row=5 ,column=0)

numbuttonarray = [0,1,3,4,5,6,7,8,9,0]
x=1
rowcomp=0
colcomp=0
while(x<11):
    if (x > 3) and (x <= 6):
        rowcomp=1
    if (x > 6):
        rowcomp=2
    if x is 10:
        x = 0
        rowcomp = 3
        colcomp = 1
    numbuttonarray[x] = tk.Button(root, text=x, width=3, height=1, font='Times 30', command=lambda c=x: numFunction(numbuttonarray[c].cget("text")))
    numbuttonarray[x].grid(row=(2+rowcomp), column=(4+colcomp))
    if x is 0:
        break
    colcomp+=1
    if(colcomp >= 3):
        colcomp=0
    x+=1

tk.mainloop()
