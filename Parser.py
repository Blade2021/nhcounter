file = open("testfile.txt", "r+")
for line in file:
    print(line, end='')
    if "How" in line:
        file.write("However")