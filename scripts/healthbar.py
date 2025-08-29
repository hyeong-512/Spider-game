import pygame

class HealthBar:
    def __init__(self, max_hp, size=(240, 22), border=2, font=None):
        self.max_hp = max_hp
        self.size = size
        self.border = border
        self.font = font or pygame.font.Font(None, 24)  # 기본 폰트

    def draw(self, surf, hp, pos=(20, 20)):
        x, y = pos
        w, h = self.size
        # 테두리
        pygame.draw.rect(surf, (0,0,0), (x- self.border, y- self.border, w+ self.border*2, h+ self.border*2), 0)
        # 배경
        pygame.draw.rect(surf, (200,200,200), (x, y, w, h))
        # 게이지
        ratio = max(0, min(1, hp / self.max_hp))
        fill_w = int(w * ratio)
        color = (50,200,80) if ratio > 0.4 else (255,165,0) if ratio > 0.2 else (220,50,50)
        pygame.draw.rect(surf, color, (x, y, fill_w, h))
        # 숫자
        txt = self.font.render(f"{int(hp)}/{self.max_hp}", True, (255,255,255))
        surf.blit(txt, (x + w + 10, y-2))
