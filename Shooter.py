from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
bullet_cooldown = 0
player_pos = [0, 50, 0]
player_rotation = 0
camera_pos = [0, 500, 500]
camera_angle = 0
camera_height = 500
GRID_LENGTH = 600
WALL_HEIGHT = 100
fovY = 120

lives = 5
score = 0
missed_bullets = 0
game_over = False
cheat_mode = False
v_mode = False
camera_mode = "third" 

enemies = []
bullets = []
BULLET_SPEED = 15
MAX_BULLET_DISTANCE = 1500

PLAYER_SPEED = 15
ROTATION_SPEED = 5
AUTO_ROTATION_SPEED = 2

PLAYER_SCALE = 0.7



class Enemy:
    def __init__(self):
        self.x = random.randint(-GRID_LENGTH + 100, GRID_LENGTH - 100)
        self.z = random.randint(-GRID_LENGTH + 100, GRID_LENGTH - 100)
        self.y = 50
        self.scale = 2
        self.scale_cng = 1
        self.active = True
        self.size = 30
        self.speed = 0.08

    def update(self, player_pos):
        if not self.active: #Inactive hole sesh
            return
            
        # Move towards player if active
        dx = player_pos[0] - self.x
        dz = player_pos[2] - self.z
        distance = math.sqrt(dx**2 + dz**2)
        
        if distance > 0:
            self.x += (dx/distance) * self.speed
            self.z += (dz/distance) * self.speed
        
        # Breathing animation
        self.scale += 0.003 * self.scale_cng #bigger
        if self.scale > 2.5 or self.scale < 1.5:
            self.scale_cng *= -1 #smaller


class Bullet:
    def __init__(self, position, direction):
        self.x, self.y, self.z = position
        #Find bullet trajectory {vetor}
        self.dx = math.sin(math.radians(direction)) * BULLET_SPEED
        self.dz = math.cos(math.radians(direction)) * BULLET_SPEED
        self.distance_traveled = 0

    def update(self):
        self.x += self.dx
        self.z += self.dz
        self.distance_traveled += BULLET_SPEED


def init_enemies():
    global enemies
    enemies = []
    for i in range(5):
        enemies.append(Enemy())


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def keyboardListener(key, x, y):
    global player_pos, player_rotation, cheat_mode, v_mode, game_over, lives, missed_bullets, score
    
    if game_over:
        if key == b'r' or key == b'R':
            # Reset game
            player_pos = [0, 50, 0]
            player_rotation = 0
            init_enemies()
            lives = 5
            missed_bullets = 0
            score = 0
            cheat_mode = False
            v_mode = False
            game_over = False
        return

    key_decoded = key.decode('utf-8').lower() if isinstance(key, bytes) else key.lower()
    
    # Movement controls
    if key_decoded == 'w':
        dx = math.sin(math.radians(player_rotation)) * PLAYER_SPEED
        dz = math.cos(math.radians(player_rotation)) * PLAYER_SPEED
        new_x = player_pos[0] + dx #changing prev pos
        new_z = player_pos[2] + dz
        if abs(new_x) <= GRID_LENGTH - 50 and abs(new_z) <= GRID_LENGTH - 50:
            player_pos[0] = new_x #updating the changed pos is within wall
            player_pos[2] = new_z
    elif key_decoded == 's':
        dx = math.sin(math.radians(player_rotation)) * PLAYER_SPEED
        dz = math.cos(math.radians(player_rotation)) * PLAYER_SPEED
        new_x = player_pos[0] - dx
        new_z = player_pos[2] - dz
        if abs(new_x) <= GRID_LENGTH - 50 and abs(new_z) <= GRID_LENGTH - 50:
            player_pos[0] = new_x
            player_pos[2] = new_z
    elif not cheat_mode and key_decoded == 'd':
        player_rotation -= ROTATION_SPEED
    elif not cheat_mode and key_decoded == 'a':
        player_rotation += ROTATION_SPEED
        
    # Cheat mode 
    elif key_decoded == 'c':
        cheat_mode = not cheat_mode
        print(f"Cheat Mode: {'ON' if cheat_mode else 'OFF'}")
        if not cheat_mode:
            v_mode = False
    elif key_decoded == 'v' and cheat_mode and camera_mode == "first":
        v_mode = not v_mode
        print(f"Special Camera Mode: {'ON' if v_mode else 'OFF'}")


