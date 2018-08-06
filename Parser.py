import fileinput
import sys
import configparser


config = configparser.ConfigParser()
config.read('data.ini')
maxValue = int(config['DEFAULT']['KitAmount'])

x = 0
y = 0
rate = 0
value = "Z-"
slowrate = str(config['DEFAULT']['SlowRate'])
fastrate = str(config['DEFAULT']['FastRate'])


with fileinput.input(files="testfile.txt", backup="test.bak", inplace=1) as file:
    for line in file:
        line = line.replace("G23", "G03")
        line = line.replace("G22", "G02")
        pcodeCheck = line.find('P')
        if pcodeCheck >= 1:
            line = line[0:pcodeCheck]
            line += "\n"

        if value in line:
            y = file.filelineno()+1
            feedCheck = line.find('F')
            if feedCheck >= 1:
                line = line[0:feedCheck]
            #line = feedCheck(line)
            line = line.rstrip('\n')
            if rate >= 1:
                line += slowrate +"\n"
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
                line += fastrate +"\n"
                rate = 1
            #line = " F7." + line
            #line = line.replace("Apple", "Orange")
        sys.stdout.write(line)

fileinput.close()