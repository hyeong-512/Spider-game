import pygame
from scripts.character import Character  # ★ 분리한 캐릭터 클래스 임포트

pygame.init()

# ----------------- 화면/글꼴/시계 기본 설정 -----------------
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = pygame.display.get_surface().get_size()
pygame.display.set_caption("거미게임")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)
title_font = pygame.font.SysFont("malgungothic", 80)

# ----------------- 이미지 로드: 시작 시 1번만 -----------------
# convert/convert_alpha()를 해두면 blit 성능이 올라가요.
background = pygame.image.load(
    r"C:/Users/user/Downloads/jungle background-pixilart.png"
).convert()
background = pygame.transform.scale(background, (screen_width, screen_height))

# 캐릭터는 클래스로 관리
character_img_path = r"C:/Users/user\Downloads/gray spider-pixilart.png"
character_speed = 300  # px/s (초당 이동 픽셀수)
# 화면 중앙 배치
character = Character(
    image_path=character_img_path,
    start_pos=((screen_width // 2), (screen_height // 2)),
    speed=character_speed
)

# ----------------- 버튼/상태 -----------------
game_state = 'start'  # 'start', 'play', 'Encyclopedia'
play_start_time = None

# 화면 비율에 맞춰 중앙정렬 버튼 배치 (가변 해상도 대응)
start_button_rect = pygame.Rect(0, 0, 240, 80)
start_button_rect.center = (screen_width // 2, int(screen_height * 0.65))

encyclopedia_button_rect = pygame.Rect(0, 0, 240, 80)
encyclopedia_button_rect.center = (screen_width // 2, int(screen_height * 0.78))

exit_button_rect = pygame.Rect(0, 0, 240, 80)
exit_button_rect.center = (screen_width // 2 , int(screen_height * 0.91))

running = True
while running:
    dt_ms = clock.tick(60)                 # 지난 프레임 소요 시간(ms)
    dt = dt_ms / 1000.0                    # 초 단위로 변환
    screen.fill((255, 255, 255))           # 기본 배경 (메뉴에서 흰색)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ESC로 언제든 시작 화면으로 돌아가기 (원하면 빼도 됨)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            game_state = 'start'

        if game_state == 'start':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button_rect.collidepoint(event.pos):
                    game_state = 'play'
                    play_start_time = pygame.time.get_ticks()
                elif encyclopedia_button_rect.collidepoint(event.pos):
                    game_state = 'Encyclopedia'
                elif exit_button_rect.collidepoint(event.pos):
                    running = False
                    

            

        elif game_state == 'play':
            # ★ 캐릭터가 스스로 키 입력 이벤트를 처리
            character.handle_event(event)

        elif game_state == 'Encyclopedia':
            # 백 버튼을 따로 만들지 않았지만 ESC로 돌아갈 수 있어요.
            pass

    # ----------------- 상태별 그리기 -----------------
    if game_state == 'start':
        # 타이틀
        title_surf = title_font.render("spider game", True, (0, 0, 0))
        screen.blit(title_surf, (screen_width // 2 - title_surf.get_width() // 2, int(screen_height * 0.25)))

        # 백그라운드 대신 흰 배경 유지
        # 버튼(백그라운드와 대비되도록 검정 박스)
        pygame.draw.rect(screen, (0, 0, 0), encyclopedia_button_rect, border_radius=10)
        encyclopedia_text = font.render("Encyclopedia", True, (255, 255, 255))
        screen.blit(encyclopedia_text, encyclopedia_text.get_rect(center=encyclopedia_button_rect.center))

        pygame.draw.rect(screen, (0, 0, 0), start_button_rect, border_radius=10)
        start_game_text = font.render("Start Game", True, (255, 255, 255))
        screen.blit(start_game_text, start_game_text.get_rect(center=start_button_rect.center))

        pygame.draw.rect(screen, (0, 0, 0), exit_button_rect, border_radius=10)
        exit_game_text = font.render("exit", True, (255,255,255))
        screen.blit(exit_game_text, exit_game_text.get_rect(center=exit_button_rect.center))

    elif game_state == 'play':
        # 배경 그리기 (1회 로드한 이미지를 재사용)
        screen.blit(background, (0, 0))
        hpbar = HealthBar(character.max_hp)
        hpbar.draw(screen, character.hp, pos=(20,20))
        

        # ★ 캐릭터 업데이트/그리기
        character.update(dt, screen.get_rect())
        character.draw(screen)

        # "play now!" 1초 표시
        current_time = pygame.time.get_ticks()
        if play_start_time is not None and current_time - play_start_time < 1000:
            play_text = font.render("play now!", True, (0, 0, 0))
            screen.blit(play_text, (screen_width // 2 - play_text.get_width() // 2, int(screen_height * 0.85)))

    elif game_state == 'Encyclopedia':
        screen.blit(background, (0, 0))
        encyclopedia_msg = font.render('welcome to the show', True, (0, 0, 0))
        screen.blit(encyclopedia_msg, (screen_width // 2 - encyclopedia_msg.get_width() // 2, int(screen_height * 0.85)))

    pygame.display.update()

pygame.quit()