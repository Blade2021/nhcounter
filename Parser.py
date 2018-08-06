import in_place

value = "Changes"
with in_place.InPlace('testfile.txt') as file:
    line1 = file.readLine()
    line2 = file.readLine()
    for line in file:
        if string1 == "Check":
            line = line.replace(value, 'testZ')
            file.write(line)
        string1 = line
