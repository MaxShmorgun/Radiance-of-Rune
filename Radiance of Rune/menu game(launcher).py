import pygame
import sys
from easy_level import easy_level  
from midlle_level import midlle_level

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 768, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Сяйво Рун")

 
background = pygame.image.load("image/button.png.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

settings_icon = pygame.image.load("image/settings.png")
settings_icon = pygame.transform.scale(settings_icon, (50, 50))
settings_rect = settings_icon.get_rect(topright=(WIDTH - 10, 10))


pygame.mixer.music.load("music/load.music.wav")
volume = 0.5
pygame.mixer.music.set_volume(volume)
pygame.mixer.music.play(-1)


font = pygame.font.SysFont("timesnewroman", 48)
rules_font = pygame.font.SysFont("timesnewroman", 32)


WHITE = (255, 255, 255)
HOVER_COLOR = (255, 220, 150)


slider_dragging = False
fade_alpha = 0
fade_speed = 10
show_rules = False
show_settings = False
rules_alpha = 0
rules_scroll = 0


rules = [
    "🌟 Правила до гри 'Сяйво Рун':",
    "",
    "🎯 Мета:",
    "Зібрати всі Сині руни",
    "Дійти до Жовтої руни (фінішу)",
    "",
    "🕹️ Керування:",
    "←→ - рух, ↑ - стрибок",
    "ESC - меню",
    "",
    "📦 Предмети:",
    "Сині руни - обов'язкові (10)",
    "Зелені руни - +швидкість",
    "Червоні руни - смертельні",
    "Вороги - смертельні",
    "",
    "⚠️ Пастки:",
    "Лава, червоні руни",
    "Рухомі платформи",
    "",
    "💡 Порада:",
    "Плануйте маршрут!"
]


buttons = [
    {"text": "ПОЧАТИ ГРУ", "rect": pygame.Rect(185, 200, 400, 65)},
    {"text": "ПРАВИЛА",    "rect": pygame.Rect(185, 310, 400, 65)},
    {"text": "ВИЙТИ",      "rect": pygame.Rect(185, 425, 400, 65)},
]

def fade_overlay():
    global fade_alpha
    if fade_alpha < 180:
        fade_alpha = min(180, fade_alpha + fade_speed)
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, fade_alpha))
    screen.blit(overlay, (0, 0))

def fade_out():
    global fade_alpha
    while fade_alpha > 0:
        fade_alpha = max(0, fade_alpha - fade_speed)
        screen.blit(background, (0, 0))
        draw_buttons()
        screen.blit(settings_icon, settings_rect)
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, fade_alpha))
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        pygame.time.delay(10)

def difficulty_menu():
    global fade_alpha
    fade_alpha = 0
    running = True
    difficulty_buttons = [
        {"text": "🏰 Шлях Учня",   "rect": pygame.Rect(185, 200, 400, 65)},
        {"text": "⚔️ Випробування Воїна", "rect": pygame.Rect(185, 300, 400, 65)},
        {"text": "Повернутись до карти королівства",    "rect": pygame.Rect(185, 420, 400, 65)},
    ]
    
    while running:
        screen.blit(background, (0, 0))
        fade_overlay()
        
        for button in difficulty_buttons:
            mouse_over = button["rect"].collidepoint(pygame.mouse.get_pos())
            color = HOVER_COLOR if mouse_over else WHITE
            pygame.draw.rect(screen, (0, 0, 0), button["rect"], border_radius=10)
            text_surface = font.render(button["text"], True, color)
            text_rect = text_surface.get_rect(center=button["rect"].center)
            screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, button in enumerate(difficulty_buttons):
                    if button["rect"].collidepoint(event.pos):
                        if i == 0:
                            easy_level(screen)
                        elif i == 1:
                            midlle_level(screen)
                        elif i == 2:
                            running = False

        pygame.display.flip()

def draw_settings_menu():
    global volume
    overlay = pygame.Surface((WIDTH - 300, 250), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (150, 200))
    
    slider_x, slider_y, slider_w = 250, 240, 300
    pygame.draw.rect(screen, WHITE, (slider_x, slider_y, slider_w, 10))
    handle_x = int(slider_x + volume * slider_w)
    pygame.draw.circle(screen, (255, 0, 0), (handle_x, slider_y + 5), 12)
    
    vol_text = rules_font.render(f"Гучність: {int(volume * 100)}%", True, WHITE)
    screen.blit(vol_text, (slider_x, slider_y - 40))
    
    back_rect = pygame.Rect(300, 320, 100, 40)
    pygame.draw.rect(screen, (0, 0, 0), back_rect, border_radius=10)
    screen.blit(rules_font.render("Назад", True, WHITE), back_rect.move(10, 5))
    
    return pygame.Rect(slider_x, slider_y - 10, slider_w, 30), back_rect

def draw_rules_overlay():
    global rules_alpha, rules_scroll
    
    if rules_alpha < 180:
        rules_alpha += 5
    
    overlay = pygame.Surface((WIDTH - 100, HEIGHT - 200), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, rules_alpha))
    
    scroll_offset = rules_scroll * 30
    for i, line in enumerate(rules):
        y = 120 + i * 32 - scroll_offset
        if 100 < y < HEIGHT - 40:
            text = rules_font.render(line, True, WHITE)
            overlay.blit(text, (70, y - 100))
    
    screen.blit(overlay, (50, 100))

def draw_buttons():
    for button in buttons:
        mouse_over = button["rect"].collidepoint(pygame.mouse.get_pos())
        color = HOVER_COLOR if mouse_over else WHITE
        pygame.draw.rect(screen, (0, 0, 0), button["rect"], border_radius=10)
        text_surface = font.render(button["text"], True, color)
        text_rect = text_surface.get_rect(center=button["rect"].center)
        screen.blit(text_surface, text_rect)

def main_menu():
    global show_rules, rules_alpha, rules_scroll, show_settings, slider_dragging, volume
    
    clock = pygame.time.Clock()
    slider_rect, back_rect = None, None
    
    while True:
        screen.blit(background, (0, 0))
        draw_buttons()
        screen.blit(settings_icon, settings_rect)

        if show_rules:
            draw_rules_overlay()
        if show_settings:
            slider_rect, back_rect = draw_settings_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show_rules = False
                    show_settings = False
                    rules_alpha = 0
                    rules_scroll = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if show_settings:
                        if slider_rect and slider_rect.collidepoint(event.pos):
                            slider_dragging = True
                        elif back_rect and back_rect.collidepoint(event.pos):
                            show_settings = False
                    elif settings_rect.collidepoint(event.pos):
                        show_settings = True
                    elif show_rules:
                        show_rules = False
                        rules_alpha = 0
                        rules_scroll = 0
                    else:
                        for i, button in enumerate(buttons):
                            if button["rect"].collidepoint(event.pos):
                                if i == 0:
                                    difficulty_menu()
                                elif i == 1:
                                    show_rules = True
                                    rules_alpha = 0
                                    rules_scroll = 0
                                elif i == 2:
                                    pygame.quit()
                                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    slider_dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if slider_dragging and show_settings and slider_rect:
                    rel_x = event.pos[0] - 250
                    volume = max(0.0, min(1.0, rel_x / 300))
                    pygame.mixer.music.set_volume(volume)
            elif event.type == pygame.MOUSEWHEEL:
                if show_rules:
                    rules_scroll = max(0, rules_scroll - event.y)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main_menu()