def specialKeyListener(key, x, y):
    global camera_angle, camera_height
    if key == GLUT_KEY_UP:
        camera_height += 30
        if camera_height > 1000:
            camera_height = 1000
    elif key == GLUT_KEY_DOWN:
        camera_height -= 30
        if camera_height < 100:
            camera_height = 100
    elif key == GLUT_KEY_LEFT:
        camera_angle -= 5
    elif key == GLUT_KEY_RIGHT:
        camera_angle += 5


def mouseListener(button, state, x, y):
    global camera_mode, bullets
    if game_over:
        return
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Fire bullet
        start_x = player_pos[0] + math.sin(math.radians(player_rotation)) * 50
        start_z = player_pos[2] + math.cos(math.radians(player_rotation)) * 50
        bullets.append(Bullet((start_x, player_pos[1] + 70, start_z), player_rotation))
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        # Toggle camera mode
        camera_mode = "first" if camera_mode == "third" else "third"


def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    if camera_mode == "third":
        # Third-person camera
        x = 500 * math.sin(math.radians(camera_angle))
        z = 500 * math.cos(math.radians(camera_angle))
        y = camera_height
        gluLookAt(x, y, z, 0, 0, 0, 0, 1, 0)
    else:
        # First-person camera
        head_height = player_pos[1] + 90
        cam_x = player_pos[0]
        cam_y = head_height
        cam_z = player_pos[2]
        
        if cheat_mode and v_mode:
            # Special camera mode
            cam_y += 50
            # Find closest enemy to look at
            closest_enemy = None
            min_distance = float('inf')
            
            for enemy in enemies:
                if not enemy.active:
                    continue
                dx = enemy.x - player_pos[0]
                dz = enemy.z - player_pos[2]
                distance = math.sqrt(dx**2 + dz**2)
                
                if distance < min_distance:
                    min_distance = distance
                    closest_enemy = enemy
            
            if closest_enemy:
                look_x = closest_enemy.x
                look_y = closest_enemy.y + 30
                look_z = closest_enemy.z
            else:
                look_x = cam_x + math.sin(math.radians(player_rotation)) * 100
                look_y = cam_y
                look_z = cam_z + math.cos(math.radians(player_rotation)) * 100
        else: #Normal 1st person
            look_x = cam_x + math.sin(math.radians(player_rotation)) * 100
            look_y = cam_y
            look_z = cam_z + math.cos(math.radians(player_rotation)) * 100

        gluLookAt(cam_x, cam_y, cam_z, look_x, look_y, look_z, 0, 1, 0)


def draw_player():
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2])
    glRotatef(player_rotation, 0, 1, 0)
    glScalef(PLAYER_SCALE, PLAYER_SCALE, PLAYER_SCALE)

    # Torso (Green cuboid)
    glPushMatrix()
    glColor3f(85/255.0, 107/255.0, 47/255.0)
    glTranslatef(0, 60, 0)
    glScalef(40, 80, 40)
    glutSolidCube(1)
    glPopMatrix()

    # Head (Black sphere)
    glPushMatrix()
    glColor3f(0.0, 0.0, 0.0)
    glTranslatef(0, 110, 0)
    glutSolidSphere(20, 20, 20)
    glPopMatrix()

    # Arms
    glPushMatrix()
    glColor3f(255/255.0, 224/255.0, 189/255.0)
    # Right arm
    glPushMatrix()
    glTranslatef(25, 70, 0)
    glRotatef(90, 0, 0, 1)
    gluCylinder(gluNewQuadric(), 10, 10, 50, 20, 20)
    glPopMatrix()
    # Left arm
    glPushMatrix()
    glTranslatef(-25, 70, 0)
    glRotatef(90, 0, 0, 1)
    gluCylinder(gluNewQuadric(), 10, 10, 50, 20, 20)
    glPopMatrix()
    glPopMatrix()

    # Legs
    glColor3f(0/255.0, 0/255.0, 255/255.0)
    # Right leg
    glPushMatrix()
    glTranslatef(12, 20, 0)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 12, 6, 60, 20, 20)
    glPopMatrix()
    # Left leg
    glPushMatrix()
    glTranslatef(-12, 20, 0)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 12, 6, 60, 20, 20)
    glPopMatrix()

    # Gun
    glPushMatrix()
    glColor3f(192/255.0, 192/255.0, 192/255.0)
    glTranslatef(0, 70, 15)
    gluCylinder(gluNewQuadric(), 8, 3, 60, 20, 20)
    glTranslatef(0, 0, -10)
    gluCylinder(gluNewQuadric(), 13, 8, 10, 20, 20)
    glTranslatef(0, 0, 70)
    glutSolidSphere(3, 10, 10)
    glPopMatrix()

    glPopMatrix()


