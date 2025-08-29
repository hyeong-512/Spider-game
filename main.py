import pygame
from scripts.character import Character
from scripts.healthbar import HealthBar   # ★ 새로 분리된 체력바 불러오기

pygame.init()

# ----------------- 화면/글꼴/시계 기본 설정 -----------------
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = pygame.display.get_surface().get_size()
pygame.display.set_caption("거미게임")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)
title_font = pygame.font.SysFont("malgungothic", 80)

# ----------------- 이미지 로드 -----------------
background = pygame.image.load(
    r"C:/Users/user/Downloads/jungle background-pixilart.png"
).convert()
background = pygame.transform.scale(background, (screen_width, screen_height))

# 캐릭터
character_img_path = r"C:/Users/user/Downloads/gray spider-pixilart.png"
character_speed = 300
character = Character(
    image_path=character_img_path,
    start_pos=((screen_width // 2), (screen_height // 2)),
    speed=character_speed
)

# ★ 캐릭터에 체력 속성 없으면 추가
if not hasattr(character, "max_hp"):
    character.max_hp = 100
    character.hp = 100

# ★ 체력바 생성 (분리된 클래스 사용)
hpbar = HealthBar(character.max_hp, font=font, smooth_speed=100)  # smooth_speed: 체력 애니메이션 속도

# ----------------- 버튼/상태 -----------------
game_state = 'start'
play_start_time = None

start_button_rect = pygame.Rect(0, 0, 240, 80)
start_button_rect.center = (screen_width // 2, int(screen_height * 0.65))

encyclopedia_button_rect = pygame.Rect(0, 0, 240, 80)
encyclopedia_button_rect.center = (screen_width // 2, int(screen_height * 0.78))

exit_button_rect = pygame.Rect(0, 0, 240, 80)
exit_button_rect.center = (screen_width // 2 , int(screen_height * 0.91))


running = True
while running:
    dt_ms = clock.tick(60)
    dt = dt_ms / 1000.0
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
            character.handle_event(event)
            # 예시: 스페이스 누르면 데미지
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    character.hp -= 15
                    if character.hp < 0:
                        character.hp = 0

        elif game_state == 'Encyclopedia':
            pass

    # ----------------- 상태별 그리기 -----------------
    if game_state == 'start':
        title_surf = title_font.render("spider game", True, (0, 0, 0))
        screen.blit(title_surf, (screen_width // 2 - title_surf.get_width() // 2, int(screen_height * 0.25)))

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
        screen.blit(background, (0, 0))

        # ----------------- ★ 체력바 그리기 (부드럽게 감소) -----------------
        hpbar.update(dt, character.hp)  # 실제 hp를 기반으로 천천히 줄어듦
        hpbar.draw(screen, pos=(20,20))

        character.update(dt, screen.get_rect())
        character.draw(screen)

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
