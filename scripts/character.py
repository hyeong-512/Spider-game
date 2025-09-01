import pygame
import math

class Character:
    def __init__(self, image_path, start_pos, speed=300):
        # 이미지
        self.image_original = pygame.image.load(image_path).convert_alpha()
        self.image = self.image_original
        self.rect = self.image.get_rect(topleft=start_pos)

        # 위치 (float으로 부드럽게 이동)
        self._x = float(self.rect.x)
        self._y = float(self.rect.y)

        # 속도 및 이동 키 상태
        self.speed = speed
        self._left = self._right = self._up = self._down = False

        # 회전 각도
        self.angle = 0

        # 체력
        self.max_hp = 100
        self.hp = 100

        # 거미줄
        self.max_cobweb = 100
        self.cobweb = self.max_cobweb

    # 키 이벤트 처리
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a): self._left = True
            elif event.key in (pygame.K_RIGHT, pygame.K_d): self._right = True
            elif event.key in (pygame.K_UP, pygame.K_w): self._up = True
            elif event.key in (pygame.K_DOWN, pygame.K_s): self._down = True
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_a): self._left = False
            elif event.key in (pygame.K_RIGHT, pygame.K_d): self._right = False
            elif event.key in (pygame.K_UP, pygame.K_w): self._up = False
            elif event.key in (pygame.K_DOWN, pygame.K_s): self._down = False

    # 위치 업데이트
    def update(self, dt, bounds_rect):
        vx = (-self.speed if self._left else 0) + (self.speed if self._right else 0)
        vy = (-self.speed if self._up else 0) + (self.speed if self._down else 0)
        self._x += vx * dt
        self._y += vy * dt

        self.rect.x = int(self._x)
        self.rect.y = int(self._y)

        # 화면 밖 이동 방지
        before = self.rect.copy()
        self.rect.clamp_ip(bounds_rect)
        if self.rect.x != before.x: self._x = float(self.rect.x)
        if self.rect.y != before.y: self._y = float(self.rect.y)

        # 이동 방향으로 회전
        if vx != 0 or vy != 0:
            rad = math.atan2(vy, vx)
            deg = math.degrees(rad)
            self.angle = deg - 90
            self.image = pygame.transform.rotate(self.image_original, -self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)

    # 그리기
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    # 초기화
    def reset(self, pos):
        self.hp = self.max_hp
        self.cobweb = self.max_cobweb
        self.rect.center = pos
        self._x, self._y = float(self.rect.x), float(self.rect.y)
        self._left = self._right = self._up = self._down = False
