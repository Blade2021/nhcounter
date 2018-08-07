import fileinput
import sys
import configparser

import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()

config = configparser.ConfigParser()
config.read('data.ini')

x = 0
y = 0
rate = 0
value = "Z-"
index = 0

slowRateArray = [2, 2, 2, 2]
fastRateArray = [7, 7, 7, 7]
slowRateArray[0] = str('F' + config['TOOL_1']['SlowRate'])
fastRateArray[0] = str('F' + config['TOOL_1']['FastRate'])
slowRateArray[1] = str('F' + config['TOOL_2']['SlowRate'])
fastRateArray[1] = str('F' + config['TOOL_2']['FastRate'])
slowRateArray[2] = str('F' + config['TOOL_3']['SlowRate'])
fastRateArray[2] = str('F' + config['TOOL_3']['FastRate'])
slowRateArray[3] = str('F' + config['TOOL_4']['SlowRate'])
fastRateArray[3] = str('F' + config['TOOL_4']['FastRate'])

with fileinput.input(files=file_path, backup=".bak", inplace=1) as file:
    for line in file:
        if(file.filelineno() == 1):
            sys.stdout.write(line)
            continue
        parentCheck = line.find("(")
        if parentCheck != -1:
            continue

        line = line.replace("G23", "G03")
        line = line.replace("G22", "G02")
        line = line.replace("F 0684", "F2.")
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
            if rate >= 1:
                line += slowRateArray[index] + "\n"
                rate = 0
            else:
                line += "\n"
        if (file.filelineno() == y) and ("G01" in line):
            feedCheck = line.find('F')
            if feedCheck >= 1:
                line = line[0:feedCheck]
            if rate == 0:
                line = line.rstrip('\n')
                line += fastRateArray[index] + "\n"
                rate = 1
        sys.stdout.write(line)

fileinput.close()