def draw_player_dead():
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2])
    glRotatef(90, 1, 0, 0)
    glRotatef(player_rotation, 0, 0, 1)
    glScalef(PLAYER_SCALE, PLAYER_SCALE, PLAYER_SCALE)

    # Torso (Green cuboid)
    glPushMatrix()
    glColor3f(85/255.0, 107/255.0, 47/255.0)
    glTranslatef(0, 0, 60)
    glScalef(40, 40, 80)
    glutSolidCube(1)
    glPopMatrix()

    # Head (Black sphere)
    glPushMatrix()
    glColor3f(0.0, 0.0, 0.0)
    glTranslatef(0, 0, 110)
    glutSolidSphere(20, 20, 20)
    glPopMatrix()

    # Arms
    glPushMatrix()
    glColor3f(255/255.0, 224/255.0, 189/255.0)
    # Right arm
    glPushMatrix()
    glTranslatef(25, 0, 70)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 10, 10, 50, 20, 20)
    glPopMatrix()
    # Left arm
    glPushMatrix()
    glTranslatef(-25, 0, 70)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 10, 10, 50, 20, 20)
    glPopMatrix()
    glPopMatrix()

    # Legs
    glColor3f(0/255.0, 0/255.0, 255/255.0)
    # Right leg
    glPushMatrix()
    glTranslatef(12, 0, 20)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 12, 6, 60, 20, 20)
    glPopMatrix()
    # Left leg
    glPushMatrix()
    glTranslatef(-12, 0, 20)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 12, 6, 60, 20, 20)
    glPopMatrix()

    # Gun
    glPushMatrix()
    glColor3f(192/255.0, 192/255.0, 192/255.0)
    glTranslatef(-40, 0, 60)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 8, 3, 60, 20, 20)
    glTranslatef(0, 0, -10)
    gluCylinder(gluNewQuadric(), 13, 8, 10, 20, 20)
    glTranslatef(0, 0, 70)
    glutSolidSphere(3, 10, 10)
    glPopMatrix()

    glPopMatrix()


def draw_enemies():
    for enemy in enemies:
        if not enemy.active:
            continue
            
        glPushMatrix()
        glTranslatef(enemy.x, enemy.y, enemy.z)
        glScalef(enemy.scale, enemy.scale, enemy.scale)
        
        # Body (Red sphere)
        glColor3f(1, 0, 0)
        glutSolidSphere(20, 20, 20)
        
        # Head (Black sphere)
        glTranslatef(0, 30, 0)
        glColor3f(0, 0, 0)
        glutSolidSphere(15, 20, 20)
        
        glPopMatrix()


def draw_bullets():
    glColor3f(1, 1, 0)
    for bullet in bullets:
        glPushMatrix()
        glTranslatef(bullet.x, bullet.y, bullet.z)
        glutSolidCube(10)
        glPopMatrix()


