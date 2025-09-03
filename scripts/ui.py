import pygame
import math

class HealthBar:
    def __init__(self, max_value, font=None, smooth_speed=100):
        self.max_value = max_value
        self.current_value = max_value
        self.display_value = max_value
        self.smooth_speed = smooth_speed
        self.font = font

    def update(self, dt, new_value):
        self.current_value = new_value
        if self.display_value < self.current_value:
            self.display_value += self.smooth_speed * dt
            if self.display_value > self.current_value:
                self.display_value = self.current_value
        elif self.display_value > self.current_value:
            self.display_value -= self.smooth_speed * dt
            if self.display_value < self.current_value:
                self.display_value = self.current_value

    def draw(self, surface, pos=(0,0), size=(130,13), color=(0,255,0), bg_color=(100,100,100)):
        pygame.draw.rect(surface, bg_color, (*pos, size[0], size[1]))
        width = int(size[0] * (self.display_value / self.max_value))
        pygame.draw.rect(surface, color, (*pos, width, size[1]))
        # 글꼴: 바 오른쪽 끝에 표시
        if self.font:
            text_surf = self.font.render(f"{int(self.display_value)}/{self.max_value}", True, (255,0,0))
            text_rect = text_surf.get_rect(midleft=(pos[0]+size[0]+10, pos[1]+size[1]//2))  # 바 오른쪽 10px 띄움
            surface.blit(text_surf, text_rect)

class cobwebBar:
    def __init__(self, max_value, font=None, smooth_speed=100):
        self.max_value = max_value
        self.current_value = max_value
        self.display_value = max_value
        self.smooth_speed = smooth_speed
        self.font = font
        self.color = (255,255,255)  # 기본 흰색 고정

    def update(self, dt, new_value):
        self.current_value = new_value
        if self.display_value < self.current_value:
            self.display_value += self.smooth_speed * dt
            if self.display_value > self.current_value:
                self.display_value = self.current_value
        elif self.display_value > self.current_value:
            self.display_value -= self.smooth_speed * dt
            if self.display_value < self.current_value:
                self.display_value = self.current_value

    def draw(self, surface, pos=(0,0), size=(130,13)):
        # 바 배경
        pygame.draw.rect(surface, (50,50,50), (*pos, size[0], size[1]))
        
        # 실제 값 바
        width = int(size[0] * (self.display_value / self.max_value))
        pygame.draw.rect(surface, self.color, (*pos, width, size[1]))
        
        # 글꼴: 바 오른쪽 끝에 표시
        if self.font:
            text_surf = self.font.render(f"{int(self.display_value)}/{self.max_value}", True, (255,255,255))
            text_rect = text_surf.get_rect(midleft=(pos[0]+size[0]+10, pos[1]+size[1]//2))  # 바 오른쪽 10px 띄움
            surface.blit(text_surf, text_rect)


class Timer:
    def __init__(self, duration, font=None, color=(255,255,255), pos=(0,0), bg_color=(0,0,0), padding=5):
        self.duration = duration
        self.remaining = duration
        self.font = font
        self.color = color
        self.pos = pos
        self.bg_color = bg_color
        self.padding = padding
        self.running = False

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def reset(self):
        self.remaining = self.duration
        self.running = False

    def update(self, dt):
        if self.running and self.remaining > 0:
            self.remaining -= dt
            if self.remaining < 0:
                self.remaining = 0

    def draw(self, surface):
        if not self.font:
            return
        text = f"{int(self.remaining)}s"
        text_surf = self.font.render(text, True, self.color)

        # 블럭 크기 계산 (텍스트 + padding)
        block_width = text_surf.get_width() + self.padding*2
        block_height = text_surf.get_height() + self.padding*2
        block_rect = pygame.Rect(0,0,block_width, block_height)
        block_rect.center = self.pos

        # 블럭 그리기
        pygame.draw.rect(surface, self.bg_color, block_rect, border_radius=5)

        # 텍스트 그리기
        text_rect = text_surf.get_rect(center=self.pos)
        surface.blit(text_surf, text_rect)
