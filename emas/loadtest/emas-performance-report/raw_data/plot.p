#output as png image
set terminal png

#save file to "domain.png"
set output "1user_sp1_vs_sp4.png"

#graph title
set title "ab -n 1000 -c 50"

#nicer aspect ratio for image size
set size 1,0.7

# y-axis grid
set grid y

#x-axis label
set xlabel "request"

#y-axis label
set ylabel "response time (ms)"

#plot data from "csv" using column 1 with smooth sbezier lines
#and title of "something" for the given data
plot "1user_sp1_vs_sp4.csv" using 2 smooth sbezier with lines title "something"
