# DriftMania
# Oguz Demirtas

import pygame
import sys
import math

pygame.init()

# Screen specs
screen_width = 1360
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("DriftMania")

# Menu
menu_options = ["START", "HOW TO PLAY", "ABOUT"]
selected_option = 0
menu_background_load = pygame.image.load("menubackground.png")
menu_background = pygame.transform.scale(menu_background_load, (menu_background_load.get_width(), menu_background_load.get_height()))

# Define colors and font for the menu
WHITE = (255, 255, 255)
BLACK = (41, 38, 38)
RED = (214, 9, 69)
font = pygame.font.SysFont("Arial", 36, italic = True, bold = True)
state = "menu"    

# How to play instructions
how_to = pygame.font.SysFont("Arial", 24, italic = True, bold = True)
how_to_text = how_to.render("Use arrow keys to drive.", True, BLACK, (0,255,0))
how_to_text2 = how_to.render("Try to do the highest drift score.", True, BLACK, (0,255,0))
how_to_text3 = how_to.render("If you slow down, leave the drift or hit the barriers your score turns to zero.", True, BLACK, (0,255,0))
how_to_background_load = pygame.image.load("howtobackground.png")
how_to_background = pygame.transform.scale(how_to_background_load, (how_to_background_load.get_width() * 0.8, how_to_background_load.get_height() * 0.8))

# About
about = pygame.font.SysFont("Arial", 20, italic = True, bold = True)
about_text = about.render("DriftMania was developed with Python.", True, BLACK)
about_text2 = about.render("Once upon a time, Oguz Demirtas was bored and wanted to do something to have fun.", True, BLACK)
about_text3 = about.render("And DriftMania was born.", True, BLACK)
about_text4 = about.render("github.com/oguz81/driftmania", True, BLACK)
about_background_load = pygame.image.load("aboutbackground.png")
about_background = pygame.transform.scale(about_background_load, (about_background_load.get_width(), about_background_load.get_height()))

# Barrier class
class Barrier:
    def __init__(self, posx, posy, width, height, angle):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.angle = angle
        self.surf = pygame.Surface((self.width, self.height),pygame.SRCALPHA)
        
    def rotate(self):    # actually, there is no need to rotate the barriers. This function has remained from the previous version.
        the_barrier = pygame.transform.scale(self.surf, (self.surf.get_width() / 1, self.surf.get_height() / 1))
        the_barrier.fill((255, 255, 0))
        rotated_image = pygame.transform.rotate(the_barrier, self.angle)
        new_rect = rotated_image.get_rect(center = the_barrier.get_rect(center = (self.posx, self.posy)).center)
        return rotated_image, new_rect
    
# Define the barriers
barrier1 = Barrier(700, 12, 1300, 5, 0)
barrier1_draw, barrier1_rect = barrier1.rotate()
barrier2 = Barrier(-10, 350, 5, 800, 0)
barrier2_draw, barrier2_rect = barrier2.rotate()
barrier3 = Barrier(690, 690, 1300, 5, 0)
barrier3_draw, barrier3_rect = barrier3.rotate()
barrier4 = Barrier(1390, 350, 5, 800, 0)
barrier4_draw, barrier4_rect = barrier4.rotate()
barrier5 = Barrier(345, 197, 50, 5, 0)
barrier5_draw, barrier5_rect = barrier5.rotate()
barrier6 = Barrier(182, 347, 5, 40, 0)
barrier6_draw, barrier6_rect = barrier6.rotate()
barrier7 = Barrier(356, 511, 50, 5, 0)
barrier7_draw, barrier7_rect = barrier7.rotate()
barrier8 = Barrier(371, 354, 20, 20, 0)
barrier8_draw, barrier8_rect = barrier8.rotate()
barrier9 = Barrier(1100, 217, 10, 10, 0)
barrier9_draw, barrier9_rect = barrier9.rotate()
barrier10 = Barrier(735, 250, 10, 10, 0)
barrier10_draw, barrier10_rect = barrier10.rotate()
barrier11 = Barrier(900, 250, 10, 10, 0)
barrier11_draw, barrier11_rect = barrier11.rotate()
barrier12 = Barrier(900, 340, 10, 10, 0)
barrier12_draw, barrier12_rect = barrier12.rotate()
barrier13 = Barrier(735, 340, 10, 10, 0)
barrier13_draw, barrier13_rect = barrier13.rotate()
barrier14 = Barrier(1010, 500, 10, 10, 0)
barrier14_draw, barrier14_rect = barrier14.rotate()