def draw_grid():
    for i in range(-GRID_LENGTH, GRID_LENGTH, 100):
        for j in range(-GRID_LENGTH, GRID_LENGTH, 100):
            glBegin(GL_QUADS)
            if (i // 100 + j // 100) % 2 == 0:
                glColor3f(1, 1, 1)
            else:
                glColor3f(0.69, .50, 0.949)
            glVertex3f(i, 0, j)
            glVertex3f(i + 100, 0, j)
            glVertex3f(i + 100, 0, j + 100)
            glVertex3f(i, 0, j + 100)
            glEnd()

    # walls
    glColor3f(0, 1, 0)
    glBegin(GL_QUADS)
    glVertex3f(GRID_LENGTH, 0, -GRID_LENGTH)
    glVertex3f(GRID_LENGTH, 0, GRID_LENGTH)
    glVertex3f(GRID_LENGTH, WALL_HEIGHT, GRID_LENGTH)
    glVertex3f(GRID_LENGTH, WALL_HEIGHT, -GRID_LENGTH)
    glEnd()

    glColor3f(0, 0, 1)
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, 0, -GRID_LENGTH)
    glVertex3f(-GRID_LENGTH, 0, GRID_LENGTH)
    glVertex3f(-GRID_LENGTH, WALL_HEIGHT, GRID_LENGTH)
    glVertex3f(-GRID_LENGTH, WALL_HEIGHT, -GRID_LENGTH)
    glEnd()

    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, 0, GRID_LENGTH)
    glVertex3f(GRID_LENGTH, 0, GRID_LENGTH)
    glVertex3f(GRID_LENGTH, WALL_HEIGHT, GRID_LENGTH)
    glVertex3f(-GRID_LENGTH, WALL_HEIGHT, GRID_LENGTH)
    glEnd()

    glColor3f(0, 1, 1)
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, 0, -GRID_LENGTH)
    glVertex3f(GRID_LENGTH, 0, -GRID_LENGTH)
    glVertex3f(GRID_LENGTH, WALL_HEIGHT, -GRID_LENGTH)
    glVertex3f(-GRID_LENGTH, WALL_HEIGHT, -GRID_LENGTH)
    glEnd()


def draw_first_person_gun():
    glPushMatrix()
    # Position at bottom-center of the screen
    glTranslatef(500, 100, 0)
    glScalef(2.5, 2.5, 2.5)
    glRotatef(-75, 1, 0, 0)

    # Gun Model
    glColor3f(192/255.0, 192/255.0, 192/255.0)
    gun_length = 40
    gun_base_radius = 5
    gun_top_radius = 3
    
    # Barrel
    gluCylinder(gluNewQuadric(), gun_base_radius, gun_top_radius, gun_length, 20, 20)
    
    # Base
    glPushMatrix()
    glTranslatef(0, 0, -8)
    gluCylinder(gluNewQuadric(), gun_base_radius + 3, gun_base_radius, 8, 20, 20)
    glPopMatrix()
    
    # Tip
    glTranslatef(0, 0, gun_length)
    glutSolidSphere(gun_top_radius, 10, 10)

    # Hands
    glColor3f(255/255.0, 224/255.0, 189/255.0)
    hand_radius = 6
    glPushMatrix()
    glTranslatef(gun_base_radius, -hand_radius*0.5, 5)
    glutSolidSphere(hand_radius, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-gun_base_radius, -hand_radius*0.5, 5)
    glutSolidSphere(hand_radius, 10, 10)
    glPopMatrix()

    glPopMatrix()


def check_collisions():
    global bullets, score, lives, missed_bullets, game_over
    
    # Bullet-enemy collisions
    for bullet in bullets[:]: #checking every enemy for every bullet
        for enemy in enemies:
            if not enemy.active:
                continue
                
            distance = math.sqrt((bullet.x - enemy.x)**2 +(bullet.z - enemy.z)**2)
            
            if distance < enemy.size:
                enemy.active = False
                if bullet in bullets:
                    bullets.remove(bullet)
                score += 1
                # Respawn enemy
                enemy.x = random.randint(-GRID_LENGTH + 100, GRID_LENGTH - 100)
                enemy.z = random.randint(-GRID_LENGTH + 100, GRID_LENGTH - 100)
                enemy.active = True
                break

    # Enemy-player collisions
    for enemy in enemies:
        if not enemy.active:
            continue
            
        distance = math.sqrt((player_pos[0] - enemy.x)**2 +(player_pos[2] - enemy.z)**2)
        
        if distance < enemy.size + 40:
            lives -= 1
            enemy.active = False
            # Respawn enemy
            enemy.x = random.randint(-GRID_LENGTH + 100, GRID_LENGTH - 100)
            enemy.z = random.randint(-GRID_LENGTH + 100, GRID_LENGTH - 100)
            enemy.active = True
            
            if lives <= 0:
                game_over = True


