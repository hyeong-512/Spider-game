import pygame

class Character:
    def __init__(self, image_path: str, start_pos: tuple[int, int], speed: float = 300.0):
        """
        image_path: 캐릭터 이미지 경로
        start_pos : (x, y) 시작 위치 (화면 좌상단 기준)
        speed     : 초당 픽셀(px/s)
        """
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = start_pos

        # 부드러운 이동을 위해 내부적으로 실수 좌표를 유지
        self._x = float(self.rect.x)
        self._y = float(self.rect.y)

        self.speed = float(speed)

        # 입력 상태 플래그
        self._left = False
        self._right = False
        self._up = False
        self._down = False

    # ----------------- 입력 처리 -----------------
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self._left = True
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self._right = True
            elif event.key in (pygame.K_UP, pygame.K_w):
                self._up = True
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self._down = True

        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self._left = False
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self._right = False
            elif event.key in (pygame.K_UP, pygame.K_w):
                self._up = False
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self._down = False

    # ----------------- 위치 업데이트 -----------------
    def update(self, dt: float, bounds_rect: pygame.Rect):
        """
        dt: 경과 시간(초)
        bounds_rect: 캐릭터가 벗어나지 않도록 제한할 화면 경계 (보통 screen.get_rect())
        """
        # 현재 입력 상태로 속도 벡터 계산
        vx = (-self.speed if self._left else 0.0) + (self.speed if self._right else 0.0)
        vy = (-self.speed if self._up else 0.0) + (self.speed if self._down else 0.0)

        # 대각선 이동 속도 보정이 필요하면 여기서 정규화 가능(선택)
        # 예: if vx != 0 and vy != 0: factor = 1 / 1.4142; vx *= factor; vy *= factor

        # 실수 좌표로 이동
        self._x += vx * dt
        self._y += vy * dt

        # rect에 반영
        self.rect.x = int(self._x)
        self.rect.y = int(self._y)

        # 화면 밖으로 나가지 않도록 clamp
        before = self.rect.copy()
        self.rect.clamp_ip(bounds_rect)

        # clamp로 잘렸다면 내부 좌표도 동기화
        if self.rect.x != before.x:
            self._x = float(self.rect.x)
        if self.rect.y != before.y:
            self._y = float(self.rect.y)

    # ----------------- 그리기 -----------------
    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)