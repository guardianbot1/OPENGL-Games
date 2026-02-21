from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math
import random

w_width, w_height = 1280, 720
ballsList = [] #will contain ball objects
size = 11
speed = 0.1
freeze = False
blinkFlag = False ##If it is blinking or not
continuous = True ##Opposite of blink flag. Controls frame skip.
frame_count = 0  # For tracking blinking frames

class Ball: #Draw ball will use these values to draw balls each frame
    def __init__(self, x, y): #Coordinates of where it originated (right clicked)
        self.x = x
        self.y = y
        self.movement = random.choice([(1, 1), (1, -1), (-1, 1), (-1, -1)]) #any corner
        self.color = (random.randint(1,255)/255, random.randint(1,255)/255, random.randint(1,255)/255) #Avoiding pure Black

def scene():

    glLineWidth(5)
    glBegin(GL_LINES)
    glColor3f(0, 1, 0)

    glVertex2f(0,0)
    glVertex2f(w_width,0)

    glVertex2f(w_width, 0)
    glVertex2f(w_width, w_height)

    glVertex2f(w_width, w_height)
    glVertex2f(0, w_height)

    glVertex2f(0, w_height)
    glVertex2f(0,0)

    glEnd()

def draw_ball(ball): #When Blinking, continuos==False, Therefore this func is skiped for few frames, thus creating the blinking effect
    global continuous, size
    if continuous:
        glPointSize(size)
        glBegin(GL_POINTS)
        glColor3f(ball.color[0], ball.color[1], ball.color[2])
        glVertex2d(ball.x, ball.y)
        glEnd()


def animate(): ###Idle Func, continously called
    global ballsList, frame_count, continuous
    
    if blinkFlag: #during blinking state
        frame_count += 1
        if frame_count % 60 == 0:  # Toggle visibility every second for 60 fps. At every multiple of 60, if condition is toggled (on/off)
            continuous = not continuous #draw ball stop, start hote thakbe
    
    for ball in ballsList:
        move_ball(ball)  #Position is changed constantly
    glutPostRedisplay()

def move_ball(ball):#Called in animate
    if not freeze:
        ball.x += ball.movement[0] * speed #coordinate is updating every frame, corner theke deviate
        ball.y += ball.movement[1] * speed
            
        if ball.x + (size // 2) >= w_width or ball.x - (size // 2) <= 0: # Horizontal wall,reverse x. collision ball.x is the centre, so adding the other half
            ball.movement = (-ball.movement[0], ball.movement[1])
        if ball.y + (size // 2) >= w_height or ball.y - (size // 2) <= 0: # Vertical wall collision, reverse y
            ball.movement = (ball.movement[0], -ball.movement[1])


def mouse_cont(button, state, x, y):  # button pressed # state: (pressed or released) #Coord 
    global ballsList, blinkFlag, freeze

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        if not freeze: ##Freezed thakle balls create hobe na
            x, y = x, w_height - y #Mouse input coordinate originates from Top-Right
            new_ball = Ball(x, y)
            ballsList.append(new_ball)
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if not freeze: #Proceed only if running(Unfreeze)
            blinkFlag = not blinkFlag #Toggle blink flag
            if not blinkFlag: #Blinking state e l_click forces visibility=True, Unblink theke blink e gele visibility kisu hobe na (in here), but it does in animate func
                continuous = True

    glutPostRedisplay()

def keyboar_cont(key, x, y):
    global freeze, blinkFlag, continuous
    if key == b' ':
        freeze = not freeze  #Move ball will hault
        if freeze:  #Freeze hole continuous hoye jabe and blinking off
            blinkFlag = False
            continuous = True
    glutPostRedisplay()

def special_keyboar_cont(key, x, y):
    global speed, freeze
    if not freeze:
        if key == GLUT_KEY_UP:
            speed += .5
        elif key == GLUT_KEY_DOWN:
            speed /= 1.2

def iterate():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, w_width, 0, w_height, 0, 1)

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    iterate()
    ###Draw functions are executed every frame. But in this case draw_ball is halted for few frames when it is blinking
    scene()
    for ball in ballsList: #Draws every ball that has been created
        draw_ball(ball)
    glutSwapBuffers()

# Initialization
glutInit()
glutInitWindowSize(w_width, w_height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"Ball Game")

# Main Loop
glutDisplayFunc(showScreen)
glutIdleFunc(animate) ###will be called continuously, and move ball will be called inside animate
glutKeyboardFunc(keyboar_cont)
glutSpecialFunc(special_keyboar_cont)
glutMouseFunc(mouse_cont)

glutMainLoop()