from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

w_width, w_height = 1280, 720

raindrops = []  # Stores rain line's initial vertex
rain_length = 25   #Distance in y plane

wind_effect = 0 # This will bend the rain #Distance in x plane
max_wind_effect = 50  
min_wind_effect = -50 
wind_step = 1 # Bending response time #Bending it slowly

color_shift = 0

def bending_control(key, x, y): #Updates the global var wind_effect #x,y= The mouse cursor position
    global wind_effect, color_shift, day_flag
    if key == GLUT_KEY_LEFT:
        wind_effect = max(min_wind_effect, wind_effect - wind_step) # Draw er time e negetive x add hobe so it bends left # Limit hit korle limit tai return korbe 
    elif key == GLUT_KEY_RIGHT:
        wind_effect = min(max_wind_effect, wind_effect + wind_step) # Bends right

    if color_shift >= 1: #1==White
        color_shift = 1
    if color_shift <= 0: #0==Black
        color_shift = 0

    if key == GLUT_KEY_UP:
            color_shift += 0.01
    if key==GLUT_KEY_DOWN:
        color_shift -= 0.01       

    glutPostRedisplay()

def rain_cord(): #Creating 500 random starting vertex coordinates for rain lines to appear on
    global raindrops        
    if not raindrops:
        for i in range(457):
            x,y=random.randint(-100, w_width+100), random.randint(-w_height, w_height*2) #Range beshi korsi jate edges gular dikeo rain ashe
            raindrops.append([x,y])

def rain():                                
    # Drawing rain-lines
    glColor3f(0.53, 0.81, 0.98)
    glLineWidth(1)
    glBegin(GL_LINES)
    for i in raindrops: #i=[x,y], starting vertex of rain lines
        x, y = i
        glVertex2f(x, y)
        glVertex2f(x + wind_effect, y - rain_length)  # Diagonal rain. adding wind_effect bends it more, subtracting rain length makes the lines longer
    glEnd()


def rain_bending(): #Makes the rain fall and resets. Also takes care of rain bending
    global raindrops
    for drop in raindrops: #drop=[x,y], starting vertex of rain lines
        drop[1] -= rain_length #starting rain's vertex y
        drop[0] += wind_effect #starting rain's vertex x
        
        #Recycling 
        if (drop[1] < -w_height or # screen er niche chole gele
            drop[0] > w_width * 1.5 or #screen er right e chole gele
            drop[0] < -w_width * 0.5): #screen er left e chole gele

            drop[1] = random.randint(0, w_height * 2) #resets y of rain from bottom of screen to top er double. 0 na nile, bend korar time e bottom-side edges gula faka thake cuz rain don't generate on bottom 2 cornes, so rain porte porte oi edge gulai reach kore na
            drop[0] = random.randint(-100, w_width+100) # left and right edges gulai jate jai

    glutPostRedisplay()  #Tells GLUT to redraw the scene, creating the animation effect


