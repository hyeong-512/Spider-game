import pygame
import random
import math
from scripts.임시캐릭터루프 import Character
from scripts.임시체력바루프 import HealthBar
from scripts.임시몬스터루프 import MonsterManager

pygame.init()

# ----------------- 화면/글꼴/시계 -----------------
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
pygame.display.set_caption("spider game")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)
title_font = pygame.font.SysFont("malgungothic", 80)
background = pygame.image.load("C:/Users/user/Downloads/jungle background-pixilart.png").convert()
background = pygame.transform.scale(background, (screen_width, screen_height))

# ----------------- 캐릭터 / 체력바 -----------------
character = Character("C:/Users/user/Downloads/gray spider-pixilart.png",
                      (screen_width//2, screen_height//2))
hpbar = HealthBar(character.max_hp, font=font, smooth_speed=100)

# ----------------- 몬스터 매니저 -----------------
monster_images = [
    "C:/Users/user/Downloads/gray spider-pixilart.png",
    "C:/Users/user/Downloads/jungle background-pixilart.png"
]
monster_manager = MonsterManager(
    screen_width, screen_height,
    max_monsters=5,
    spawn_interval=2.0,
    size=(50,50),
    speed=150,
    image_paths=monster_images
)

# ----------------- 버튼 -----------------
def make_button(center_x, center_y, w=240, h=80):
    rect = pygame.Rect(0,0,w,h)
    rect.center = (center_x, center_y)
    return rect

start_button_rect = make_button(screen_width//2, int(screen_height*0.65))
exit_button_rect = make_button(screen_width//2, int(screen_height*0.91))
encyclopedia_button_rect = make_button(screen_width//2, int(screen_height*0.78))
replay_button_rect = make_button(int(screen_width*0.6), int(screen_height*0.91))
enstart_button_rect = make_button(int(screen_width*0.9), int(screen_height*0.91))
overstart_button_rect = make_button(int(screen_width*0.4), int(screen_height*0.91))
pause_button_rect = make_button(screen_width//2, screen_height//2)

game_state = 'start'

running = True
while running:
    dt = clock.tick(60)/1000.0
    screen.fill((255,255,255))

    # ----------------- 이벤트 처리 -----------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ESC 처리
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if game_state == 'play':
                game_state = 'pause'
            elif game_state == 'pause':
                game_state = 'play'
            else:
                game_state = 'start'

        # 플레이 중 키 이벤트 처리
        if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            if game_state == 'play':
                character.handle_event(event)

        # 마우스 클릭 처리
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game_state == 'start':
                if start_button_rect.collidepoint(event.pos):
                    game_state = 'play'
                    character.reset((screen_width//2, screen_height//2))
                    monster_manager.reset()
                elif encyclopedia_button_rect.collidepoint(event.pos):
                    game_state = 'encyclopedia'
                elif exit_button_rect.collidepoint(event.pos):
                    running = False

            elif game_state == 'pause':
                if pause_button_rect.collidepoint(event.pos):
                    game_state = 'end'

            elif game_state == 'end':
                if replay_button_rect.collidepoint(event.pos):
                    character.reset((screen_width//2, screen_height//2))
                    monster_manager.reset()
                    game_state = 'play'
                elif overstart_button_rect.collidepoint(event.pos):
                    game_state = 'start'

            elif game_state == 'encyclopedia':
                if enstart_button_rect.collidepoint(event.pos):
                    game_state = 'start'

    # ----------------- 상태별 그리기 -----------------
    if game_state == 'start':
        screen.fill((255,255,255))
        title_surf = title_font.render("Spider Game", True, (0,0,0))
        screen.blit(title_surf, (screen_width//2 - title_surf.get_width()//2,
                                  int(screen_height*0.25)))

        pygame.draw.rect(screen, (0,0,0), start_button_rect, border_radius=10)
        screen.blit(font.render("Start Game", True, (255,255,255)),
                    font.render("Start Game", True, (255,255,255)).get_rect(center=start_button_rect.center))

        pygame.draw.rect(screen, (0,0,0), encyclopedia_button_rect, border_radius=10)
        screen.blit(font.render("Encyclopedia", True, (255,255,255)),
                    font.render("Encyclopedia", True, (255,255,255)).get_rect(center=encyclopedia_button_rect.center))

        pygame.draw.rect(screen, (0,0,0), exit_button_rect, border_radius=10)
        screen.blit(font.render("Exit", True, (255,255,255)),
                    font.render("Exit", True, (255,255,255)).get_rect(center=exit_button_rect.center))

    elif game_state == 'play':
        screen.blit(background, (0,0))
        character.update(dt, screen.get_rect())
        character.draw(screen)
        monster_manager.update(dt, character.rect.center)
        monster_manager.draw(screen)
        hpbar.update(dt, character.hp)
        hpbar.draw(screen, pos=(20,20))

        # 충돌 체크
        for m in monster_manager.monsters:
            if character.rect.colliderect(m.rect):
                character.hp -= 100*dt
                if character.hp < 0:
                    character.hp = 0

        if character.hp <= 0:
            game_state = 'end'

    elif game_state == 'pause':
        # 기존 플레이 화면 유지
        screen.blit(background, (0,0))
        character.draw(screen)
        monster_manager.draw(screen)
        hpbar.draw(screen, pos=(20,20))

        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(150)
        overlay.fill((0,0,0))
        screen.blit(overlay, (0,0))

        # Pause 버튼
        pygame.draw.rect(screen, (255,255,255), pause_button_rect, border_radius=10)
        text = font.render("Game Over?", True, (0,0,0))
        screen.blit(text, text.get_rect(center=pause_button_rect.center))

    elif game_state == 'encyclopedia':
        screen.blit(background, (0,0))

        pygame.draw.rect(screen, (255,255,255), enstart_button_rect, border_radius=10)
        screen.blit(font.render("Home", True, (0,0,0)),
                    font.render("Home", True, (0,0,0)).get_rect(center=enstart_button_rect.center))

    elif game_state == 'end':
        screen.fill((0,0,0))
        end_surf = title_font.render("GAME OVER", True, (255,0,0))
        screen.blit(end_surf, (screen_width//2 - end_surf.get_width()//2, screen_height//2 - 50))

        pygame.draw.rect(screen, (255,255,255), replay_button_rect, border_radius=10)
        screen.blit(font.render("Replay", True, (0,0,0)),
                    font.render("Replay", True, (0,0,0)).get_rect(center=replay_button_rect.center))

        pygame.draw.rect(screen, (255,255,255), overstart_button_rect, border_radius=10)
        screen.blit(font.render("Home", True, (0,0,0)),
                    font.render("Home", True, (0,0,0)).get_rect(center=overstart_button_rect.center))

    pygame.display.update()

pygame.quit()

