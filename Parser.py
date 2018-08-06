import fileinput
import sys

x = 0
y = 0
value = "Pear"

with fileinput.input(files="testfile.txt", backup="test.bak",inplace=1) as file:
    for line in file:
        print(line, end='')
        if value in line:
            y = file.lineno()+1
            print(y)
        if file.lineno() == y:
            print("Line:"+line, end='')
            line = line.replace("Apple", "Orange")
            sys.stdout.write(line)
            print("Triggered", end='')

fileinput.close()