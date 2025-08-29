#임시 체력바 삽입
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
background = pygame.image.load(
    r"C:/Users/user/Downloads/jungle background-pixilart.png"
).convert()
background = pygame.transform.scale(background, (screen_width, screen_height))

# 캐릭터는 클래스로 관리
character_img_path = r"C:/Users/user\Downloads/gray spider-pixilart.png"
character_speed = 300  # px/s (초당 이동 픽셀수)
character = Character(
    image_path=character_img_path,
    start_pos=((screen_width // 2), (screen_height // 2)),
    speed=character_speed
)

# ----------------- ★ 체력바 클래스 추가 -----------------
class HealthBar:
    def __init__(self, max_hp, size=(240, 22), border=2):
        self.max_hp = max_hp
        self.size = size
        self.border = border

    def draw(self, surf, hp, pos=(20, 20)):
        x, y = pos
        w, h = self.size
        # 테두리
        pygame.draw.rect(surf, (0,0,0), (x- self.border, y- self.border, w+ self.border*2, h+ self.border*2), 0)
        # 배경
        pygame.draw.rect(surf, (200,200,200), (x, y, w, h))
        # 게이지
        ratio = max(0, min(1, hp / self.max_hp))
        fill_w = int(w * ratio)
        color = (255,0,0) if ratio > 0.4 else (255,165,0) if ratio > 0.2 else (220,50,50)
        pygame.draw.rect(surf, color, (x, y, fill_w, h))
        # 숫자
        txt = font.render(f"{int(hp)}/{self.max_hp}", True, (255,255,255))
        surf.blit(txt, (x + w + 10, y-2))

# ★ 캐릭터에 체력 속성이 있다고 가정 (없다면 Character 클래스에 self.max_hp, self.hp 추가 필요)
if not hasattr(character, "max_hp"):
    character.max_hp = 100
    character.hp = 100

# 체력바 생성
hpbar = HealthBar(character.max_hp)

# ----------------- 버튼/상태 -----------------
game_state = 'start'  # 'start', 'play', 'Encyclopedia'
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

        # ----------------- ★ 체력바 그리기 -----------------
        hpbar.draw(screen, character.hp, pos=(20,20))

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