import os

lines = 0
totalLines = 0
for file in os.listdir():
	if os.path.isfile(file) and file[-3:] == ".py":
		with open(file) as in_file:
			for line in in_file.readlines():
				totalLines += 1
				line = line.strip()
				if line != "" and line[0] != "#":
					print(line)
					lines += 1
print(lines, totalLines)