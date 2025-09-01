import pygame
import math
import random

class Monster:
    def __init__(self, start_pos, size=(50, 50), speed=150, color=(255, 0, 0), image=None):
        """몬스터 초기화
        image: pygame.Surface 객체, None이면 빨간 블록
        """
        self.rect = pygame.Rect(start_pos[0], start_pos[1], size[0], size[1])
        self.speed = speed
        self.color = color
        self.image = image  # 이미지 Surface 객체

    def update(self, dt, target_pos):
        dx = target_pos[0] - self.rect.centerx
        dy = target_pos[1] - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance != 0:
            dx /= distance
            dy /= distance
            self.rect.x += dx * self.speed * dt
            self.rect.y += dy * self.speed * dt

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)


class MonsterManager:
    """여러 몬스터 관리 및 랜덤 이미지 스폰"""
    def __init__(self, screen_width, screen_height, max_monsters=5,
                 spawn_interval=2.0, size=(50,50), speed=150, image_paths=None):
        """
        image_paths: 이미지 경로 리스트, 랜덤 선택
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.max_monsters = max_monsters
        self.spawn_interval = spawn_interval
        self.size = size
        self.speed = speed
        self.image_paths = image_paths or []
        self.images = []

        # 이미지 로드
        for path in self.image_paths:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, size)
            self.images.append(img)

        self.monsters = []
        self.spawn_timer = 0.0

    def update(self, dt, player_pos):
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval and len(self.monsters) < self.max_monsters:
            self.spawn_timer = 0
            self.monsters.append(self.spawn_monster())

        for m in self.monsters:
            m.update(dt, player_pos)

    def draw(self, surface):
        for m in self.monsters:
            m.draw(surface)

    def spawn_monster(self):
        edge = random.choice(["top", "bottom", "left", "right"])
        size = self.size

        if edge == "top":
            x = random.randint(0, self.screen_width - size[0])
            y = -size[1]
        elif edge == "bottom":
            x = random.randint(0, self.screen_width - size[0])
            y = self.screen_height
        elif edge == "left":
            x = -size[0]
            y = random.randint(0, self.screen_height - size[1])
        else:  # right
            x = self.screen_width
            y = random.randint(0, self.screen_height - size[1])

        # 이미지 랜덤 선택
        image = random.choice(self.images) if self.images else None

        return Monster((x, y), size=size, speed=self.speed, image=image)

    def reset(self):
        self.monsters.clear()
        self.spawn_timer = 0