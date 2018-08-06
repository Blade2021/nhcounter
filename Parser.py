import fileinput
import sys

x = 0
y = 0
value = "Pear"

with fileinput.input(files="testfile.txt", backup="test.bak", inplace=1) as file:
    for line in file:
        if value in line:
            y = file.filelineno()+1
        if (file.filelineno() == y) and ("Apple" in line):
            line = line.replace("Apple", "Orange")
        sys.stdout.write(line)

fileinput.close()