def scene():
    global color_shift
    ###BACKGROUND {I'm using 2 triangles to make the ground rectangle}{Another 2 for sky}
    divider = w_height / 1.4  
    glBegin(GL_TRIANGLES)

    glColor3f(color_shift, color_shift, color_shift)
    #Triangle 1 Sky
    glVertex2f(w_width,w_height)
    glVertex2f(0,divider)
    glVertex2f(w_width,divider)
    #Triangle 2 Sky
    glVertex2f(0,divider)
    glVertex2f(0,w_height)
    glVertex2f(w_width,w_height)


    glColor3f(0.478, 0.361, 0.094)
    #Triangle 1 Ground
    glVertex2f(0,0)
    glVertex2f(w_width,0)
    glVertex2f(w_width,divider)
    #Triangle 2 Ground
    glVertex2f(0,0)
    glVertex2f(0,divider)
    glVertex2f(w_width,divider)
    glEnd()

    ###TREES
    for i in range(20):
        width=64
        glBegin(GL_TRIANGLES)
        #Tree Borders
        glColor3f(0.0, 0.0, 0.0)
        glVertex2f(0+(i*64),divider-122)
        glVertex2f(0+(i*64)+64,divider-122)
        glVertex2f(0+(i*64)+32,divider-9)
        #Actual Trees
        glColor3f(0.0, 0.2, 0.0)
        glVertex2f(0+(i*64),divider-123) #Left side

        glColor3f(0.0, 0.2, 0.0)
        glVertex2f(0+(i*64)+64,divider-123) #Right side

        glColor3f(0.13, 0.7, 0.13)
        glVertex2f(0+(i*64)+32,divider-10) #Top
        glEnd()

    ###HOUSE

    #Roof
    
    glColor3f(0.282, 0.145, 0.549)
    glBegin(GL_TRIANGLES)
    w=250
    d=100
    left_roof_edge_x, left_roof_edge_y=(w_width/2) - w , divider-d
    right_roof_edge_x, right_roof_edge_y=(w_width/2) + w ,divider-d 
    glVertex2f(w_width/2,divider+25)
    glVertex2f(left_roof_edge_x, left_roof_edge_y)
    glVertex2f(right_roof_edge_x, right_roof_edge_y)

    #Wall
    glColor3f(0.988, 0.953, 0.91)
    i=20
    j=200
    left_top_x,left_top_y=left_roof_edge_x +i , left_roof_edge_y
    left_foot_x,left_foot_y=left_roof_edge_x +i , left_roof_edge_y-j
    right_top_x,right_top_y=right_roof_edge_x -i, right_roof_edge_y
    right_foot_x,right_foot_y= right_roof_edge_x -i, right_roof_edge_y-j

    glVertex2f(left_foot_x,left_foot_y)
    glVertex2f(right_foot_x,right_foot_y)
    glVertex2f(right_top_x,right_top_y)

    glVertex2f(left_foot_x,left_foot_y)
    glVertex2f(left_top_x,left_top_y)
    glVertex2f(right_top_x,right_top_y)

    ###DOOR
    glColor3f(0.129, 0.588, 1.0)
    t=175 #Width
    u=150 #Height
    d_left_foot_x,d_left_foot_y=left_foot_x + t ,left_foot_y
    d_left_top_x,d_left_top_y=left_foot_x + t ,left_foot_y+u
    d_right_foot_x,d_right_foot_y= right_foot_x - t ,right_foot_y
    d_right_top_x,d_right_top_y= right_foot_x - t ,right_foot_y+u

    glVertex2f(d_left_foot_x,d_left_foot_y)
    glVertex2f(d_right_foot_x,d_right_foot_y)
    glVertex2f(d_right_top_x,d_right_top_y)

    glVertex2f(d_left_foot_x,d_left_foot_y)
    glVertex2f(d_left_top_x,d_left_top_y)
    glVertex2f(d_right_top_x,d_right_top_y)

    glEnd()

    glColor3f(0,0,0)
    glPointSize(10)
    glBegin(GL_POINTS)
    hinge_cord_x,hinge_cord_y=d_right_foot_x-25 ,(d_right_top_y-d_right_foot_y)/2 +d_right_foot_y
    glVertex2f(hinge_cord_x,hinge_cord_y)  #Hinge
    glVertex2f(0,0)
    glEnd()

    ###WINDOWS
    glColor3f(0.129, 0.588, 1.0)
    glBegin(GL_TRIANGLES)

    top_d_w_1st=30
    top_d_w_2nd=111
    m=70 # Window Depression

    #Left Window
    left_window_right_top_x,left_window_right_top_y= d_left_top_x - top_d_w_1st, d_left_top_y
    left_window_left_top_x,left_window_left_top_y= d_left_top_x - top_d_w_2nd, d_left_top_y
    left_window_right_foot_x,left_window_right_foot_y= d_left_top_x - top_d_w_1st, d_left_top_y - m
    left_window_left_foot_x,left_window_left_foot_y= d_left_top_x - top_d_w_2nd, d_left_top_y - m

    glVertex2f(left_window_left_foot_x,left_window_left_foot_y)
    glVertex2f(left_window_right_foot_x,left_window_right_foot_y)
    glVertex2f(left_window_right_top_x,left_window_right_top_y)

    glVertex2f(left_window_left_foot_x,left_window_left_foot_y)
    glVertex2f(left_window_left_top_x,left_window_left_top_y)
    glVertex2f(left_window_right_top_x,left_window_right_top_y)

    #Right Window
    right_window_right_top_x,right_window_right_top_y= d_right_top_x + top_d_w_1st, d_right_top_y
    right_window_left_top_x,right_window_left_top_y= d_right_top_x + top_d_w_2nd, d_right_top_y
    right_window_right_foot_x,right_window_right_foot_y= d_right_top_x + top_d_w_1st, d_right_top_y - m
    right_window_left_foot_x,right_window_left_foot_y= d_right_top_x + top_d_w_2nd, d_right_top_y - m

    glVertex2f(right_window_left_foot_x,right_window_left_foot_y)
    glVertex2f(right_window_right_foot_x,right_window_right_foot_y) 
    glVertex2f(right_window_right_top_x,right_window_right_top_y)

    glVertex2f(right_window_left_foot_x,right_window_left_foot_y)
    glVertex2f(right_window_left_top_x,right_window_left_top_y)
    glVertex2f(right_window_right_top_x,right_window_right_top_y)

    #Left Window Frames  
    glEnd()
    glColor3f(0,0,0)
    glLineWidth(2)
    glBegin(GL_LINES)

    glVertex2f(left_window_left_foot_x+((left_window_right_foot_x-left_window_left_foot_x)/2),left_window_left_foot_y)
    glVertex2f(left_window_left_foot_x+((left_window_right_foot_x-left_window_left_foot_x)/2),left_window_left_top_y)

    glVertex2f(left_window_left_foot_x,left_window_left_foot_y+((left_window_left_top_y-left_window_left_foot_y)/2))
    glVertex2f(left_window_right_foot_x,left_window_left_foot_y+((left_window_left_top_y-left_window_left_foot_y)/2))

    #Right Window Frames
    glVertex2f(right_window_left_foot_x+((right_window_right_foot_x-right_window_left_foot_x)/2),right_window_left_foot_y)
    glVertex2f(right_window_left_foot_x+((right_window_right_foot_x-right_window_left_foot_x)/2),right_window_left_top_y)

    glVertex2f(right_window_left_foot_x,right_window_left_foot_y+((right_window_left_top_y-right_window_left_foot_y)/2))
    glVertex2f(right_window_right_foot_x,right_window_left_foot_y+((right_window_left_top_y-right_window_left_foot_y)/2))

    glEnd()


def iterate():
    glViewport(0, 0, w_width, w_height) ##maps canvas size to window pixels, (start x,start y,end x,end y)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, w_width, 0.0, w_height, 0.0, 1.0)##sets the co-ordinate system througout the window
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def showScreen():#Calls all the drawings
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    ###Draw functions are executed every frame 
    scene()
    rain()
    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(w_width, w_height) #window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice") #Creates Window

rain_cord() 
glutDisplayFunc(showScreen) # Initializes Drawing that are in showscreen
glutIdleFunc(rain_bending)  # For animation #This function is called continuosly when no event takes place. Thus the functions which need constant updates are called via this func

glutSpecialFunc(bending_control) #For Rain Bending via direction keys {glutSpecialFunc makes the func air_bending a special function that handles key inputs}

glutMainLoop()