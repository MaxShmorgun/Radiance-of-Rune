import pygame
def midlle_level(screen):
    pygame.mixer.init()
    clock = pygame.time.Clock()
    WIDTH, HEIGHT = screen.get_size()
    font = pygame.font.SysFont("timesnewroman", 32)
    button_font = pygame.font.SysFont("timesnewroman", 24)

    player = pygame.Rect(100, 500, 72, 72)
    velocity_y = 0
    on_ground = False
    camera_x = 0
    score = 0
    speed_boost = False
    death_animation = False
    death_timer = 0
    rune_glow = []

    blue_runes = []
    green_runes = []

    def reset_game():
        nonlocal player, camera_x, score, blue_runes, green_runes, speed_boost, velocity_y, on_ground, death_animation, death_timer, rune_glow
        player.x, player.y = 100, 500
        camera_x = 0
        score = 0
        velocity_y = 0
        blue_runes[:] = [
            pygame.Rect(350, 435, 40, 40),    
            pygame.Rect(650, 375, 40, 40),    
            pygame.Rect(950, 320, 40, 40),    
            pygame.Rect(1200, 275, 40, 40),   
            pygame.Rect(1550, 225, 40, 40),   
            pygame.Rect(1850, 190, 40, 40),   
            pygame.Rect(2150, 290, 40, 40),   
            pygame.Rect(2400, 240, 40, 40),   
            pygame.Rect(2750, 220, 40, 40),   
            pygame.Rect(3050, 155, 40, 40)    
        ]
        green_runes[:] = [
            pygame.Rect(1000, 320, 40, 40),   
            pygame.Rect(6680, 160, 40, 40)     
        ]
        speed_boost = False
        on_ground = False
        death_animation = False
        death_timer = 0
        rune_glow.clear()
        for plat in platforms + [m.rect for m in moving_platforms]:
            if player.colliderect(plat):
                player.bottom = plat.top
                velocity_y = 0
                on_ground = True
                break

    rune_sound = pygame.mixer.Sound("music/rune.wav")
    win_sound = pygame.mixer.Sound("music/win_sound.wav")
    death_sound = pygame.mixer.Sound("music/death.wav")

    def load_sprite_sheet(path, frame_width, frame_height):
        sheet = pygame.image.load(path).convert_alpha()
        return [sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height)) for i in range(sheet.get_width() // frame_width)]

    def fade_in(screen, background, camera_x):
        fade = pygame.Surface(screen.get_size())
        fade.fill((0, 0, 0))
        for alpha in range(255, -1, -5):
            screen.blit(background, (-camera_x * 0.5, 0))
            fade.set_alpha(alpha)
            screen.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(10)

    hero_frames = load_sprite_sheet("image/hero.png", 72, 72)
    enemy_frames = load_sprite_sheet("image/enemy_smaller.png", 48, 48)
    rune_blue_img = pygame.image.load("image/rune_blue.png").convert_alpha()
    rune_green_img = pygame.image.load("image/rune_green.png").convert_alpha()
    rune_red_img = pygame.image.load("image/rune_red.png").convert_alpha()
    rune_yellow_img = pygame.image.load("image/reny_yellow.png").convert_alpha()
    platform_img = pygame.image.load("image/platform_fixed.png").convert_alpha()
    lava_img = pygame.image.load("image/lava.png").convert_alpha()

    bg_calm = pygame.image.load("image/fons.png").convert()
    level_width = 8000
    bg_calm = pygame.transform.scale(bg_calm, (level_width, HEIGHT))
    fade_in(screen, bg_calm, 0)

    lava_img = pygame.transform.scale(lava_img, (level_width, 100))
    exit_img = pygame.transform.scale(pygame.image.load("image/back_arrow.png").convert_alpha(), (100, 40))
    exit_button = exit_img.get_rect(topright=(WIDTH - 10, 10))
    retry_button = pygame.Rect(WIDTH // 2 - 110, HEIGHT // 2 + 60, 220, 50)
    menu_button = pygame.Rect(WIDTH // 2 - 110, HEIGHT // 2 + 120, 220, 50)

    player = pygame.Rect(100, 500, 72, 72)
    velocity_y = 0
    on_ground = False
    camera_x = 0
    score = 0
    total_runes = 10
    start_time = pygame.time.get_ticks()
    flash_time = 0
    timer_active = True
    game_over = False
    speed_boost = False
    boost_timer = 0
    death_animation = False
    death_timer = 0
    rune_glow = []

    
    platforms = [pygame.Rect(x, y, 180, 70) for x, y in [
        (0, HEIGHT - 170),   
        (300, 480),           
        (600, 420),           
        (900, 360),           
        (1200, 300),         
        (1500, 260),          
        (1800, 220),          
        (2100, 320),          
        (2400, 280),          
        (2700, 260),          
        (3000, 200),          
        (3300, 250),          
        (3600, 200),          
        (3900, 150),         
        (4200, 100),          
        (4500, 150),          
        (4800, 200),          
        (5100, 250),          
        (5400, 200),          
        (5700, 150),         
        (6000, 100),          
        (6300, 150),          
        (6600, 200),          
        (6900, 250),          
        (7200, 200),          
        (7500, 150)           
    ]]

    class MovingPlatform:
        def __init__(self, x, y, width, height, range_x=0):
            self.rect = pygame.Rect(x, y, width, height)
            self.start_x = x
            self.range_x = range_x
            self.dir_x = 1
            self.spawn_time = pygame.time.get_ticks()
        
        def update(self):
            if self.range_x:
                self.rect.x += self.dir_x * 2
                if abs(self.rect.x - self.start_x) >= self.range_x:
                    self.dir_x *= -1
        
        def animate_spawn(self):
            return min(int((pygame.time.get_ticks() - self.spawn_time) / 2), 255)

    moving_platforms = [
        MovingPlatform(3800, 80, 180, 70, range_x=200),  
        MovingPlatform(5500, 130, 180, 70, range_x=150)   
    ]

    platforms.append(pygame.Rect(7800, 200, 180, 70))  

    
    red_runes = [
        pygame.Rect(1200 + 70, 260, 40, 40),   
        pygame.Rect(2400 + 70, 240, 40, 40),  
        pygame.Rect(3600 + 70, 160, 40, 40),   
        pygame.Rect(4800 + 70, 175, 40, 40),   
        pygame.Rect(6000 + 70, 75, 40, 40)     
    ]

    gold_rune = pygame.Rect(7850, 130, 50, 50)  

    
    enemies = [
        {'rect': pygame.Rect(600 + 30, 370, 48, 48), 'left': 600, 'right': 600 + 180 - 48, 'dir': 1},   
        {'rect': pygame.Rect(1500 + 30, 215, 48, 48), 'left': 1500, 'right': 1500 + 180 - 48, 'dir': 1}, 
        {'rect': pygame.Rect(2100 + 30, 280, 48, 48), 'left': 2100, 'right': 2100 + 180 - 48, 'dir': 1},  
        {'rect': pygame.Rect(2700 + 30, 220,48, 48), 'left': 2700, 'right': 2700 + 180 - 48, 'dir': 1},  
        {'rect': pygame.Rect(3300 + 30, 210, 48, 48), 'left': 3300, 'right': 3300 + 180 - 48, 'dir': 1},  
        {'rect': pygame.Rect(3900 + 30, 110, 48, 48), 'left': 3900, 'right': 3900 + 180 - 48, 'dir': 1},   
        {'rect': pygame.Rect(4500 + 30, 120, 48, 48), 'left': 4500, 'right': 4500 + 180 - 48, 'dir': 1},  
        {'rect': pygame.Rect(5100 + 30, 215, 48, 48), 'left': 5100, 'right': 5100 + 180 - 48, 'dir': 1}   
    ]

    reset_game()

    while True:
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
                    return
                if game_over:
                    if retry_button.collidepoint(event.pos):
                        return midlle_level(screen)
                    if menu_button.collidepoint(event.pos):
                        return
        if keys[pygame.K_ESCAPE]:
            return

        if not game_over:
            if death_animation:
                if pygame.time.get_ticks() - death_timer > 1500:
                    reset_game()
                else:
                    fade = pygame.Surface((WIDTH, HEIGHT))
                    fade.fill((0, 0, 0))
                    fade.set_alpha(min(255, int(255 * (pygame.time.get_ticks() - death_timer) / 1500)))
                    screen.blit(bg_calm, (-camera_x * 0.5, 0))
                    for plat in platforms:
                        screen.blit(platform_img, plat.move(-camera_x, 0))
                    screen.blit(fade, (0, 0))
                    pygame.display.flip()
                    clock.tick(60)
                    continue

            move_speed = 8 if speed_boost else 5
            if keys[pygame.K_LEFT]:
                player.x -= move_speed
            if keys[pygame.K_RIGHT]:
                player.x += move_speed
            if keys[pygame.K_UP] and on_ground:
                velocity_y = -12

            velocity_y += 0.5
            player.y += velocity_y

            for mplat in moving_platforms:
                mplat.update()

            if player.y > HEIGHT - 100:
                death_sound.play()
                death_animation = True
                death_timer = pygame.time.get_ticks()

            on_ground = False
            for plat in platforms + [m.rect for m in moving_platforms]:
                if player.colliderect(plat):
                    if velocity_y >= 0 and player.bottom - plat.top < 20:
                        player.bottom = plat.top
                        velocity_y = 0
                        on_ground = True

            for rune in blue_runes[:]:
                if player.colliderect(rune):
                    blue_runes.remove(rune)
                    rune_sound.play()
                    score += 1
                    rune_glow.append((pygame.time.get_ticks(), rune.center))

            for rune in green_runes[:]:
                if player.colliderect(rune):
                    green_runes.remove(rune)
                    speed_boost = True
                    boost_timer = pygame.time.get_ticks()
                    rune_glow.append((pygame.time.get_ticks(), rune.center))

            if speed_boost and pygame.time.get_ticks() - boost_timer > 5000:
                speed_boost = False

            if any(player.colliderect(rune) for rune in red_runes) or \
               any(player.colliderect(enemy['rect']) for enemy in enemies):
                death_sound.play()
                death_animation = True
                death_timer = pygame.time.get_ticks()

            for enemy in enemies:
                enemy['rect'].x += enemy['dir']
                if enemy['rect'].x <= enemy['left'] or enemy['rect'].x >= enemy['right']:
                    enemy['dir'] *= -1

            if player.colliderect(gold_rune) and score == total_runes:
                game_over = True
                timer_active = False
                flash_time = pygame.time.get_ticks()
                win_sound.play()

            target_camera_x = player.x - WIDTH // 2
            camera_x += (target_camera_x - camera_x) * 0.1
            camera_x = max(0, min(camera_x, level_width - WIDTH))

        screen.blit(bg_calm, (-camera_x * 0.5, 0))
        for plat in platforms:
            screen.blit(platform_img, plat.move(-camera_x, 0))
        for mplat in moving_platforms:
            surface = platform_img.copy()
            surface.set_alpha(mplat.animate_spawn())
            screen.blit(surface, mplat.rect.move(-camera_x, 0))

        for rune in blue_runes:
            screen.blit(rune_blue_img, rune.move(-camera_x, 0))
        for rune in green_runes:
            screen.blit(rune_green_img, rune.move(-camera_x, 0))
        for rune in red_runes:
            screen.blit(rune_red_img, rune.move(-camera_x, 0))
        screen.blit(rune_yellow_img, gold_rune.move(-camera_x, 0))

        for glow_time, center in rune_glow[:]:
            elapsed = pygame.time.get_ticks() - glow_time
            if elapsed < 400:
                radius = 30 + elapsed // 10
                alpha = 255 - elapsed // 2
                glow = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow, (255, 255, 100, alpha), (radius, radius), radius)
                screen.blit(glow, (center[0] - radius - camera_x, center[1] - radius))
            else:
                rune_glow.remove((glow_time, center))

        screen.blit(hero_frames[(pygame.time.get_ticks() // 150) % len(hero_frames)], player.move(-camera_x, 0))
        for enemy in enemies:
            screen.blit(enemy_frames[(pygame.time.get_ticks() // 200) % len(enemy_frames)], enemy['rect'].move(-camera_x, 0))
        screen.blit(lava_img, (-camera_x, HEIGHT - 100))
        screen.blit(exit_img, exit_button)
        screen.blit(font.render(f"Руни: {score}/{total_runes}", True, (255, 255, 255)), (10, 10))
        if timer_active:
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
            screen.blit(font.render(f"⏱ Час: {elapsed_time} с", True, (255, 255, 255)), (10, 50))

        progress = min(1.0, player.x / (level_width - 100))
        bar_width = 300
        bar_height = 20
        bar_x = WIDTH // 2 - bar_width // 2
        bar_y = 20
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height), border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, int(bar_width * progress), bar_height), border_radius=10)
        percent_text = font.render(f"{int(progress * 100)}%", True, (255, 255, 255))
        screen.blit(percent_text, (bar_x + bar_width + 10, bar_y - 2))

        if game_over:
            if pygame.time.get_ticks() - flash_time < 500:
                flash = pygame.Surface((WIDTH, HEIGHT))
                flash.set_alpha(150)
                flash.fill((255, 255, 255))
                screen.blit(flash, (0, 0))
            else:
                dark = pygame.Surface((WIDTH, HEIGHT))
                dark.set_alpha(min((pygame.time.get_ticks() - flash_time - 500) // 2, 180))
                dark.fill((0, 0, 0))
                screen.blit(dark, (0, 0))

            win_text = font.render("🎉 Ви пройшли рівень!", True, (0, 128, 0))
            screen.blit(win_text, win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60)))
            screen.blit(font.render(f"⏱ Час: {elapsed_time} с", True, (255, 100, 0)),
                        (WIDTH // 2 - 80, HEIGHT // 2 - 20))

            mouse_hover_retry = retry_button.collidepoint(mouse_pos)
            mouse_hover_menu = menu_button.collidepoint(mouse_pos)

            retry_color = (0, 255, 0) if mouse_hover_retry else (0, 200, 0)
            menu_color = (0, 200, 200) if mouse_hover_menu else (0, 150, 150)

            pygame.draw.rect(screen, retry_color, retry_button, border_radius=10)
            pygame.draw.rect(screen, menu_color, menu_button, border_radius=10)

            retry_text = button_font.render("🔁 Спробувати ще раз", True, (0, 0, 0))
            menu_text = button_font.render("⬅️ Вийти в меню", True, (0, 0, 0))

            retry_text_rect = retry_text.get_rect(center=retry_button.center)
            menu_text_rect = menu_text.get_rect(center=menu_button.center)

            screen.blit(retry_text, retry_text_rect)
            screen.blit(menu_text, menu_text_rect)

        pygame.display.flip()
        clock.tick(60)