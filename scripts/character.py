import pygame
import math

class Character:
    def __init__(self, image_paths, start_pos, anim_interval=0.1, size=(80, 80), tile_size=64, speed=300):
        self.tile_size = tile_size
        self.speed = speed

        self.idle_image = pygame.image.load(image_paths[0]).convert_alpha()
        self.idle_image = pygame.transform.scale(self.idle_image, size)

        self.walk_frames = []
        for path in image_paths[1:]:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, size)
            self.walk_frames.append(img)

        self.image_original = self.idle_image
        self.image = self.image_original
        self.rect = self.image.get_rect(topleft=start_pos)

        self.pos = pygame.math.Vector2(start_pos[0], start_pos[1])
        # 위치 타일 좌표로 스냅
        self.target_pos = pygame.math.Vector2(
            int(self.pos.x // self.tile_size) * self.tile_size,
            int(self.pos.y // self.tile_size) * self.tile_size,
        )

        self.key_left = False
        self.key_right = False
        self.key_up = False
        self.key_down = False

        self.move_dir = pygame.math.Vector2(0, 0)
        self.moving = False

        self.anim_interval = anim_interval
        self.anim_timer = 0.0
        self.anim_index = 0

        self.angle = 0

        self.max_hp = 100
        self.hp = self.max_hp
        self.hit_cooldown = 1.0
        self.hit_timer = 0.0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.key_left = True
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.key_right = True
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.key_up = True
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.key_down = True

        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.key_left = False
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.key_right = False
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.key_up = False
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.key_down = False

        move_x = 0
        move_y = 0
        if self.key_left and not self.key_right:
            move_x = -1
        elif self.key_right and not self.key_left:
            move_x = 1
        if self.key_up and not self.key_down:
            move_y = -1
        elif self.key_down and not self.key_up:
            move_y = 1
        self.move_dir = pygame.math.Vector2(move_x, move_y)

    def update(self, dt, bounds_rect):
        if self.hit_timer > 0:
            self.hit_timer -= dt

        if self.move_dir.x != 0 and self.move_dir.y != 0:
            self.move_dir.y = 0

        if not self.moving and (self.move_dir.x != 0 or self.move_dir.y != 0):
            new_target = self.target_pos + pygame.math.Vector2(self.move_dir.x * self.tile_size,
                                                              self.move_dir.y * self.tile_size)
            temp_rect = self.rect.copy()
            temp_rect.topleft = new_target
            if bounds_rect.contains(temp_rect):
                self.target_pos = new_target
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

        if self.move_dir.length_squared() > 0:
            rad = math.atan2(self.move_dir.y, self.move_dir.x)
            self.angle = math.degrees(rad) - 90

        if self.moving:
            self.anim_timer += dt
            if self.anim_timer >= self.anim_interval:
                self.anim_timer = 0
                self.anim_index = (self.anim_index + 1) % len(self.walk_frames)
            self.image_original = self.walk_frames[self.anim_index]
        else:
            self.image_original = self.idle_image
            self.anim_index = 0
            self.anim_timer = 0

        self.image = pygame.transform.rotate(self.image_original, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def reset(self, pos):
        self.pos = pygame.math.Vector2(int(pos[0] // self.tile_size) * self.tile_size,
                                      int(pos[1] // self.tile_size) * self.tile_size)
        self.target_pos = self.pos.copy()
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        self.key_left = False
        self.key_right = False
        self.key_up = False
        self.key_down = False
        self.move_dir = pygame.math.Vector2(0, 0)
        self.moving = False

        self.anim_index = 0
        self.anim_timer = 0
        self.image_original = self.idle_image
        self.image = self.idle_image
        self.angle = 0

        self.hp = self.max_hp
        self.hit_timer = 0.0

    def take_damage(self, amount):
        if self.hit_timer <= 0:
            self.hp -= amount
            self.hit_timer = self.hit_cooldown
            print(f"Hit! Current HP: {self.hp}")
