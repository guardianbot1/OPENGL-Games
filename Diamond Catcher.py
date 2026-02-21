from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# Game constants and variables
w_width, w_height = 1280, 720
move = 0 #Handles Catcher Movement
score = 0
game_over = False
paused = False
diamond_speed = 2 #Base falling speed
speed_increase = 0.02 #Increase with each score
diamond_pos = [0, 0] #will change in gen_new_dia
diamond_color = [1.0, 1.0, 1.0]  # Default white
catcher_color = [1.0, 1.0, 1.0]  # White #Will cng to Red
diamond_active = False # No diamonds at the start # Generate Diamond will turn it on

# Button positions centers and size #Will make button box with this
button_size = 30
restart_button = [50, w_height - 50]
playpause_button = [w_width // 2, w_height - 50]
exit_button = [w_width - 50, w_height - 50]

#******************************************************************************************************************************************************#
def zone_finder(start, end):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    
    # If line has no lenght
    if dx == 0 and dy == 0:
        return 0  
    
    # If line falls on axis
    if dx == 0:  # Vertical line
        return 2 if dy > 0 else 6
    
    if dy == 0:  # Horizontal line
        return 0 if dx > 0 else 4
    
    # If line falls on diagonal division line |dx| == |dy|
    if abs(dx) == abs(dy):
        if dx > 0 and dy > 0:  
            return 1
        elif dx < 0 and dy > 0: 
            return 2
        elif dx < 0 and dy < 0:
            return 5
        elif dx > 0 and dy < 0:
            return 6
    
    # Normal cases
    if abs(dx) > abs(dy):  # Zones 0, 3, 4, 7 |dx| > |dy|
        if dx > 0:
            return 0 if dy > 0 else 7
        else:
            return 3 if dy > 0 else 4
    else:  # Zones 1, 2, 5, 6 |dy| > |dx|
        if dy > 0:
            return 1 if dx > 0 else 2
        else:
            return 6 if dx > 0 else 5
        
def zone_converter(point, current_zone, target_zone):
    x, y = point
    
    # If already in target zone
    if current_zone == target_zone:
        return (x, y)
    
    #convert to zone 0
    if current_zone != 0:
        x, y = convert_to_zone0(x, y, current_zone)
    
    #convert from zone 0 to target zone
    if target_zone != 0:
        x, y = convert_from_zone0(x, y, target_zone)
    
    return (x, y)

def convert_to_zone0(x, y, current_zone):
    if current_zone == 0:
        return (x, y)
    elif current_zone == 1:
        return (y, x)
    elif current_zone == 2:
        return (y, -x)
    elif current_zone == 3:
        return (-x, y)
    elif current_zone == 4:
        return (-x, -y)
    elif current_zone == 5:
        return (-y, -x)
    elif current_zone == 6:
        return (-y, x)
    elif current_zone == 7:
        return (x, -y)

def convert_from_zone0(x, y, target_zone):
    if target_zone == 0:
        return (x, y)
    elif target_zone == 1:
        return (y, x)
    elif target_zone == 2:
        return (-y, x)
    elif target_zone == 3:
        return (-x, y)
    elif target_zone == 4:
        return (-x, -y)
    elif target_zone == 5:
        return (-y, -x)
    elif target_zone == 6:
        return (y, -x)
    elif target_zone == 7:
        return (x, -y)

def mpl(start, end):
    x0, y0 = start
    x1, y1 = end
    
    zone = zone_finder(start, end)
    x0_z0, y0_z0 = zone_converter((x0, y0), zone, 0)
    x1_z0, y1_z0 = zone_converter((x1, y1), zone, 0)
    
    dx = x1_z0 - x0_z0
    dy = y1_z0 - y0_z0
    d_old = 2*dy - dx
    dE = 2*dy
    dNE = 2*(dy - dx)
    
    x, y = x0_z0, y0_z0
    pixels_z0 = [(x, y)]
    
    while x < x1_z0:
        if d_old <= 0:  # East
            x += 1
            d_old += dE
        else:  # Northeast
            x += 1
            y += 1
            d_old += dNE
        pixels_z0.append((x, y))
    
    # Converting all pixels to original zone
    pixels = []
    for i in pixels_z0:
        original_point = zone_converter(i, 0, zone)
        pixels.append(original_point)
    
    return pixels
#******************************************************************************************************************************************************#

def generate_new_diamond(): # Determines the changed dia_pos, dia_color and it's speed
    global diamond_pos, diamond_color, diamond_active, diamond_speed
    
    diamond_pos = [random.randint(100, w_width - 100), w_height - 50]

    base_brightness = 0.7
    diamond_color = [random.uniform(base_brightness, 1.0), random.uniform(0.5, 1.0),random.uniform(0.5, 1.0)]
    random.shuffle(diamond_color) #Shuffles the element of the list
    
    diamond_active = True
    diamond_speed = 0.1 + (score * speed_increase)
#========================================Drawings Down===============================
def draw_diamond(): #Won't draw at 1st due to dia_act flag, generate_new_dia must be called first (it is called through idle func)
    if not diamond_active: #If dia_act==True then False (won't return), if dia_act==False then True (will return)
        return
    
    #Taking center point and streching it equally on 4 sides #center position gen_new_dia changes in update dia
    size = 15
    top = (diamond_pos[0], diamond_pos[1] + size) #diamond_pos is changing cuz of update_dia
    bottom = (diamond_pos[0], diamond_pos[1] - size)
    left = (diamond_pos[0] - size, diamond_pos[1])
    right = (diamond_pos[0] + size, diamond_pos[1])   
    #Getting the pixels     
    top_right=mpl(top, right)
    right_bottom=mpl(right, bottom)
    bottom_left=mpl(bottom, left)
    left_top=mpl(left, top)
 
    glPointSize(2)
    glBegin(GL_POINTS)
    glColor3f(diamond_color[0], diamond_color[1], diamond_color[2])
    #Drawing the 4 lines
    for x, y in top_right:
        glVertex2f(x, y)
    for x, y in right_bottom:
        glVertex2f(x, y)
    for x, y in bottom_left:
        glVertex2f(x, y)
    for x, y in left_top:
        glVertex2f(x, y)    
    glEnd()
#========================================Drawings Up===============================

def update_diamond(): #diamond fall, score and hit detection
    global diamond_pos, diamond_active, score, game_over, catcher_color
    #update when dhukbe na therefore when false ashbe
    if not diamond_active or paused or game_over: #update when dia_act==True or not paused or not over
        return
    
    diamond_pos[1] -= diamond_speed 
    
    catcher_left = (w_width/2) - 65 + move
    catcher_right = (w_width/2) + 65 + move
    
    if diamond_pos[1] <= 25:
        if catcher_left <= diamond_pos[0] <= catcher_right:
            # Diamond caught
            score += 1
            print(f"Score: {score}")
            diamond_active = False
            generate_new_diamond()  # Generate new diamond immediately
        else:
            # Diamond missed
            game_over = True
            catcher_color = [1.0, 0.0, 0.0]  # Red
            print(f"Game Over! Final Score: {score}")
            diamond_active = False
#========================================Drawings Down===============================
def draw_buttons():
    # Restart button (left arrow)

    #End coords of the arrows
    arrow_right_end=(80, w_height - 50)
    arrow_left_end=(20, w_height - 50)
    arrow_up_slant_end=(20+10,w_height - 50 + 10)
    arrow_down_slant_end=(20+10,w_height - 50 - 10)
    #Getting the Points
    arrow_base=mpl(arrow_right_end,arrow_left_end)
    arrow_up=mpl(arrow_left_end,arrow_up_slant_end)
    arrow_down=mpl(arrow_left_end,arrow_down_slant_end)
    #Drawing
    glPointSize(3)
    glColor3f(0.0, 1.0, 1.0) # Teal
    glBegin(GL_POINTS)
    for x, y in arrow_base:
        glVertex2f(x, y)
    for x, y in arrow_up:
        glVertex2f(x, y)
    for x, y in arrow_down:
        glVertex2f(x, y)    
    glEnd()
    
    # Play/Pause button
    if paused:        
        # Play icon (Triangle)
        right_cent=(w_width/2 + 15, w_height - 50)
        left_bot=(w_width/2 - 15, w_height - 50 - 15)
        left_top=(w_width/2 - 15, w_height - 50 + 15)
        #Getting the Points
        up_arm=mpl(right_cent,left_top)
        bot_arm=mpl(right_cent, left_bot)
        left=mpl(left_bot,left_top)
        #Drawing
        glPointSize(3)
        glColor3f(1.0, 0.75, 0.0) # Amber
        glBegin(GL_POINTS)
        for x, y in up_arm:
            glVertex2f(x, y)
        for x, y in bot_arm:
            glVertex2f(x, y)
        for x, y in left:
            glVertex2f(x, y)    
        glEnd()
    else:
        # Play icon (2 lines) [w_width // 2, w_height - 50]
        y_change=17
        left_top=(w_width // 2 - y_change, w_height - 50 + y_change)
        left_bot=(w_width // 2 - y_change, w_height - 50 - y_change)
        right_top=(w_width // 2 + y_change, w_height - 50 + y_change)
        right_bot=(w_width // 2 + y_change, w_height - 50 - y_change)
        #Getting the Points
        left=mpl(left_top,left_bot)
        right=mpl(right_top,right_bot)
        #Drawing
        glPointSize(3)
        glColor3f(1.0, 0.75, 0.0) # Amber
        glBegin(GL_POINTS)
        for x, y in left:
            glVertex2f(x, y)
        for x, y in right:
            glVertex2f(x, y)
        glEnd()

    # Exit button (X)
    x_center_x,x_center_y=(w_width - 50, w_height - 50)
    x_change=15
    y_change=15
    left_top=( x_center_x - x_change,x_center_y + y_change)
    left_bot=( x_center_x - x_change,x_center_y - y_change)
    right_top=( x_center_x + x_change,x_center_y + y_change)
    right_bot=( x_center_x + x_change ,x_center_y - y_change)
    #Getting the Points
    left_right=mpl(left_top,right_bot)
    right_left=mpl(right_top,left_bot)
    #Drawing
    glPointSize(3)
    glColor3f(1.0, 0.0, 0.0)  # Red
    glBegin(GL_POINTS)
    for x, y in left_right:
        glVertex2f(x, y)
    for x, y in right_left:
        glVertex2f(x, y)
    glEnd()
#========================================Drawings Up===============================

def clicked_where(x, y):
    global paused, game_over, score, move, diamond_active
    y = w_height - y   # Y is flipped for mouse 

    #Check restart button
    if (restart_button[0] - button_size <= x <= restart_button[0] + button_size and
        restart_button[1] - button_size <= y <= restart_button[1] + button_size):
        reset_game()
        print("Starting Over")    
    # Check play/pause button
    elif (playpause_button[0] - button_size <= x <= playpause_button[0] + button_size and
          playpause_button[1] - button_size <= y <= playpause_button[1] + button_size):
        if not game_over:
            paused = not paused    #Toggling pause flag
    # Check exit button
    elif (exit_button[0] - button_size <= x <= exit_button[0] + button_size and
          exit_button[1] - button_size <= y <= exit_button[1] + button_size):
        print(f"Goodbye! Your score was: {score}")
        glutLeaveMainLoop()

def reset_game():
    global score, game_over, paused, move, catcher_color, diamond_active
    #reverting all pointers to initial value
    score = 0
    game_over = False
    paused = False
    move = 0
    catcher_color = [1.0, 1.0, 1.0] #White
    diamond_active = False
    generate_new_diamond()

def bending_control(key, x, y): #Bends the Catcher
    global move    
    if game_over or paused: #game_over==True or paused==True  (Then don't run, just return)
        return  
    #Move is the current deviation of the the catcher. Initially 0
    step = 10  # Catcher Movement Speed
    if key == GLUT_KEY_LEFT:
        if (w_width/2)-65 + move - step > 0: #checks if another step is possible from the current position #(w_width/2)-65 + move is the current position
            move -= step
    elif key == GLUT_KEY_RIGHT:
        if (w_width/2)+65 + move + step < w_width:
            move += step    
    glutPostRedisplay()

#========================================Drawings Down===============================
def catcher():
    global move
    #Calculating the 4 X of the 4 corners of the catcher
    base_left = (w_width/2)-50 + move # move changes in ben_cont
    base_right = (w_width/2)+50 + move
    top_left = (w_width/2)-65 + move
    top_right = (w_width/2)+65 + move

    # Getting the points to draw the catcher
    catcher_base = mpl((base_left, 5), (base_right, 5))
    catcher_left = mpl((base_left, 5), (top_left, 20))
    catcher_right = mpl((base_right, 5), (top_right, 20))
    catcher_top = mpl((top_left, 21), (top_right, 21))

    glPointSize(2) 
    glBegin(GL_POINTS)
    glColor3f(catcher_color[0], catcher_color[1], catcher_color[2])
    #Drawing the points for the catcher
    for x, y in catcher_base:
        glVertex2f(x, y)
    for x, y in catcher_left:
        glVertex2f(x, y)
    for x, y in catcher_right:
        glVertex2f(x, y)
    for x, y in catcher_top:
        glVertex2f(x, y)
    
    glEnd()
#========================================Drawings Up===============================

def mouse_click(button, state, x, y): #sends mouse coord to clicked_where
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        clicked_where(x, y)
        glutPostRedisplay()

def idle_func(): #Called repetedly.Therefore, update_dia and gen_new_dia always called
    global diamond_active
    #updating diamond repetedly if game_over and paused==False
    if not game_over and not paused: 
        update_diamond()
        glutPostRedisplay()
    #Generating dia if dia_act and game_over and paused==False
    if not diamond_active and not game_over and not paused: 
        generate_new_diamond() #Dia_act =True will be done in gen_new_dia

def iterate():
    glViewport(0, 0, w_width, w_height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, w_width, 0.0, w_height, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    
    # Drawing Functions Below
    catcher()
    draw_diamond()
    draw_buttons()
    
    glutSwapBuffers()

# Main program
glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(w_width, w_height)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Catch the Diamonds!")

glutDisplayFunc(showScreen) #Actual Drawings (vertex2f)
glutSpecialFunc(bending_control) #keyboard presses for catcher
glutMouseFunc(mouse_click) #Mouse click for buttons
glutIdleFunc(idle_func)  # Using this for all animations

glutMainLoop()