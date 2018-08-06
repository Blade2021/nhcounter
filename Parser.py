import fileinput
import sys

x = 0
y = 0
rate = 0
value = "Z-"


def feedCheck(line):
    feedCheck = line.find('F')
    if feedCheck >= 1:
        line = line[0:feedCheck]
        return str(line)


with fileinput.input(files="testfile.txt", backup="test.bak", inplace=1) as file:
    for line in file:
        if value in line:
            y = file.filelineno()+1
            feedCheck = line.find('F')
            if feedCheck >= 1:
                line = line[0:feedCheck]
            #line = feedCheck(line)
            line = line.rstrip('\n')
            if rate >= 1:
                line += " F4. \n"
                rate = 0
            else:
                line += "\n"
        if (file.filelineno() == y) and ("G01" in line):
            feedCheck = line.find('F')
            if feedCheck >= 1:
                line = line[0:feedCheck]
            #line = feedCheck(line)
            if rate == 0:
                line = line.rstrip('\n')
                line += " F7. \n"
                rate = 1
            #line = " F7." + line
            #line = line.replace("Apple", "Orange")
        sys.stdout.write(line)

fileinput.close()