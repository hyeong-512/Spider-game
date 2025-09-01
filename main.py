import pygame
import random
import math
from scripts.character import Character
from scripts.ui import HealthBar, cobwebBar, Timer
from scripts.monster import MonsterManager

pygame.init()

# ----------------- 화면/글꼴/시계 -----------------
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
pygame.display.set_caption("Spider Game")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)
title_font = pygame.font.SysFont("malgungothic", 80)
background = pygame.image.load("C:/Users/user/Downloads/jungle background-pixilart.png").convert()
background = pygame.transform.scale(background, (screen_width, screen_height))

# ----------------- 캐릭터 / 체력바 -----------------
character = Character(
    "C:/Users/user/Downloads/gray spider-pixilart.png",
    (screen_width//2, screen_height//2)
)
character.max_cobweb = 100
character.cobweb = character.max_cobweb

hpbar = HealthBar(character.max_hp, font=font, smooth_speed=100)
cobar = cobwebBar(character.max_cobweb, font=font, smooth_speed=100)
cobar.color = (255,255,255)

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

# ----------------- Q 메시지 변수 -----------------
q_message_timer = 0
q_message_duration = 2.0

# ----------------- 타이머 생성 -----------------
timer = Timer(duration=30, font=font, pos=(screen_width//2, 50), radius=40, color=(255,255,0), bg_color=(50,50,50), thickness=3)
"""duration: 총 시간 (초), font: 글자 폰트, pos: 원 중심 위치 (x,y), radius: 원 반지름, color: 진행 호 색, bg_color: 배경 원 색, thickness: 호 두께"""

# ----------------- 메인 루프 -----------------
running = True
while running:
    dt = clock.tick(60)/1000.0
    screen.fill((255,255,255))

    # ----------------- 이벤트 처리 -----------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_state == 'play':
                    game_state = 'pause'
                elif game_state == 'pause':
                    game_state = 'play'
                else:
                    game_state = 'start'

            # Q키 사용
            if event.key == pygame.K_q and game_state == 'play':
                if character.cobweb >= 10:
                    character.cobweb -= 10
                    # Q키 효과 실행
                else:
                    q_message_timer = q_message_duration
                    print("거미줄이 부족하여 Q를 사용할 수 없습니다!")

        if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            if game_state == 'play':
                character.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game_state == 'start':
                if start_button_rect.collidepoint(event.pos):
                    game_state = 'play'
                    character.reset((screen_width//2, screen_height//2))
                    character.cobweb = character.max_cobweb
                    monster_manager.reset()
                    timer.start()
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
                    character.cobweb = character.max_cobweb
                    monster_manager.reset()
                    timer.reset()
                    timer.start()
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
        screen.blit(title_surf, (screen_width//2 - title_surf.get_width()//2, int(screen_height*0.25)))

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

        # 체력/거미줄 회복
        character.hp += 3*dt
        if character.hp > character.max_hp: character.hp = character.max_hp
        character.cobweb += 2*dt
        if character.cobweb > character.max_cobweb: character.cobweb = character.max_cobweb

        hpbar.update(dt, character.hp)
        hpbar.draw(screen, pos=(20, screen_height-100))
        cobar.update(dt, character.cobweb)
        cobar.draw(screen, pos=(20, screen_height-50))

        # Q 부족 메시지
        if q_message_timer > 0:
            msg = font.render("I can't use Q because I don't have enough spider webs!", True, (230,167,161))
            msg_x = screen_width//2 - msg.get_width()//2
            msg_y = screen_height - 60  # 하단에서 30px 위
            screen.blit(msg, (msg_x, msg_y))
            q_message_timer -= dt

        # 타이머
        timer.update(dt)
        timer.draw(screen) 

        # 충돌 체크
        for m in monster_manager.monsters:
            if character.rect.colliderect(m.rect):
                character.hp -= 100*dt
                if character.hp < 0: character.hp = 0

        if character.hp <= 0 or timer.remaining <= 0:
            game_state = 'end'

    elif game_state == 'pause':
        screen.blit(background, (0,0))
        character.draw(screen)
        monster_manager.draw(screen)
        hpbar.draw(screen, pos=(20, screen_height-100))
        cobar.draw(screen, pos=(20, screen_height-50))

        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(150)
        overlay.fill((0,0,0))
        screen.blit(overlay, (0,0))

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
