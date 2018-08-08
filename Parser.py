import fileinput
import sys
import configparser

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

slowRateArray = ['2', '2', '2', '2']
fastRateArray = ['10', '10', '10', '10']
saveVar = 0
root = tk.Tk()
root.title("GCode File Parser - By Matt W.")

slowRate1 = tk.Label(root, text="Slow Rate 1", font='Times 12', borderwidth=3, width=12)
slowRate1.grid(row=1, column=0)
slowRate2 = tk.Label(root, text="Slow Rate 2", font='Times 12', borderwidth=3, width=12)
slowRate2.grid(row=2, column=0)
slowRate3 = tk.Label(root, text="Slow Rate 3", font='Times 12', borderwidth=3, width=12)
slowRate3.grid(row=3, column=0)
slowRate4 = tk.Label(root, text="Slow Rate 4", font='Times 12', width=12)
slowRate4.grid(row=4, column=0)
fastRate1 = tk.Label(root, text="Fast Rate 1", font='Times 12', width=12)
fastRate1.grid(row=1, column=3)
fastRate2 = tk.Label(root, text="Fast Rate 2", font='Times 12', width=12)
fastRate2.grid(row=2, column=3)
fastRate3 = tk.Label(root, text="Fast Rate 3", font='Times 12', width=12)
fastRate3.grid(row=3, column=3)
fastRate4 = tk.Label(root, text="Fast Rate 4", font='Times 12', width=12)
fastRate4.grid(row=4, column=3)


def execute():
    root.withdraw()
    x = 0
    y = 0
    rate = 0
    value = "Z-"

    slowRateArray[0] = str('F' + slowRateArray[0])
    slowRateArray[1] = str('F' + slowRateArray[1])
    slowRateArray[2] = str('F' + slowRateArray[2])
    slowRateArray[3] = str('F' + slowRateArray[3])
    fastRateArray[0] = str('F' + fastRateArray[0])
    fastRateArray[1] = str('F' + fastRateArray[1])
    fastRateArray[2] = str('F' + fastRateArray[2])
    fastRateArray[3] = str('F' + fastRateArray[3])

    file_path = filedialog.askopenfilename()
    try:
        with fileinput.input(files=file_path, backup=".bak", inplace=1) as file:
            for line in file:
                if(file.filelineno() == 1):
                    sys.stdout.write(line)
                    continue
                parentCheck = line.find("(")
                if parentCheck != -1:
                    if parentCheck == 0:
                        continue
                    else:
                        line = line[0:parentCheck]
                        line = line + "\n"
                # Remove Feed rates if applicable
                feedCheck = line.find('F')
                if feedCheck >= 1:
                    line = line[0:feedCheck]
                    line += "\n"

                line = line.replace("G23", "G03")
                line = line.replace("G22", "G02")
                # line = line.replace("F 0684", "F2.")
                # Search document for P codes and remove them
                pcodeCheck = line.find('P')
                if pcodeCheck >= 1:
                    line = line[0:pcodeCheck]
                    line += "\n"

                toolCheck = line.find('T')
                if toolCheck >= 1:
                    index += 1
                    if index >= len(slowRateArray):
                        index = 0

                # Search document line by line for Z negatives
                if value in line:
                    if "G00" in line:
                        continue

                    y = file.filelineno() + 1
                    feedCheck = line.find('F')
                    if feedCheck >= 1:
                        line = line[0:feedCheck]
                    line = line.rstrip('\n')
                    if rate >= 2:
                        line += slowRateArray[index] + "\n"
                        rate = 1
                    else:
                        if rate == 0:
                            rate = 1
                            line += slowRateArray[index]
                        line += "\n"
                if (file.filelineno() == y) and ("G01" in line):
                    feedCheck = line.find('F')
                    if feedCheck >= 1:
                        line = line[0:feedCheck]
                    if rate == 1:
                        line = line.rstrip('\n')
                        line += fastRateArray[index] + "\n"
                        rate = 2
                sys.stdout.write(line)

        fileinput.close()
    except IOError:
        print("File not found")
    exit()

def grabMax():
    indx = 0

    # if saveVar != 1:
    saveVariable = tk.messagebox.askyesno("Data File", "Would you like to save the data?")
    if saveVariable == 'yes':
        saveVar = 1
    else:
        saveVar = 0


    config = configparser.ConfigParser()
    config.read('data.ini')
    dataFile = open('data.ini', 'r+')
    while indx < 4:
        try:
            slowRateArray[indx] = str(slowRateEntryArray[indx].get())
            if saveVar == 1:
                try:
                    config.set('TOOL_' + (indx+1), 'SlowRate', slowRateArray[indx])
                except:
                    print("Something went wrong")
        except ValueError:
            indx += 1
            slowRateArray[indx] = '2'
            continue
        indx += 1
    indx = 0
    while indx < 4:
        try:
            fastRateArray[indx] = str(fastRateEntryArray[indx].get())
            if saveVar == 1:
                try:
                    config.set('TOOL_' + (indx+1), 'SlowRate', slowRateArray[indx])
                except:
                    print("Something went wrong")
        except ValueError:
            indx += 1
            fastRateArray[indx] = '8'
            continue
        indx += 1
    config.write(dataFile)
    dataFile.close()
    execute()


def exeDataFile():
    config = configparser.ConfigParser()
    config.read('data.ini')

    try:
        slowRateArray[0] = config['TOOL_1']['SlowRate']
        slowRateArray[1] = config['TOOL_2']['SlowRate']
        slowRateArray[2] = config['TOOL_3']['SlowRate']
        slowRateArray[3] = config['TOOL_4']['SlowRate']
        fastRateArray[0] = config['TOOL_1']['FastRate']
        fastRateArray[1] = config['TOOL_2']['FastRate']
        fastRateArray[2] = config['TOOL_3']['FastRate']
        fastRateArray[3] = config['TOOL_4']['FastRate']
    except ValueError:
        print("something went wrong")
    execute()


slowRateEntryArray = ["", "", "", ""]
fastRateEntryArray = ["", "", "", ""]
slowRateEntryArray[0] = tk.Entry(master=root, width=10)
slowRateEntryArray[0].grid(column=2, row=1)

slowRateEntryArray[1] = tk.Entry(master=root, width=10)
slowRateEntryArray[1].grid(column=2, row=2)

slowRateEntryArray[2] = tk.Entry(master=root, width=10)
slowRateEntryArray[2].grid(column=2, row=3)

slowRateEntryArray[3] = tk.Entry(master=root, width=10)
slowRateEntryArray[3].grid(column=2, row=4)

fastRateEntryArray[0] = tk.Entry(master=root, width=10)
fastRateEntryArray[0].grid(column=4, row=1)

fastRateEntryArray[1] = tk.Entry(master=root, width=10)
fastRateEntryArray[1].grid(column=4, row=2)

fastRateEntryArray[2] = tk.Entry(master=root, width=10)
fastRateEntryArray[2].grid(column=4, row=3)

fastRateEntryArray[3] = tk.Entry(master=root, width=10)
fastRateEntryArray[3].grid(column=4, row=4)


grabMaxButton = tk.Button(root, text="Enter", width=10, command=grabMax)
grabMaxButton.grid(row=9, column=0)

grabMaxButton = tk.Button(root, text="Use Data File", width=10, command=exeDataFile)
grabMaxButton.grid(row=9, column=3)

tk.mainloop()
# root.withdraw()
