f = open("points.txt", "r")

points = []

i = 1

#Read in the points
for line in f:
	line = line.rstrip('\n')
	line = line.split(',')
	points.append((i, line[0], line[1]))
	i += 1

f.close()

col1 = []
col2 = []
col3 = []
col4 = []

for point in points:
	if float(point[1]) < -2.5:
		col1.append(point)
	elif float(point[1]) < 0:
		col2.append(point)
	elif float(point[1]) < 2.5:
		col3.append(point)
	else:
		col4.append(point)

#Sort columns by number of points

cols = [(col, len(col)) for col in [col1, col2, col3, col4]]

cols = sorted(cols, key = lambda x: x[1])

for col in cols:
	print col
	col = sorted(col, key = lambda x: x[2])

for i in range(len(cols)):
	if i%2 == 0:
		cols[i].reverse()

points = [item for sublist in cols for item in sublist]

f = open("points.txt", "w")

f.write("SORT_THIS_SHIT:\n")

#Write list of X values
for i in range(len(points)):
	f.write("X%02d: DW %s\n" % (i+1, points[i][1]))

#Write list of Y values
f.write("\n")
for i in range(len(points)):
	f.write("Y%02d: DW %s\n" % (i+1, points[i][1]))

f.write("\n")
f.write("Points: DW X%02d\n" %(points[0][0],))

#Write list of point labels
f.write("\n")
for i in range(len(points)):
	f.write("Pnt%02d: DW X%02d\n" %(i+1, points[i][0]))

f.close()