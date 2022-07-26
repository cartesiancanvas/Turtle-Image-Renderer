import turtle
import cv2
import numpy as np
import math

SCREEN_HEIGHT=1080 		#provide screen width and height
SCREEN_WIDTH=1920

win=turtle.Screen()
win.screensize(SCREEN_WIDTH,SCREEN_HEIGHT)	#provides the width and height of the space the turtle can draw in
win.setup(SCREEN_WIDTH, SCREEN_HEIGHT)   	#provides the width and the height of the window
win.mode('world')
win.bgcolor("black")
win.title("Render")
win.tracer(10,0)         #tracer() function turns automatic screen updates on or off (0 for automatic screen updates to be off)

#draw turtle
draw=turtle.Turtle()
draw.shape("arrow")
draw.color("Red")		#to change colour of the turtle
draw.speed(0)           #sets the animation speed to max.

#Functions
def dim_img(image_name):
  img = cv2.imread(image_name)
  dimensions = img.shape
  height = img.shape[0]
  width = img.shape[1]
  return width,height

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



contours, hierarchy = cv2.findContours(edge,   #https://docs.opencv.org/4.x/d9/d8b/tutorial_py_contours_hierarchy.html
    cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)     

  

xoff=int(dim_img(image_name)[1])/2
yoff=int(dim_img(image_name)[0])/2
	
for i in range(len(contours)):
	for j in range(len(contours[i])-1):
		x1 = contours[i][j][0][0]-xoff
		y1 = -contours[i][j][0][1]+yoff	 #to transform the x and y coordinate so as to see the center the  image(Put acoordingly)
		x2 = contours[i][j+1][0][0]-xoff
		y2 = -contours[i][j+1][0][1]+yoff
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
