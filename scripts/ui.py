import pygame

class HealthBar:
    def __init__(self, max_hp, font=None, size=(240,22), border=2, smooth_speed=100):
        self.max_hp = max_hp
        self.size = size
        self.border = border
        self.font = font or pygame.font.Font(None, 40)
        self.display_hp = max_hp
        self.smooth_speed = smooth_speed

    def update(self, dt, hp):
        if self.display_hp > hp:
            self.display_hp -= self.smooth_speed * dt
            if self.display_hp < hp:
                self.display_hp = hp
        else:
            self.display_hp = hp

    def draw(self, surf, pos=(20,20)):
        x, y = pos
        w, h = self.size
        pygame.draw.rect(surf, (0,0,0), (x-self.border, y-self.border, w+self.border*2, h+self.border*2))
        pygame.draw.rect(surf, (200,200,200), (x,y,w,h))
        ratio = max(0, min(1, self.display_hp/self.max_hp))
        color = (0,255,0) if ratio>0.4 else (255,165,0) if ratio>0.2 else (220,50,50)
        fill_w = int(w * ratio)
        pygame.draw.rect(surf, color, (x,y,fill_w,h))
        txt = self.font.render(f"{int(self.display_hp)}/{self.max_hp}", True, (255,255,255))
        surf.blit(txt, (x+w+10, y-2))