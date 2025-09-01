import pygame
import math

class Character:
    def __init__(self, image_path, start_pos, speed=300):
        self.image_original = pygame.image.load(image_path).convert_alpha()
        self.image = self.image_original
        self.rect = self.image.get_rect(topleft=start_pos)
        self._x = float(self.rect.x)
        self._y = float(self.rect.y)
        self.speed = speed
        self._left = self._right = self._up = self._down = False
        self.angle = 0
        self.max_hp = 100
        self.hp = 100

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

    def update(self, dt, bounds_rect):
        vx = (-self.speed if self._left else 0) + (self.speed if self._right else 0)
        vy = (-self.speed if self._up else 0) + (self.speed if self._down else 0)
        self._x += vx * dt
        self._y += vy * dt
        self.rect.x = int(self._x)
        self.rect.y = int(self._y)
        before = self.rect.copy()
        self.rect.clamp_ip(bounds_rect)
        if self.rect.x != before.x: self._x = float(self.rect.x)
        if self.rect.y != before.y: self._y = float(self.rect.y)

        if vx != 0 or vy != 0:
            rad = math.atan2(vy, vx)
            deg = math.degrees(rad)
            self.angle = deg - 90
            self.image = pygame.transform.rotate(self.image_original, -self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def reset(self, pos):
        """캐릭터 상태를 초기화"""
        self.hp = self.max_hp
        self.rect.center = pos

        # 이동 좌표 변수 초기화 (없으면 무시 가능)
        if hasattr(self, "_x") and hasattr(self, "_y"):
            self._x, self._y = float(self.rect.x), float(self.rect.y)

        # 입력 상태 초기화
        self._left = False
        self._right = False
        self._up = False
        self._down = False
