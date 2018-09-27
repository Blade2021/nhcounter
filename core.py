import tkinter as tk
import serial
import threading

class dataStorage():
    pauseStatus = 0
    orig_color = "ivory2"


#ser = serial.Serial('/dev/ttyUSB0', 19200, 8, 'N', 1, timeout=5)
ser = serial.Serial('COM8', 19200, 8, 'N', 1, timeout=5)

# Initialise arrays for parsing
# Array sizes will be increased as needed
countVariable = 100
countInterval = 0
countstring=""

# Main Window
root = tk.Tk()
root.title("National Hanger - Pad Print Counter")
root.resizable(width=False, height=False)  # Disable resizing

changecountlabel = tk.Label(root, text=("Input:"), anchor='e',justify='right', font='Times 20')
changecountlabel.grid(row=1,column=3,columnspan=3, pady=13)
changecountvariable = tk.Label(root, text=(countstring), font='Times 20', width=7, bd=1, relief='groove')
changecountvariable.grid(row=1,column=6,columnspan=2, pady=13)
currentcountlabel = tk.Label(root, text=("Current Count"), font='Times 20', borderwidth=3, width=12)
currentcountlabel.grid(row=2, column=0)
displaycountvariable = tk.Label(root, text=("0"), font='Times 20', borderwidth=3, width=12, bd=1, relief='groove', anchor='s')
displaycountvariable.grid(row=3, column=0)
countvariable = tk.Label(root, text='Counter:', font='Times 20')
countvariable.grid(row=1, column=0)

def pausecommand():
    if (dataStorage.pauseStatus == 0):
        string1 = "RUN.0"
        pausefunction(1)
    else:
        string1 = "RUN.2"
        dataStorage.pauseStatus = 0
        pausefunction(0)
    ser.write((string1 + '\n').encode())


def pausefunction(pstatus):
    if(pstatus == 1):
        dataStorage.pauseStatus = 1
        dataStorage.orig_color = pausebutton.cget("background")
        pausebutton.config(bg='yellow')
    else:
        pausebutton.config(bg=dataStorage.orig_color)

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
    ser.write(("VARCHANGE." + countstring + '\n').encode())
    clear()

def countreset():
    #displaycountvariable.config(text="0")
    #global countInterval
    #countInterval = 0
    dataStorage.pauseStatus = 0
    ser.write(("RUN.0\n").encode())
    displaycountvariable.config(bg='OrangeRed2')
    pausefunction(0)

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
    pausefunction(0)
    string1 = 'RUN.1'
    ser.write((string1 + '\n').encode())
    displaycountvariable.config(text='0')
    displaycountvariable.config(bg='yellow')



def handle_data(data):
    data = data.rstrip('\n')
    if 'S:' in data:
        # data = data.rstrip('\n')
        in_count = data[2:]
        displaycountvariable.config(text=in_count)
        displaycountvariable.config(bg='yellow')
    if "COMPLETE" in data:
        displaycountvariable.config(bg='green yellow')
    if 'CVAR' in data:
        countstring = data[5:]
        countvariable.config(text="Counter: " + countstring)
    print(data)


def read_from_port():
        while True:
            if ser.in_waiting > 0:
                reading = ser.readline().decode()
                handle_data(reading)



thread = threading.Thread(target=read_from_port)
thread.start()


enterbutton = tk.Button(root, text='Enter', width=6, font='Times 26', command=setInterval)
enterbutton.grid(row=5,column=6)

clearbutton = tk.Button(root, text='Clear', width=6, font='Times 26', command=clear)
clearbutton.grid(row=5,column=4)

runbutton = tk.Button(root, text='Run', width=10, font='Times 26', command=run)
runbutton.grid(row=4,column=0)

resetbutton = tk.Button(root, text='Stop', width=10, font='Times 26', command=countreset)
resetbutton.grid(row=5 ,column=0)

pausebutton = tk.Button(root, text='Pause', width=10, font='Times 26', command=pausecommand)
pausebutton.grid(row=6 ,column=0)

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
