import pygame

pygame.init() # initialization


screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) #screen size setting
screen_width, screen_height = pygame.display.get_surface().get_size()

pygame.display.set_caption("Spider") # title setting

clock = pygame.time.Clock()

background = pygame.image.load("C:\\Users\\이윤형\\Desktop\\python\\Spider_beta\\game_images\\jungle background-pixilart.png") # importing background image

background = pygame.transform.scale(background, (screen_width, screen_height)) # matching background image

character = pygame.image.load("C:\\Users\\이윤형\\Desktop\\python\\Spider_beta\\game_images\\gray spider-pixilart.png") # importing charater image
character_size = character.get_rect().size # charater size setting
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width - character_width) / 2
character_y_pos = (screen_height - character_height) / 2

to_x = 0
to_y = 0

character_speed = 0.3

running = True
while running : # event loop

    dt = clock.tick(30) # FPS setting

    # print("fps : " + str(clock.get_fps()))

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # closing the window
            running = False

        if event.type == pygame.KEYDOWN : #  character movement
            if event.key == pygame.K_LEFT :
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT :
                to_x += character_speed
            elif event.key == pygame.K_UP :
                to_y -= character_speed
            elif event.key == pygame.K_DOWN : 
                to_y += character_speed

        if event.type == pygame.KEYUP : # character hlat
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                to_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN :
                to_y = 0

    character_x_pos += to_x * dt
    character_y_pos += to_y * dt

    if character_x_pos < 0 : # character movement limit on x
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width :
        character_x_pos = screen_width - character_width
    
    if character_y_pos < 0 : # character movement limit on y
        character_y_pos = 0
    elif character_y_pos > screen_height - character_height :
        character_y_pos = screen_height - character_height

    screen.blit(background, (0, 0)) # drawing game screen

    screen.blit(character, (character_x_pos, character_y_pos)) # drawing game character

    pygame.display.update() # redrawing game screen

pygame.quit() # game termination