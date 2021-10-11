import turtle
import cv2
import numpy as np
import math

SCREEN_HEIGHT=1080 		#provide screen width and height
SCREEN_WIDTH=1920

win=turtle.Screen()
win.screensize(SCREEN_WIDTH,SCREEN_HEIGHT)
win.mode('world')
win.bgcolor("black")
win.title("Render")
win.tracer(10)         #tracer() function turns automatic screen updates on or off (0 for automatic screen updates to be off)

#draw turtle
draw=turtle.Turtle()
draw.shape("arrow")
draw.color("Red")		#to change colour of the turtle
draw.speed(0)           #sets the animation speed to max.

#Functions
def auto_canny(image, sigma=0.33):
	v = np.median(image)
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
	return edged

def distance(x1,y1,x2,y2):
	dist=math.sqrt((x2-x1)**2+(y2-y1)**2)
	return dist


image_name="Tanjiro.jfif" #Desired Image
img = cv2.imread(image_name)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_blur = cv2.GaussianBlur(img_gray, (3,3), 0) 
edge = auto_canny(img_blur)



contours, hierarchy = cv2.findContours(edge, 
    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

  
for i in range(len(contours)):
	for j in range(len(contours[i])-1):
		x1 = contours[i][j][0][0]
		y1 = -contours[i][j][0][1]+325	#to transform the y coordinate so as to see the full image(Put acoordingly)
		x2 = contours[i][j+1][0][0]
		y2 = -contours[i][j+1][0][1]+325
		d=distance(x1,y1,x2,y2)
		draw.penup()
		draw.setposition(x1,y1)
		if x1!=x2:
			m=(y2-y1)/(x2-x1)      #to get the slope of the line .
			draw.pendown()
			draw.lt(m)
			draw.forward(d)
			draw.rt(m)
		if x1==x2 and y1>y2:
			draw.pendown()
			draw.lt(90)
			draw.forward(-d)
			draw.rt(90)
		if x1==x2 and y1<y2:
			draw.pendown()
			draw.lt(90)
			draw.forward(d)
			draw.rt(90)	

draw.hideturtle()			
while True:
	win.update()


win.mainloop()