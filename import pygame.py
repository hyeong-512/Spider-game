import pygame

pygame.init()  # 초기화 설정

# 화면 크기 설정
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = pygame.display.get_surface().get_size()

# 캐릭터 이미지 불러오기
character = pygame.image.load("C:/Users/user/Downloads/gray spider-pixilart.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width - character_width) / 2
character_y_pos = (screen_height - character_height) / 2

to_x = 0
to_y = 0

character_speed = 0.5  # 속도 조금 증가시킴

pygame.display.set_caption("거미게임")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)

# 상태 변수
game_state = 'start'  # 'start', 'play', 'Encyclopedia'
play_start_time = None

# 버튼 위치
start_button_rect = pygame.Rect(500, 450, 200, 80)
button_rect = pygame.Rect(100, 450, 200, 80)

# 메인 루프
running = True
while running:
    dt = clock.tick(60)  # 프레임 시간 (ms)
    screen.fill((255, 255, 255))  # 배경 흰색

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == 'start':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button_rect.collidepoint(event.pos):
                    game_state = 'play'
                    play_start_time = pygame.time.get_ticks()
                elif button_rect.collidepoint(event.pos):
                    game_state = 'Encyclopedia'

        elif game_state == 'play':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    to_x -= character_speed
                elif event.key == pygame.K_RIGHT:
                    to_x += character_speed
                elif event.key == pygame.K_UP:
                    to_y -= character_speed
                elif event.key == pygame.K_DOWN:
                    to_y += character_speed

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    to_x = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    to_y = 0

    # 게임 상태별 화면
    if game_state == 'start':
        start_font = pygame.font.SysFont("malgungothic", 80)
        start_text = start_font.render("spider game", True, (0, 0, 0))
        screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, 150))

        pygame.draw.rect(screen, (0, 0, 0), button_rect, border_radius=10)
        encyclopedia_text = font.render("Encyclopedia", True, (255, 255, 255))
        screen.blit(encyclopedia_text, encyclopedia_text.get_rect(center=button_rect.center))

        pygame.draw.rect(screen, (0, 0, 0), start_button_rect, border_radius=10)
        start_game_text = font.render("Start Game", True, (255, 255, 255))
        screen.blit(start_game_text, start_game_text.get_rect(center=start_button_rect.center))

    elif game_state == 'play':
        background = pygame.image.load("C:/Users/user/Downloads/jungle background-pixilart.png")
        background = pygame.transform.scale(background, (screen_width, screen_height))
        screen.blit(background, (0, 0))

        # 캐릭터 위치 이동
        character_x_pos += to_x * dt
        character_y_pos += to_y * dt

        # 화면 밖으로 못 나가게 제한
        if character_x_pos < 0:
            character_x_pos = 0
        elif character_x_pos > screen_width - character_width:
            character_x_pos = screen_width - character_width

        if character_y_pos < 0:
            character_y_pos = 0
        elif character_y_pos > screen_height - character_height:
            character_y_pos = screen_height - character_height

        # 캐릭터 그리기
        screen.blit(character, (character_x_pos, character_y_pos))

        # "play now!" 텍스트 표시 (1초 동안만)
        current_time = pygame.time.get_ticks()
        if play_start_time is not None and current_time - play_start_time < 1000:
            play_text = font.render("play now!", True, (0, 0, 0))
            screen.blit(play_text, (350, 500))

    elif game_state == 'Encyclopedia':
        background = pygame.image.load("C:/Users/user/OneDrive/바탕 화면/python Workspace/임시 배경화면.png")
        screen.blit(background, (0, 0))
        Encyclopedia_text = font.render('welcome to the show', True, (0, 0, 0))
        screen.blit(Encyclopedia_text, (270, 500))

    pygame.display.update()

pygame.quit()
