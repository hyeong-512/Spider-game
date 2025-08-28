[import pygame.py](https://github.com/user-attachments/files/22028017/import.pygame.py)
import pygame

pygame.init()  # 초기화 설정

# 화면 크기 설정
W, H = 800, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("거미게임")  # 게임 제목 설정

clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)  # 폰트 객체 생성

# 상태 변수
game_state = 'start'  # 'start' or 'play'
play_start_time = None # 화면 전환 이후 시간 측정 변수

# 버튼 설정
start_button_rect = pygame.Rect(500, 450, 200, 80)
button_rect = pygame.Rect(100, 450, 200, 80)

# 메인 루프
running = True
while running:
    screen.fill((255, 255, 255))  # 배경색 채우기 (흰색)

    for event in pygame.event.get(): #이벤트 루프, 화면 종료기
        if event.type == pygame.QUIT:
            running = False

        # 마우스 클릭 시 처리
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 왼쪽 클릭
            if start_button_rect.collidepoint(event.pos):  # 버튼 클릭 시
                game_state = 'play'
                play_start_time = pygame.time.get_ticks()  # 현재 시간 기록
            elif button_rect.collidepoint(event.pos):
                game_state = 'Encyclopedia'

    if game_state == 'start':
        
        start_font = pygame.font.SysFont("malgungothic", 80) 
        start_text = start_font.render("spider game", True, (0, 0, 0))
        screen.blit(start_text, (W//2 - start_text.get_width()//2, 150))  # 화면 위쪽 가운데쯤


        # button_rect 버튼 그리기
        pygame.draw.rect(screen, (0, 0, 0), button_rect, border_radius=10)
        text = font.render("Encyclopedia", True, (255, 255, 255)) #'start Game', True, 색상(rgb코드)
        screen.blit(text, text.get_rect(center=button_rect.center))

        # start button_rect 버튼 그리기
        pygame.draw.rect(screen, (0, 0, 0), start_button_rect, border_radius=10)
        text = font.render("Start Game", True, (255, 255, 255)) #'start Game', True, 색상(rgb코드)
        screen.blit(text, text.get_rect(center=start_button_rect.center))

    elif game_state == 'play':
        # 게임 시작 화면 (예시로 텍스트 표시)
        background = pygame.image.load("C:/Users/user/OneDrive/바탕 화면/python Workspace/임시 배경화면.png") #링크 삽입하여 배경 설정
        screen.blit(background, (0,0))
        current_time = pygame.time.get_ticks()
        if play_start_time is not None and current_time - play_start_time < 1000: #1초 (=1000)
            play_text = font.render("play now!", True, (0, 0, 0))
            screen.blit(play_text, (350, 500))
    
    elif game_state == 'Encyclopedia':
        background = pygame.image.load("C:/Users/user/OneDrive/바탕 화면/python Workspace/임시 배경화면.png") #링크 삽입하여 배경 설정
        screen.blit(background, (0,0))
        Encyclopedia_text = font.render('welcome to the show', True, (0,0,0))
        screen.blit(Encyclopedia_text, (270, 500))

        

    pygame.display.update()
    clock.tick(60)  # FPS 60

pygame.quit()
