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

    def draw(self, surface, pos=(0,0), size=(200,20), color=(0,255,0), bg_color=(100,100,100)):
        pygame.draw.rect(surface, bg_color, (*pos, size[0], size[1]))
        width = int(size[0] * (self.display_value / self.max_value))
        pygame.draw.rect(surface, color, (*pos, width, size[1]))
        # 글꼴: 바 오른쪽 끝에 표시
        if self.font:
            text_surf = self.font.render(f"{int(self.display_value)}/{self.max_value}", True, (255,255,255))
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

    def draw(self, surface, pos=(0,0), size=(200,20)):
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
    def __init__(self, duration, font=None, pos=(0,0), radius=50, color=(255,255,255), bg_color=(100,100,100), thickness=5):
        """
        duration: 총 시간 (초)
        font: 글자 폰트
        pos: 원 중심 위치 (x,y)
        radius: 원 반지름
        color: 진행 호 색
        bg_color: 배경 원 색
        thickness: 호 두께
        """
        self.duration = duration
        self.remaining = duration
        self.font = font
        self.pos = pos
        self.radius = radius
        self.color = color
        self.bg_color = bg_color
        self.thickness = thickness
        self.running = False

    def start(self):
        self.running = True
        self.remaining = self.duration

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
        x, y = self.pos
        # 배경 원
        pygame.draw.circle(surface, self.bg_color, self.pos, self.radius)
        # 진행 호
        fraction = self.remaining / self.duration
        start_angle = -math.pi/2
        end_angle = start_angle + fraction * 2 * math.pi
        rect = pygame.Rect(x - self.radius, y - self.radius, self.radius*2, self.radius*2)
        pygame.draw.arc(surface, self.color, rect, start_angle, end_angle, self.thickness)
        # 중앙 텍스트
        if self.font:
            text_surf = self.font.render(f"{int(self.remaining)}s", True, self.color)
            text_rect = text_surf.get_rect(center=self.pos)
            surface.blit(text_surf, text_rect)
