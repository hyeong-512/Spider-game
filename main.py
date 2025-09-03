# main.py
import pygame
from scripts.character import Character
from scripts.ui import HealthBar, cobwebBar, Timer
from scripts.enemy import enemyManager

pygame.init()

# ----------------- 화면/글꼴/시계 -----------------
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
pygame.display.set_caption("생존은 꺼미다")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)
btn_font = pygame.font.Font(None, 60)
title_font = pygame.font.SysFont("malgungothic", 50)

# ----------------- 배경 이미지 -----------------
background = pygame.image.load("C:/Users/user/OneDrive/바탕 화면/python Workspace/game_images/jungle_background image.png").convert()
background = pygame.transform.scale(background, (screen_width, screen_height))
background2 = pygame.image.load("C:/Users/user/OneDrive/바탕 화면/python Workspace/game_images/jungle_backgruound image2.png").convert()
background2 = pygame.transform.scale(background2, (screen_width, screen_height))
image = pygame.image.load("C:/Users/user/OneDrive/바탕 화면/python Workspace/game_images/skill&hp_player.png")
image = pygame.transform.scale(image, (400, 400))
image_x, image_y = 50, 700


# ----------------- 캐릭터 / 체력바 -----------------
character = Character(
    [
        "C:/Users/user/OneDrive/바탕 화면/python Workspace/game_images/gray spider_player.png",   # 가만히 있는 이미지
        "C:/Users/user/OneDrive/바탕 화면/python Workspace/game_images/gray spider(left)_player.png",  # 걷기 1
        "C:/Users/user/OneDrive/바탕 화면/python Workspace/game_images/gray spider(right)_player.png"   # 걷기 2
    ],
    (screen_width//2, screen_height//2),
    speed=300,
    anim_interval=0.2,
    size=(80, 80)
)

if not hasattr(character, "max_cobweb"):
    character.max_cobweb = 100
if not hasattr(character, "cobweb"):
    character.cobweb = character.max_cobweb

hpbar = HealthBar(character.max_hp, font=font, smooth_speed=100)
cobar = cobwebBar(character.max_cobweb, font=font, smooth_speed=100)
cobar.color = (255,255,255)

# ----------------- 타이머 -----------------
timer = Timer(duration=10, font=font, pos=(screen_width//2, 30))
timer2 = Timer(duration=10, font=font, pos=(screen_width//2, 30))
timer.start()

# ----------------- 몬스터 매니저 -----------------
monster_images = [
    "C:/Users/user/OneDrive/바탕 화면/python Workspace/game_images/jungle_background image.png",
    "C:/Users/user/OneDrive/바탕 화면/python Workspace/game_images/gray spider_player.png"
]
monster_manager = enemyManager(screen_width, screen_height, 5, 2.0, (50,50), 150, monster_images)
monster_manager2 = enemyManager(screen_width, screen_height, 8, 1.5, (60,60), 180, monster_images)

# ----------------- 버튼 생성 -----------------
def make_button(center_x, center_y, w=240, h=80):
    rect = pygame.Rect(0,0,w,h)
    rect.center = (center_x, center_y)
    return rect

start_button_rect = make_button(screen_width//2, int(screen_height*0.65))
exit_button_rect = make_button(screen_width//2, int(screen_height*0.91))
encyclopedia_button_rect = make_button(screen_width//2, int(screen_height*0.78))
replay_button_rect = make_button(int(screen_width*0.6), int(screen_height*0.91))
overstart_button_rect = make_button(int(screen_width*0.4), int(screen_height*0.91))
enstart_button_rect = make_button(int(screen_width*0.9), int(screen_height*0.91))
pause_button_rect = make_button(screen_width//2, screen_height//2)
next_stage_button_rect = make_button(screen_width//2, int(screen_height//2 + 70), w=300, h=100)
clearhome_button_rect = make_button(screen_width//2, int(screen_height*0.78))

# ----------------- 상태 (필수변수들)-----------------
game_state = 'start'
previous_stage = 'play'
q_message_timer = 0.0
q_message_duration = 2.0
blink_timer = 0.0
blink_interval = 0.5  # 0.5초마다 깜빡임
show_text = True

# ----------------- 헬퍼 함수 -----------------
def center_player_and_clear_movement(player):
    player.rect.center = (screen_width//2, screen_height//2)
    if hasattr(player, "_x") and hasattr(player, "_y"):
        player._x, player._y = float(player.rect.x), float(player.rect.y)
    if hasattr(player, "movement"):
        player.movement = [0,0]
    for attr in ("_left","_right","_up","_down"):
        if hasattr(player, attr):
            setattr(player, attr, False)

# ----------------- 메인 루프 -----------------
running = True
while running:
    dt = clock.tick(60)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ----------------- 키보드 입력 -----------------
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_state in ['play','play2']:
                    previous_stage = game_state
                    game_state = 'pause'
                elif game_state == 'pause':
                    game_state = previous_stage
                else:
                    game_state = 'start'

            if event.key == pygame.K_q and game_state in ['play','play2']:
                if character.cobweb >= 10:
                    character.cobweb -= 10
                else:
                    q_message_timer = q_message_duration
                    print("거미줄 부족!")

        if event.type in [pygame.KEYDOWN, pygame.KEYUP] and game_state in ['play','play2']:
            character.handle_event(event)

        # ----------------- 마우스 입력 -----------------
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if game_state == 'start':
                if start_button_rect.collidepoint(mouse_pos):
                    game_state = 'play'
                    center_player_and_clear_movement(character)
                    character.cobweb = character.max_cobweb
                    monster_manager.reset()
                    timer.reset()
                    timer.start()
                elif encyclopedia_button_rect.collidepoint(mouse_pos):
                    game_state = 'encyclopedia'
                elif exit_button_rect.collidepoint(mouse_pos):
                    running = False

            elif game_state == 'pause':
                if pause_button_rect.collidepoint(mouse_pos):
                    game_state = 'end'

            elif game_state == 'stage_transition':
                if next_stage_button_rect.collidepoint(mouse_pos):
                    game_state = 'play2'
                    center_player_and_clear_movement(character)
                    monster_manager2.reset()
                    timer2.reset()
                    timer2.start()

            elif game_state == 'end':
                if replay_button_rect.collidepoint(mouse_pos):
                    game_state = 'play'
                    center_player_and_clear_movement(character)
                    character.hp = character.max_hp
                    character.cobweb = character.max_cobweb
                    monster_manager.reset()
                    timer.reset()
                    timer.start()
                elif overstart_button_rect.collidepoint(mouse_pos):
                    game_state = 'start'

            elif game_state == 'encyclopedia':
                if enstart_button_rect.collidepoint(mouse_pos):
                    game_state = 'start'
            elif game_state == 'clear':
                if clearhome_button_rect.collidepoint(mouse_pos):
                    game_state = 'start'

    # ----------------- 상태 업데이트 -----------------
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
        screen.blit(image, (image_x, image_y))

        # 체력/거미줄 회복
        character.hp = min(character.hp + 3*dt, character.max_hp)
        character.cobweb = min(character.cobweb + 2*dt, character.max_cobweb)

        hpbar.update(dt, character.hp)
        hpbar.draw(screen, pos=(194, screen_height-78), size=(240,12))
        cobar.update(dt, character.cobweb)
        cobar.draw(screen, pos=(194, screen_height-54), size=(240,12))

        if q_message_timer > 0:
            msg = font.render("I can't use Q because I don't have enough spider webs!", True, (230,167,161))
            screen.blit(msg, (screen_width//2 - msg.get_width()//2, screen_height-30 - msg.get_height()))
            q_message_timer -= dt

        timer.update(dt)
        timer.draw(screen)

        if timer.remaining <= 0:
            game_state = 'stage_transition'
            center_player_and_clear_movement(character)
            monster_manager2.reset()
            timer2.reset()

        for m in monster_manager.monsters:
            if character.rect.colliderect(m.rect):
                character.hp -= 100*dt
        if character.hp <= 0:
            game_state = 'end'

    elif game_state == 'stage_transition':
        screen.blit(background, (0,0))
        character.draw(screen)
        monster_manager.draw(screen)
        screen.blit(image, (image_x, image_y))
        hpbar.draw(screen, pos=(194, screen_height-78), size=(240,12))
        cobar.draw(screen, pos=(194, screen_height-54), size=(240,12))
        timer.draw(screen)
        
        

        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(150)
        overlay.fill((0,0,0))
        screen.blit(overlay, (0,0))

        box_w, box_h = 600, 300
        box_rect = pygame.Rect(0,0,box_w, box_h)
        box_rect.center = (screen_width//2, screen_height//2)
        pygame.draw.rect(screen, (255,255,255), box_rect, border_radius=12)

        title_text = title_font.render("Stage 1 Complete", True, (0,0,0))
        screen.blit(title_text, (box_rect.centerx - title_text.get_width()//2, box_rect.top + 20))

        info = font.render("Ready for Stage 2?", True, (0,0,0))
        screen.blit(info, (box_rect.centerx - info.get_width()//2, box_rect.top + 120))

        pygame.draw.rect(screen, (0,0,0), next_stage_button_rect, border_radius=12)
        btn_text = btn_font.render("Go to Stage 2", True, (255,255,255))
        screen.blit(btn_text, btn_text.get_rect(center=next_stage_button_rect.center))

    elif game_state == 'play2':
        screen.blit(background2, (0,0))
        character.update(dt, screen.get_rect())
        character.draw(screen)
        monster_manager2.update(dt, character.rect.center)
        monster_manager2.draw(screen)

        character.hp = min(character.hp + 3*dt, character.max_hp)
        character.cobweb = min(character.cobweb + 2*dt, character.max_cobweb)

        screen.blit(image, (image_x, image_y))
        hpbar.update(dt, character.hp)
        hpbar.draw(screen, pos=(194, screen_height-78), size=(240,12))
        cobar.update(dt, character.cobweb)
        cobar.draw(screen, pos=(194, screen_height-54), size=(240,12))
        

        if q_message_timer > 0:
            msg = font.render("I can't use Q because I don't have enough spider webs!", True, (230,167,161))
            screen.blit(msg, (screen_width//2 - msg.get_width()//2, screen_height-30 - msg.get_height()))
            q_message_timer -= dt

        timer2.update(dt)
        timer2.draw(screen)

        for m in monster_manager2.monsters:
            if character.rect.colliderect(m.rect):
                character.hp -= 100*dt
        if character.hp <= 0:
            game_state = 'end'
        elif timer2.remaining <= 0:
            game_state = 'clear'
            


    elif game_state == 'pause':
        # 일시정지 화면
        if previous_stage == 'play2':
            screen.blit(background2, (0,0))
            monster_manager2.draw(screen)
        else:
            screen.blit(background, (0,0))
            monster_manager.draw(screen)
        character.draw(screen)
        screen.blit(image, (image_x, image_y))
        hpbar.draw(screen, pos=(194, screen_height-78), size=(240,12))
        cobar.draw(screen, pos=(194, screen_height-54), size=(240,12))

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

        # Replay 버튼
        pygame.draw.rect(screen, (255,255,255), replay_button_rect, border_radius=10)
        replay_text = font.render("Replay", True, (0,0,0))
        screen.blit(replay_text, replay_text.get_rect(center=replay_button_rect.center))

        # Home 버튼
        pygame.draw.rect(screen, (255,255,255), overstart_button_rect, border_radius=10)
        home_text = font.render("Home", True, (0,0,0))
        screen.blit(home_text, home_text.get_rect(center=overstart_button_rect.center))
    
    elif game_state == 'clear':
        screen.fill((255,255,255))
        
        # 깜빡임 타이머 업데이트
        blink_timer += dt
        if blink_timer >= blink_interval:
            blink_timer = 0
            show_text = not show_text  # 토글

        # 글자 크게 만들기
        big_font = pygame.font.SysFont("malgungothic", 120)
        if show_text:
            clear_surf = big_font.render("CLEAR!", True, (0,0,255))
            screen.blit(clear_surf, (screen_width//2 - clear_surf.get_width()//2,
                                    screen_height//2 - clear_surf.get_height()//2))

        # Home 버튼
        pygame.draw.rect(screen, (0,0,0), clearhome_button_rect, border_radius=10)
        clearhome_text = font.render("Home", True, (255,255,255))
        screen.blit(clearhome_text, clearhome_text.get_rect(center=clearhome_button_rect.center))

    # 화면 업데이트
    pygame.display.update()

pygame.quit()
