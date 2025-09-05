import pygame
import math
import random

class enemy:
    def __init__(self, start_pos, size=(50, 50), speed=150, image=None, tile_size=64):
        self.tile_size = tile_size
        self.speed = speed

        self.rect = pygame.Rect(start_pos[0], start_pos[1], size[0], size[1])
        self.image = image
        if self.image:
            self.image = pygame.transform.scale(self.image, size)

        self.pos = pygame.math.Vector2(start_pos[0], start_pos[1])
        self.target_pos = pygame.math.Vector2(
            int(self.pos.x // self.tile_size) * self.tile_size,
            int(self.pos.y // self.tile_size) * self.tile_size,
        )
        self.moving = False
        self.move_dir = pygame.math.Vector2(0, 0)

    def update(self, dt, target_pos, bounds_rect):
        if not self.moving:
            dx = target_pos[0] - self.pos.x
            dy = target_pos[1] - self.pos.y

            move_x, move_y = 0, 0

            # 큰 방향 우선으로 이동 결정
            if abs(dx) > abs(dy):
                move_x = 1 if dx > 0 else -1
                move_y = 0
            elif abs(dy) > 0:
                move_y = 1 if dy > 0 else -1
                move_x = 0

            new_target = self.target_pos + pygame.math.Vector2(move_x * self.tile_size, move_y * self.tile_size)

            temp_rect = self.rect.copy()
            temp_rect.topleft = new_target
            if bounds_rect.contains(temp_rect):
                self.target_pos = new_target
                self.move_dir = pygame.math.Vector2(move_x, move_y)
                self.moving = True

        if self.moving:
            direction = self.target_pos - self.pos
            distance = direction.length()
            if distance != 0:
                direction.normalize_ip()
                move_dist = self.speed * dt
                if move_dist >= distance:
                    self.pos = self.target_pos
                    self.moving = False
                else:
                    self.pos += direction * move_dist

        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, self.rect)
        else:
            pygame.draw.rect(surface, (255, 0, 0), self.rect)

class enemymanager:
    def __init__(self, screen_width, screen_height, max_monsters=5,
                 spawn_interval=2.0, size=(50, 50), speed=150, image_paths=None, tile_size=64):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.max_monsters = max_monsters
        self.spawn_interval = spawn_interval
        self.size = size
        self.speed = speed
        self.tile_size = tile_size
        self.image_paths = image_paths or []
        self.images = []

        for path in self.image_paths:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, size)
            self.images.append(img)

        self.monsters = []
        self.spawn_timer = 0.0

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
        else:
            x = self.screen_width
            y = random.randint(0, self.screen_height - size[1])

        image = random.choice(self.images) if self.images else None
        return enemy((x, y), size=size, speed=self.speed, image=image, tile_size=self.tile_size)

    def update(self, dt, player_pos, bounds_rect):
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval and len(self.monsters) < self.max_monsters:
            self.spawn_timer = 0
            self.monsters.append(self.spawn_monster())

        for m in self.monsters:
            m.update(dt, player_pos, bounds_rect)

    def draw(self, surface):
        for m in self.monsters:
            m.draw(surface)

    def reset(self):
        self.monsters.clear()
        self.spawn_timer = 0.0
