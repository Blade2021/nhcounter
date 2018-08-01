from tkinter import *
from tkinter import messagebox
# import RPi.GPIO as GPIO
import time
import configparser
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(7, GPIO.OUT)

root = Tk()
maxValue = 100  # set a default
theCountValue = 0
max = 31
start = time.time()
root.title("NAHA Counting Machine")
root.geometry('370x220')

# Import configurations
config = configparser.ConfigParser()
config.read('data.ini')
maxValue = int(config['DEFAULT']['KitAmount'])
print("Read from INI File | Kit Amount: " + str(maxValue))
print("Startup:")
print(time.gmtime())


countingLabel = Label(root, text="Time to Count:0", background='blue', foreground='white', font='Times 28',
                      relief='groove', borderwidth=3, width=12)
countingLabel.grid(row=0, column=1)
maxValueCount = Label(root, text="Kit Size:" + str(maxValue), background='blue', foreground='white', font='Times 28',
                      relief='groove', borderwidth=3, width=12)
maxValueCount.grid(row=1, column=1)


def grabMax():
    value = txtEntry.get()
    if value.isnumeric():
        try:
            print("Updated Kit Amount to: " + value)
            finalValue = int(value)
            global maxValue
            maxValue = finalValue
            maxValueCount.configure(text="Kit Size:" + str(maxValue))
            config['DEFAULT']['KitAmount'] = value
            with open('data.ini', 'w') as configfile:
                config.write(configfile)
            return int(value)
        except ValueError:
            return None



def begin_count():
    global theCountValue, countingLabel
    if theCountValue >= maxValue:
        reset_count()
        return
    theCountValue = theCountValue + 1
    countingLabel.configure(text="Count:" + str(theCountValue))


def error():
    messagebox.showerror('Machine Error', 'Frigging roger...')


def lower_count():
    global theCountValue, countingLabel
    theCountValue = theCountValue - 1
    countingLabel.configure(text="Count:" + str(theCountValue))


def reset_count():
    global theCountValue, countingLabel
    theCountValue = 0
    countingLabel.configure(text="Count:0")


txtEntry = Entry(master=root, width=15)
txtEntry.grid(column=1, row=9)


incrementButton = Button(root, text="Increment", width=10, command=begin_count)
incrementButton.grid(row=0, column=0)

decrementButton = Button(root, text="Break me!", background='red', foreground='white', width=10, command=error)
decrementButton.grid(row=1, column=0)

resetButton = Button(root, text="Reset", width=10, command=reset_count)
resetButton.grid(row=2, column=0)

grabMaxButton = Button(root, text="Enter", width=10, command=grabMax)
grabMaxButton.grid(row=3, column=0)



mainloop()