# Score
score = 0
score_font = pygame.font.SysFont("Arial", 36, italic = True)

# Car specs
car_speed = 0
acceleration = 0.05
brake = -0.08
drag = -0.04
direction = 0  # direction that the car goes through
angle = 0      # angle that car image rotates
steering_wheel = 0
drift = 0

# Load the car image
car_image_load = pygame.image.load("car.png")
car_image = pygame.transform.scale(car_image_load, (car_image_load.get_width() / 10, car_image_load.get_height() / 10))
# Initialize the car position
car_x = screen_width / 2 - car_image.get_width() / 2
car_y = screen_height / 2 - car_image.get_height()

# Load the track image
track_image_load = pygame.image.load("drifttrack1.jpg")
track = pygame.transform.scale(track_image_load, (screen_width, screen_height ))

# Rotation of the car image
def rot_center(image, direction, x, y):
    rotated_image = pygame.transform.rotate(image, direction)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)
    return rotated_image, new_rect


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_option = (selected_option - 1) % len(menu_options)
            elif event.key == pygame.K_DOWN:
                selected_option = (selected_option + 1) % len(menu_options)
            elif event.key == pygame.K_RETURN:
                if selected_option == 0:
                    state = "game"
                elif selected_option == 1:
                    state = "howto"
                elif selected_option == 2:
                    state = "about"
            elif event.key == pygame.K_ESCAPE and state != "game":
                state = "menu"
    if state == "menu":
        screen.blit(menu_background, (0,0))
        for i, option in enumerate(menu_options):
            text = font.render(option, True, RED if i == selected_option else BLACK)
            text_rect = text.get_rect(center=(1200, 250 + i * 50))
            screen.blit(text, text_rect)
    elif state == "game":
        keys = pygame.key.get_pressed()
        # first move
        if keys[pygame.K_UP]:
            car_speed += acceleration
        if keys[pygame.K_DOWN]:
            car_speed -= acceleration
            # when car goes up
        if car_speed > 0:
            if keys[pygame.K_UP]:
                car_speed = car_speed + acceleration # Accelerate when the up key is pressed
            elif keys[pygame.K_DOWN]:
                car_speed = car_speed + brake # Brake when the down key is pressed
            car_speed += drag
        if car_speed < 0: # drag force when goes reverse
            car_speed -= drag
        if car_speed < 2 and car_speed > 0: # set the rotation constant to the speed when low speed
            rotation_constant = car_speed
        elif car_speed > 2:
            rotation_constant = 2 # set the rotation constant to the 2 when high speed
        else:
            rotation_constant = car_speed # set the rotation constant to the speed when goes reverse
        if car_speed < 0 :
            if car_speed < -1.99 and car_speed < 2.01: # limit reverse speed
                car_speed = -2
            # rotation_constant = car_speed
        if car_speed > 4:
            car_speed = 4
       
        if keys[pygame.K_LEFT] and steering_wheel != 180:
            steering_wheel += 12 
        elif keys[pygame.K_RIGHT] and steering_wheel != -180:
            steering_wheel -= 12
 
        if car_speed != 0: 
            direction += steering_wheel * 0.008 * rotation_constant
            angle += steering_wheel * 0.008 * rotation_constant    
            if steering_wheel > 0 :
                steering_wheel -= 6
            elif steering_wheel < 0 :
                steering_wheel += 6
            if keys[pygame.K_LEFT]:
                if angle - direction < 70 and car_speed > 3:
                    angle += 2
            elif angle - direction > 0 :
                angle -= 1
            if keys[pygame.K_RIGHT]:
                if angle - direction > -70 and car_speed > 3:
                    angle -= 2
            elif angle - direction < 0:
                    angle += 1
            if car_speed < 0.041 and car_speed > 0 : # set the car speed to 0 when it is too low
                car_speed = 0
            if car_speed == 0:
                direction = angle
        direction_in_radians = math.radians(direction)
        car_x -= car_speed * math.sin(direction_in_radians)
        car_y -= car_speed * math.cos(direction_in_radians)
        car_image_rotation, car_rect = rot_center(car_image, angle, car_x, car_y)
        #steering_wheel_rotation, steering_wheel_rect = rot_center(steering_wheel_image, steering_wheel, steering_wheel_x, steering_wheel_y) # There was a steering wheel image in the previous version. It has been removed.
   
        # Check for collision
        if barrier1_rect.colliderect(car_rect):
            car_speed += -2
        if barrier2_rect.colliderect(car_rect):
            car_speed += -2
        if barrier3_rect.colliderect(car_rect):
            car_speed += -2
        if barrier4_rect.colliderect(car_rect):
            car_speed += -2
        if barrier5_rect.colliderect(car_rect):
            car_speed += -2
        if barrier6_rect.colliderect(car_rect):
            car_speed += -2
        if barrier7_rect.colliderect(car_rect):
            car_speed += -2
        if barrier8_rect.colliderect(car_rect):
            car_speed += -2
        if barrier9_rect.colliderect(car_rect):
            car_speed += -2
        if barrier10_rect.colliderect(car_rect):
            car_speed += -2
        if barrier11_rect.colliderect(car_rect):
            car_speed += -2
        if barrier12_rect.colliderect(car_rect):
            car_speed += -2
        if barrier13_rect.colliderect(car_rect):
            car_speed += -2
        if barrier14_rect.colliderect(car_rect):
            car_speed += -2
        
        # Score
        if car_speed > 2:
            if abs(angle - direction) > 2 or (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
                score += 1
        else:
            score = 0
        # Clear the screen
        screen.fill((255,255,255))

        # Load the track
        screen.blit(track, (0,0))
        # Draw the car
        screen.blit(car_image_rotation, car_rect)
        # Draw the barriers
        screen.blit(barrier1_draw, barrier1_rect)
        screen.blit(barrier2_draw, barrier2_rect)
        screen.blit(barrier3_draw, barrier3_rect)
        screen.blit(barrier4_draw, barrier4_rect)
        screen.blit(barrier5_draw, barrier5_rect)
        screen.blit(barrier6_draw, barrier6_rect) 
        screen.blit(barrier7_draw, barrier7_rect)
        screen.blit(barrier8_draw, barrier8_rect)
        screen.blit(barrier9_draw, barrier9_rect)
        screen.blit(barrier10_draw, barrier10_rect)
        screen.blit(barrier11_draw, barrier11_rect)
        screen.blit(barrier12_draw, barrier12_rect)
        screen.blit(barrier13_draw, barrier13_rect)
        screen.blit(barrier14_draw, barrier14_rect)
        
        # Draw the score
        score_surface = score_font.render("Score: " + str(score), True, (255, 255, 255), (0,0,0))
        screen.blit(score_surface, (10, 10))
    elif state == "howto":
        screen.blit(how_to_background, (0,0))
        screen.blit(how_to_text, (100, 300))
        screen.blit(how_to_text2, (100, 350))
        screen.blit(how_to_text3, (100, 400))
    elif state == "about":
        screen.blit(about_background, (0,0)) 
        screen.blit(about_text, (100, 250))
        screen.blit(about_text2, (100,300))
        screen.blit(about_text3, (100,350))
        screen.blit(about_text4, (100,400))
      
    pygame.display.flip()
    # Limit the frame rate
    pygame.time.Clock().tick(60)

pygame.quit()