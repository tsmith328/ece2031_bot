#!usr/bin/python
import os

def sort():
    f = open("points.txt", "r")
    points = []
    i = 1

    #Read in the points
    for line in f:
        line = line.rstrip()
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
    cols.reverse()

    #Sort points within each column
    cols = [sorted(col[0], key=lambda x: float(x[2])) for col in cols]

    #Reverse every other column for back-and-forth
    for i in range(len(cols)):
        if (i+1)%2 == 0:
            cols[i].reverse()

    points = [point for col in cols for point in col]

    #print points
    f = open("sorted.txt.tmp", "w")
    f.write("TableOfPoints:\n")

    #Write list of X values
    for i in range(len(points)):
        f.write("X%02d: DW %s\n" % (i+1, points[i][1]))

    #Write list of Y values
    f.write("\n")
    for i in range(len(points)):
        f.write("Y%02d: DW %s\n" % (i+1, points[i][2]))

    f.write("\n")
    f.write("Points:\n")

    #Write list of point labels
    f.write("\n")
    for i in range(len(points)):
        f.write("DW %02d\n" %(points[i][0]))

    f.close()

def sort2():
    f = open("points.txt", "r")
    points = []
    i = 1
    for line in f:
        line = line.rstrip()
        line = line.split(',')
        points.append((i, line[0], line[1]))
        i += 1

    f.close()

    curr = (0,0)
    s_points = []
    while i > 1:
        dist = []
        for point in points:
            dist.append((point, (((curr[0]-float(point[1]))**2)+((curr[1]-float(point[2]))**2))**0.5))
        dist = sorted(dist, key=lambda x: x[1])
        point = dist.pop(0)[0]
        s_points.append(point)
        points.remove(point)
        i -= 1

    points = s_points

    #print points
    f = open("sorted.txt.tmp", "w")
    f.write("TableOfPoints:\n")

    #Write list of X values
    for i in range(len(points)):
        f.write("X%02d: DW %s\n" % (i+1, points[i][1]))

    #Write list of Y values
    f.write("\n")
    for i in range(len(points)):
        f.write("Y%02d: DW %s\n" % (i+1, points[i][2]))

    f.write("\n")
    f.write("Points:\n")

    #Write list of point labels
    f.write("\n")
    for i in range(len(points)):
        f.write("DW %02d\n" %(points[i][0]))

    f.close()

def scale():
    pts = open("sorted.txt.tmp", "r")
    pts_out = open("scaled.txt.tmp", "w")
    for line in pts:
        if line[0] in ["X","Y"]: #If line is a coord
            label, num = line.rstrip().split(":")
            label = label + ": DW "
            num = int(num[4:])
            num *= 305
            num = round(float(num) / 1.05)
            pts_out.write(label + str(int(num)) + '\n')
        else: #Else just copy the line
            pts_out.write(line)
    pts.close()
    pts_out.close()
    #Copy back to sorted.txt.tmp
    pts = open("sorted.txt.tmp", "w")
    scaled = open("scaled.txt.tmp", "r")
    for line in scaled:
        pts.write(line)
    pts.close()
    scaled.close()
    os.remove("scaled.txt.tmp")

def main():
    asm = open("movement_code.asm", "r")
    out = open("robot.asm", "w")
    points = open("sorted.txt.tmp", "r")

    #Copy assembly code to new file except where points need to be
    for line in asm:
        if line.rstrip() == ";Put points here":
            for pline in points:
                out.write(pline)
        else:
            out.write(line)

    asm.close()
    out.close()
    points.close()
    os.remove("sorted.txt.tmp")

if __name__ == "__main__":
    sort() #Sort points using column method
    #sort2() #Sort points using nearest neighbor
    scale() #Scale values into odometry ticks (1.05mm/tick)
    main() #Write to assembly file