def idle():
    global bullets, player_rotation, missed_bullets, game_over, bullet_cooldown
    
    if game_over:
        glutPostRedisplay()
        return
    
    # Decrease cooldown if active
    if bullet_cooldown > 0:
        bullet_cooldown -= 1
    
    # Cheat mode functionality
    if cheat_mode:
        # Auto-rotation
        player_rotation += AUTO_ROTATION_SPEED
        player_rotation %= 360
        
        # Auto-firing at enemies in line of sight (with cooldown)
        if bullet_cooldown == 0:
            for enemy in enemies:
                if not enemy.active:
                    continue
                    
                dx = enemy.x - player_pos[0]
                dz = enemy.z - player_pos[2]
                distance = math.sqrt(dx**2 + dz**2)
                
                if distance > 0:
                    # Calculate angle to enemy
                    angle_to_enemy = math.degrees(math.atan2(dx, dz)) % 360
                    angle_diff = abs((angle_to_enemy - player_rotation + 180) % 360 - 180)
                    
                    # Check if enemy is in line of sight
                    if angle_diff < 10:
                        # Fire bullet
                        start_x = player_pos[0] + math.sin(math.radians(player_rotation)) * 50
                        start_z = player_pos[2] + math.cos(math.radians(player_rotation)) * 50
                        bullets.append(Bullet((start_x, player_pos[1] + 70, start_z), player_rotation))
                        bullet_cooldown = 10
                        break
    
    # Update enemies
    for enemy in enemies:
        enemy.update(player_pos)
    
    # Update bullets
    bullets_to_remove = []
    for bullet in bullets:
        bullet.update()
        
        # Check if bullet is out of bounds
        if (abs(bullet.x) > GRID_LENGTH or 
            abs(bullet.z) > GRID_LENGTH or 
            bullet.distance_traveled > MAX_BULLET_DISTANCE):
            bullets_to_remove.append(bullet)
            missed_bullets += 1
            
            if missed_bullets >= 10:
                game_over = True
    
    # Remove out-of-bounds bullets
    for bullet in bullets_to_remove:
        if bullet in bullets:
            bullets.remove(bullet)
    
    # Check collisions
    check_collisions()
    
    glutPostRedisplay()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glViewport(0, 0, 1000, 800)

    # Set up 3D projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(80, 1.25, 0.1, 1500)

    # Set up camera
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    setupCamera()
    glEnable(GL_DEPTH_TEST)

    # Draw 3D scene
    draw_grid()
    
    if not game_over:
        if camera_mode == "third":
            draw_player()
        draw_enemies()
    else:
        draw_player_dead()
        
    draw_bullets()

    # Set up 2D overlay
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)

    
    if not game_over and camera_mode == "first":
        draw_first_person_gun()

    # UI text
    if not game_over:        
        draw_text(10, 770, f"Player Life Remaining: {lives}")
        draw_text(10, 750, f"Game Score: {score}")
        draw_text(10, 730, f"Player Bullet Missed: {missed_bullets}")
    else:
        # Game over text
        glColor3f(0, 0, 0)
        glBegin(GL_QUADS)
        glVertex2f(370, 430)
        glVertex2f(620, 430)
        glVertex2f(620, 350)
        glVertex2f(370, 350)
        glEnd()
        
        draw_text(400, 400, "GAME OVER")
        draw_text(400, 380, f"Your Score: {score}")
        draw_text(400, 360, "Press R to restart.")

    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

    glutSwapBuffers()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Bullet Frenzy")
    
    glEnable(GL_DEPTH_TEST)
    
    # Initialize game
    init_enemies()
    
    # Register callbacks
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    
    glutMainLoop()


if __name__ == "__main__":
    main()