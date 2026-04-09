#!/usr/bin/env python3
"""
Spearified Desktop App - Real Game Client
A desktop multiplayer tag game with maps and game modes.
"""

import pygame
import asyncio
import websockets
import json
import random
import sys
import math
from enum import Enum

# Initialize Pygame
pygame.init()
pygame.font.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60
PLAYER_SIZE = 20
OBSTACLE_SIZE = 30
WORLD_SIZE = 100  # World is -50 to +50 in each direction

# Colors - Modern Palette
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 59, 48)
GREEN = (52, 199, 89)
BLUE = (0, 122, 255)
YELLOW = (255, 204, 0)
ORANGE = (255, 149, 0)
PURPLE = (175, 82, 222)
PINK = (255, 45, 85)
GRAY = (142, 142, 147)
DARK_GRAY = (44, 44, 46)
LIGHT_GRAY = (229, 229, 234)
DARK_BLUE = (0, 39, 118)
NEON_GREEN = (48, 209, 88)
NEON_BLUE = (64, 156, 255)
NEON_PURPLE = (191, 90, 242)
BROWN = (139, 69, 19)
CYAN = (0, 255, 255)

class GameState(Enum):
    MENU = 0
    LOGIN = 1
    REGISTER = 2
    PLAYING = 3

class DesktopGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Spearified - Modern Edition")
        self.clock = pygame.time.Clock()
        
        # Modern Fonts
        try:
            self.font = pygame.font.SysFont('Segoe UI', 24)
            self.small_font = pygame.font.SysFont('Segoe UI', 16)
            self.large_font = pygame.font.SysFont('Segoe UI', 48)
            self.title_font = pygame.font.SysFont('Segoe UI', 72)
        except:
            # Fallback fonts
            self.font = pygame.font.SysFont('Arial', 24)
            self.small_font = pygame.font.SysFont('Arial', 16)
            self.large_font = pygame.font.SysFont('Arial', 36)
            self.title_font = pygame.font.SysFont('Arial', 48)

        self.game_state = GameState.MENU
        self.websocket = None
        self.player_id = None
        self.username = ""
        self.game_data = None

        # Input fields
        self.login_username = ""
        self.login_password = ""
        self.register_username = ""
        self.register_password = ""
        self.active_input = None

        # Player position and movement
        self.player_x = 0
        self.player_y = 0
        self.keys_pressed = set()

        # Camera
        self.camera_x = 0
        self.camera_y = 0

        # Mini-map settings
        self.mini_map_size = 200
        self.mini_map_x = SCREEN_WIDTH - self.mini_map_size - 20
        self.mini_map_y = 100
        self.world_size = WORLD_SIZE

        # Animation
        self.animation_time = 0

    def draw_mini_map(self):
        if not self.game_data:
            return

        # Mini-map background with border
        pygame.draw.rect(self.screen, DARK_GRAY, 
                        (self.mini_map_x - 5, self.mini_map_y - 5, 
                         self.mini_map_size + 10, self.mini_map_size + 10), 
                        border_radius=10)
        pygame.draw.rect(self.screen, BLACK, 
                        (self.mini_map_x, self.mini_map_y, 
                         self.mini_map_size, self.mini_map_size))

        # Draw obstacles on mini-map
        if self.game_data.get('current_map', {}).get('obstacles'):
            for obstacle in self.game_data['current_map']['obstacles']:
                # Convert world coordinates to mini-map coordinates
                map_x = self.mini_map_x + (obstacle['x'] + self.world_size//2) / self.world_size * self.mini_map_size
                map_y = self.mini_map_y + (obstacle['y'] + self.world_size//2) / self.world_size * self.mini_map_size
                
                if (self.mini_map_x <= map_x <= self.mini_map_x + self.mini_map_size and 
                    self.mini_map_y <= map_y <= self.mini_map_y + self.mini_map_size):
                    
                    color = GREEN
                    if obstacle.get('type') == 'building':
                        color = GRAY
                    elif obstacle.get('type') == 'dune':
                        color = (210, 180, 140)
                    elif obstacle.get('type') == 'mountain':
                        color = BROWN
                    elif obstacle.get('type') == 'station':
                        color = (192, 192, 192)
                    elif obstacle.get('type') == 'volcano':
                        color = RED
                    
                    pygame.draw.circle(self.screen, color, (int(map_x), int(map_y)), 2)

        # Draw players on mini-map
        for player in self.game_data['players']:
            # Convert world coordinates to mini-map coordinates
            map_x = self.mini_map_x + (player['x'] + self.world_size//2) / self.world_size * self.mini_map_size
            map_y = self.mini_map_y + (player['z'] + self.world_size//2) / self.world_size * self.mini_map_size
            
            if (self.mini_map_x <= map_x <= self.mini_map_x + self.mini_map_size and 
                self.mini_map_y <= map_y <= self.mini_map_y + self.mini_map_size):
                
                color = GREEN
                if self.game_data['game_mode'] == 'tag' and player.get('isTagger'):
                    color = RED
                elif self.game_data['game_mode'] == 'zombie' and player.get('isZombie'):
                    color = GRAY
                elif self.game_data['game_mode'] == 'bomb' and player['userId'] == self.game_data.get('bombHolder'):
                    color = ORANGE
                
                # Highlight current player
                if player['userId'] == self.player_id:
                    pygame.draw.circle(self.screen, WHITE, (int(map_x), int(map_y)), 4)
                    pygame.draw.circle(self.screen, color, (int(map_x), int(map_y)), 3)
                else:
                    pygame.draw.circle(self.screen, color, (int(map_x), int(map_y)), 2)

        # Mini-map border
        pygame.draw.rect(self.screen, WHITE, 
                        (self.mini_map_x, self.mini_map_y, 
                         self.mini_map_size, self.mini_map_size), 
                        2, border_radius=5)

    async def connect_websocket(self):
        try:
            self.websocket = await websockets.connect('ws://localhost:8765')
            print("Connected to server!")
            return True
        except Exception as e:
            print(f"Failed to connect: {e}")
            return False

    def draw_text(self, text, x, y, color=WHITE, font=None):
        if font is None:
            font = self.font
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_button(self, text, x, y, width, height, color, hover_color=None, glow=False):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        is_hovered = x <= mouse_x <= x + width and y <= mouse_y <= y + height

        button_color = hover_color if is_hovered and hover_color else color
        
        # Modern rounded rectangle with glow effect
        if glow or is_hovered:
            glow_surface = pygame.Surface((width + 20, height + 20), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (*button_color[:3], 100), (0, 0, width + 20, height + 20), border_radius=15)
            self.screen.blit(glow_surface, (x - 10, y - 10))

        pygame.draw.rect(self.screen, button_color, (x, y, width, height), border_radius=10)
        pygame.draw.rect(self.screen, WHITE, (x, y, width, height), 2, border_radius=10)

        # Modern text with shadow
        text_surface = self.font.render(text, True, BLACK)
        shadow_surface = self.font.render(text, True, (0, 0, 0, 128))
        text_x = x + (width - text_surface.get_width()) // 2
        text_y = y + (height - text_surface.get_height()) // 2
        
        self.screen.blit(shadow_surface, (text_x + 1, text_y + 1))
        self.screen.blit(text_surface, (text_x, text_y))

        return is_hovered

    def draw_menu(self):
        # Animated gradient background
        self.animation_time += 1
        gradient_color1 = (20 + abs(math.sin(self.animation_time * 0.01)) * 50, 
                          50 + abs(math.sin(self.animation_time * 0.015)) * 100, 
                          100 + abs(math.sin(self.animation_time * 0.02)) * 155)
        gradient_color2 = (50 + abs(math.sin(self.animation_time * 0.02)) * 100,
                          20 + abs(math.sin(self.animation_time * 0.01)) * 50,
                          150 + abs(math.sin(self.animation_time * 0.015)) * 105)
        
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            color = (
                int(gradient_color1[0] * (1 - ratio) + gradient_color2[0] * ratio),
                int(gradient_color1[1] * (1 - ratio) + gradient_color2[1] * ratio),
                int(gradient_color1[2] * (1 - ratio) + gradient_color2[2] * ratio)
            )
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))

        # Modern title with glow effect
        title = self.title_font.render("SPEARIFIED", True, WHITE)
        glow_title = self.title_font.render("SPEARIFIED", True, NEON_BLUE)
        
        title_x = SCREEN_WIDTH//2 - title.get_width()//2
        title_y = 80
        
        # Glow effect
        for offset in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
            self.screen.blit(glow_title, (title_x + offset[0], title_y + offset[1]))
        
        self.screen.blit(title, (title_x, title_y))

        subtitle = self.font.render("Modern Multiplayer Gaming Experience", True, LIGHT_GRAY)
        self.screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 160))

        # Animated buttons with modern styling
        button_width = 350
        button_height = 60
        button_x = SCREEN_WIDTH//2 - button_width//2
        base_y = 280

        # Pulsing animation for buttons
        pulse = abs(math.sin(self.animation_time * 0.05)) * 0.1 + 0.9

        if self.draw_button("Login", button_x, int(base_y * pulse), button_width, button_height, NEON_BLUE, NEON_PURPLE, glow=True):
            if pygame.mouse.get_pressed()[0]:
                self.game_state = GameState.LOGIN

        if self.draw_button("Register", button_x, int((base_y + 80) * pulse), button_width, button_height, NEON_GREEN, GREEN, glow=True):
            if pygame.mouse.get_pressed()[0]:
                self.game_state = GameState.REGISTER

        if self.draw_button("Quick Play (Guest)", button_x, int((base_y + 160) * pulse), button_width, button_height, ORANGE, YELLOW, glow=True):
            if pygame.mouse.get_pressed()[0]:
                self.username = f"Guest{random.randint(100, 999)}"
                self.player_id = f"player_{random.randint(1000, 9999)}"
                self.game_state = GameState.PLAYING
                asyncio.create_task(self.join_game())

        # Modern feature list
        features = [
            "🎮 9 Random Maps • ⚡ Real-time Multiplayer",
            "🏃 Smooth Movement • 🎯 Multiple Game Modes",
            "💫 Particle Effects • 🎨 Modern UI Design"
        ]

        for i, feature in enumerate(features):
            feature_surface = self.small_font.render(feature, True, LIGHT_GRAY)
            self.screen.blit(feature_surface, (SCREEN_WIDTH//2 - feature_surface.get_width()//2, 550 + i * 30))

    def draw_login(self):
        # Modern gradient background
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            color = (
                int(50 * (1 - ratio) + 20 * ratio),
                int(50 * (1 - ratio) + 100 * ratio),
                int(100 * (1 - ratio) + 150 * ratio)
            )
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))

        title = self.large_font.render("LOGIN", True, WHITE)
        glow_title = self.large_font.render("LOGIN", True, NEON_BLUE)
        
        title_x = SCREEN_WIDTH//2 - title.get_width()//2
        title_y = 100
        
        # Glow effect
        for offset in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
            self.screen.blit(glow_title, (title_x + offset[0], title_y + offset[1]))
        
        self.screen.blit(title, (title_x, title_y))

        # Modern input fields with rounded corners
        input_width = 400
        input_height = 50
        input_x = SCREEN_WIDTH//2 - input_width//2

        # Username field
        self.draw_text("Username:", input_x, 220, LIGHT_GRAY)
        pygame.draw.rect(self.screen, WHITE if self.active_input == "login_username" else DARK_GRAY,
                        (input_x, 250, input_width, input_height), border_radius=10)
        pygame.draw.rect(self.screen, NEON_BLUE if self.active_input == "login_username" else GRAY,
                        (input_x, 250, input_width, input_height), 3, border_radius=10)
        username_text = self.font.render(self.login_username, True, WHITE)
        self.screen.blit(username_text, (input_x + 15, 265))

        # Password field
        self.draw_text("Password:", input_x, 330, LIGHT_GRAY)
        pygame.draw.rect(self.screen, WHITE if self.active_input == "login_password" else DARK_GRAY,
                        (input_x, 360, input_width, input_height), border_radius=10)
        pygame.draw.rect(self.screen, NEON_BLUE if self.active_input == "login_password" else GRAY,
                        (input_x, 360, input_width, input_height), 3, border_radius=10)
        password_text = self.font.render("*" * len(self.login_password), True, WHITE)
        self.screen.blit(password_text, (input_x + 15, 375))

        # Modern buttons
        button_width = 180
        button_height = 50
        button_spacing = 40

        if self.draw_button("Login", input_x, 450, button_width, button_height, NEON_BLUE, NEON_PURPLE, glow=True):
            if pygame.mouse.get_pressed()[0]:
                asyncio.create_task(self.login())

        if self.draw_button("Back", input_x + button_width + button_spacing, 450, button_width, button_height, GRAY, DARK_GRAY):
            if pygame.mouse.get_pressed()[0]:
                self.game_state = GameState.MENU

    def draw_register(self):
        self.screen.fill((100, 50, 50))

        title = self.large_font.render("REGISTER", True, WHITE)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))

        # Username field
        self.draw_text("Username:", 400, 200)
        pygame.draw.rect(self.screen, WHITE if self.active_input == "register_username" else GRAY,
                        (400, 230, 400, 40), 2)
        username_text = self.font.render(self.register_username, True, WHITE)
        self.screen.blit(username_text, (410, 240))

        # Password field
        self.draw_text("Password:", 400, 300)
        pygame.draw.rect(self.screen, WHITE if self.active_input == "register_password" else GRAY,
                        (400, 330, 400, 40), 2)
        password_text = self.font.render("*" * len(self.register_password), True, WHITE)
        self.screen.blit(password_text, (410, 340))

        # Buttons
        if self.draw_button("Register", 450, 400, 150, 50, GREEN):
            if pygame.mouse.get_pressed()[0]:
                asyncio.create_task(self.register())

        if self.draw_button("Back", 450, 470, 150, 50, RED):
            if pygame.mouse.get_pressed()[0]:
                self.game_state = GameState.MENU

    def draw_game(self):
        if not self.game_data:
            self.screen.fill(BLACK)
            self.draw_text("Connecting to game...", SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2)
            return

        # Set background based on map
        if self.game_data.get('current_map'):
            map_name = self.game_data['current_map']['name'].lower()
            if 'forest' in map_name:
                bg_color = (34, 139, 34)
            elif 'city' in map_name:
                bg_color = (112, 128, 144)
            elif 'desert' in map_name:
                bg_color = (244, 164, 96)
            elif 'mountain' in map_name:
                bg_color = (139, 69, 19)
            elif 'beach' in map_name:
                bg_color = (135, 206, 235)
            elif 'space' in map_name:
                bg_color = (25, 25, 112)
            elif 'underwater' in map_name:
                bg_color = (0, 0, 128)
            elif 'castle' in map_name:
                bg_color = (218, 165, 32)
            elif 'volcano' in map_name:
                bg_color = (139, 0, 0)
            else:
                bg_color = (135, 206, 235)
        else:
            bg_color = (135, 206, 235)

        self.screen.fill(bg_color)

        # Update camera to follow player
        if self.game_data['players']:
            current_player = next((p for p in self.game_data['players'] if p['id'] == self.player_id), None)
            if current_player:
                self.camera_x = current_player['x'] - SCREEN_WIDTH//2
                self.camera_y = current_player['z'] - SCREEN_HEIGHT//2

        # Draw obstacles
        if self.game_data.get('obstacles'):
            for obstacle in self.game_data['obstacles']:
                screen_x = obstacle['x'] - self.camera_x
                screen_y = obstacle['z'] - self.camera_y

                if -50 <= screen_x <= SCREEN_WIDTH + 50 and -50 <= screen_y <= SCREEN_HEIGHT + 50:
                    color = GREEN  # default
                    if obstacle['type'] == 'building':
                        color = GRAY
                    elif obstacle['type'] == 'dune':
                        color = (210, 180, 140)
                    elif obstacle['type'] == 'mountain':
                        color = BROWN
                    elif obstacle['type'] == 'station':
                        color = (192, 192, 192)
                    elif obstacle['type'] == 'volcano':
                        color = RED
                    elif obstacle['type'] == 'lava':
                        color = (255, 69, 0)

                    pygame.draw.circle(self.screen, color,
                                     (int(screen_x), int(screen_y)),
                                     obstacle['size'])

        # Draw players
        for player in self.game_data['players']:
            screen_x = player['x'] - self.camera_x
            screen_y = player['z'] - self.camera_y

            if -50 <= screen_x <= SCREEN_WIDTH + 50 and -50 <= screen_y <= SCREEN_HEIGHT + 50:
                color = GREEN
                if self.game_data['game_mode'] == 'tag' and player.get('is_tagger'):
                    color = RED
                elif self.game_data['game_mode'] == 'zombie' and player.get('is_zombie'):
                    color = GRAY
                elif self.game_data['game_mode'] == 'bomb' and player['id'] == self.game_data.get('bomb_holder'):
                    color = ORANGE

                pygame.draw.circle(self.screen, color, (int(screen_x), int(screen_y)), PLAYER_SIZE//2)

                # Draw name
                name_text = self.small_font.render(player['username'], True, WHITE)
                self.screen.blit(name_text, (screen_x - name_text.get_width()//2, screen_y - 40))

        # Draw UI
        self.draw_game_ui()

    def draw_game_ui(self):
        # Modern semi-transparent HUD background
        hud_height = 80
        hud_surface = pygame.Surface((SCREEN_WIDTH, hud_height), pygame.SRCALPHA)
        pygame.draw.rect(hud_surface, (0, 0, 0, 180), (0, 0, SCREEN_WIDTH, hud_height), border_radius=15)
        self.screen.blit(hud_surface, (0, 0))

        # Top bar with modern styling
        pygame.draw.rect(self.screen, NEON_BLUE, (0, 0, SCREEN_WIDTH, 5))  # Accent line

        # Map name with glow effect
        if self.game_data.get('current_map'):
            map_name = self.game_data['current_map']['name']
            map_title = self.large_font.render(map_name, True, WHITE)
            glow_map_title = self.large_font.render(map_name, True, NEON_PURPLE)
            
            title_x = 30
            title_y = 15
            
            # Subtle glow
            self.screen.blit(glow_map_title, (title_x + 1, title_y + 1))
            self.screen.blit(map_title, (title_x, title_y))

        # Game mode and timer with modern badge
        mode_text = f"Mode: {self.game_data['game_mode'].upper()}"
        if self.game_data['game_mode'] == 'bomb' and self.game_data.get('bomb_timer', 0) > 0:
            mode_text += f" - Bomb: {math.ceil(self.game_data['bomb_timer'] / 1000)}s"
        
        mode_surface = self.font.render(mode_text, True, LIGHT_GRAY)
        self.screen.blit(mode_surface, (30, 45))

        # Player count with icon
        players_text = f"👥 {len(self.game_data['players'])} Players"
        players_surface = self.font.render(players_text, True, LIGHT_GRAY)
        self.screen.blit(players_surface, (SCREEN_WIDTH//2 - players_surface.get_width()//2, 20))

        # FPS and ping (placeholder)
        fps_text = f"FPS: {int(self.clock.get_fps())}"
        fps_surface = self.small_font.render(fps_text, True, GRAY)
        self.screen.blit(fps_surface, (SCREEN_WIDTH - 200, 15))

        ping_text = "Ping: 23ms"
        ping_surface = self.small_font.render(ping_text, True, GRAY)
        self.screen.blit(ping_surface, (SCREEN_WIDTH - 200, 35))

        # Controls help in bottom right
        controls = [
            "WASD: Move",
            "ESC: Menu",
            "Mouse: Camera"
        ]
        
        controls_bg = pygame.Surface((180, 80), pygame.SRCALPHA)
        pygame.draw.rect(controls_bg, (0, 0, 0, 150), (0, 0, 180, 80), border_radius=10)
        self.screen.blit(controls_bg, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 100))
        
        for i, control in enumerate(controls):
            control_surface = self.small_font.render(control, True, WHITE)
            self.screen.blit(control_surface, (SCREEN_WIDTH - 190, SCREEN_HEIGHT - 85 + i * 20))

        # Draw mini-map
        self.draw_mini_map()

        # World boundaries indicator
        boundary_size = 10
        pygame.draw.rect(self.screen, RED, (0, 0, SCREEN_WIDTH, boundary_size))  # Top
        pygame.draw.rect(self.screen, RED, (0, 0, boundary_size, SCREEN_HEIGHT))  # Left
        pygame.draw.rect(self.screen, RED, (SCREEN_WIDTH - boundary_size, 0, boundary_size, SCREEN_HEIGHT))  # Right
        pygame.draw.rect(self.screen, RED, (0, SCREEN_HEIGHT - boundary_size, SCREEN_WIDTH, boundary_size))  # Bottom

    async def login(self):
        if not self.websocket:
            connected = await self.connect_websocket()
            if not connected:
                return

        await self.websocket.send(json.dumps({
            'type': 'login',
            'username': self.login_username,
            'password': self.login_password
        }))

    async def register(self):
        if not self.websocket:
            connected = await self.connect_websocket()
            if not connected:
                return

        await self.websocket.send(json.dumps({
            'type': 'register',
            'username': self.register_username,
            'password': self.register_password
        }))

    async def join_game(self):
        if not self.websocket:
            connected = await self.connect_websocket()
            if not connected:
                return

        await self.websocket.send(json.dumps({
            'type': 'join',
            'player_id': self.player_id,
            'username': self.username
        }))

    async def handle_websocket_messages(self):
        try:
            async for message in self.websocket:
                data = json.loads(message)
                if data['type'] == 'auth_response':
                    if data['success']:
                        self.player_id = data.get('player_id', self.player_id)
                        self.game_state = GameState.PLAYING
                        await self.join_game()
                    else:
                        print(f"Auth failed: {data['message']}")
                elif data['type'] == 'game_state':
                    self.game_data = data['data']
                elif data['type'] == 'chat':
                    print(f"Chat: {data['username']}: {data['message']}")
        except Exception as e:
            print(f"WebSocket error: {e}")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == GameState.PLAYING:
                        self.game_state = GameState.MENU
                    else:
                        return False
                elif self.game_state == GameState.LOGIN:
                    if event.key == pygame.K_BACKSPACE:
                        if self.active_input == "login_username":
                            self.login_username = self.login_username[:-1]
                        elif self.active_input == "login_password":
                            self.login_password = self.login_password[:-1]
                    elif event.key == pygame.K_TAB:
                        if self.active_input == "login_username":
                            self.active_input = "login_password"
                        else:
                            self.active_input = "login_username"
                    elif event.key == pygame.K_RETURN:
                        asyncio.create_task(self.login())
                    else:
                        if self.active_input == "login_username":
                            self.login_username += event.unicode
                        elif self.active_input == "login_password":
                            self.login_password += event.unicode
                elif self.game_state == GameState.REGISTER:
                    if event.key == pygame.K_BACKSPACE:
                        if self.active_input == "register_username":
                            self.register_username = self.register_username[:-1]
                        elif self.active_input == "register_password":
                            self.register_password = self.register_password[:-1]
                    elif event.key == pygame.K_TAB:
                        if self.active_input == "register_username":
                            self.active_input = "register_password"
                        else:
                            self.active_input = "register_username"
                    elif event.key == pygame.K_RETURN:
                        asyncio.create_task(self.register())
                    else:
                        if self.active_input == "register_username":
                            self.register_username += event.unicode
                        elif self.active_input == "register_password":
                            self.register_password += event.unicode
                else:
                    self.keys_pressed.add(event.key)
            elif event.type == pygame.KEYUP:
                self.keys_pressed.discard(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_x, mouse_y = event.pos
                    if self.game_state == GameState.LOGIN:
                        if 400 <= mouse_x <= 800:
                            if 230 <= mouse_y <= 270:
                                self.active_input = "login_username"
                            elif 330 <= mouse_y <= 370:
                                self.active_input = "login_password"
                    elif self.game_state == GameState.REGISTER:
                        if 400 <= mouse_x <= 800:
                            if 230 <= mouse_y <= 270:
                                self.active_input = "register_username"
                            elif 330 <= mouse_y <= 370:
                                self.active_input = "register_password"
        return True

    def update_movement(self):
        if self.game_state != GameState.PLAYING or not self.websocket:
            return

        dx = 0
        dz = 0
        speed = 2

        if pygame.K_w in self.keys_pressed:
            dz -= speed
        if pygame.K_s in self.keys_pressed:
            dz += speed
        if pygame.K_a in self.keys_pressed:
            dx -= speed
        if pygame.K_d in self.keys_pressed:
            dx += speed

        if dx != 0 or dz != 0:
            self.player_x += dx
            self.player_y += dz

            asyncio.create_task(self.send_movement())

    async def send_movement(self):
        if self.websocket:
            await self.websocket.send(json.dumps({
                'type': 'move',
                'x': self.player_x,
                'y': 1,
                'z': self.player_y
            }))

    async def run(self):
        running = True

        # Start WebSocket message handler
        if self.game_state in [GameState.LOGIN, GameState.REGISTER, GameState.PLAYING]:
            asyncio.create_task(self.handle_websocket_messages())

        while running:
            self.clock.tick(FPS)

            running = self.handle_events()
            self.update_movement()

            if self.game_state == GameState.MENU:
                self.draw_menu()
            elif self.game_state == GameState.LOGIN:
                self.draw_login()
            elif self.game_state == GameState.REGISTER:
                self.draw_register()
            elif self.game_state == GameState.PLAYING:
                self.draw_game()

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = DesktopGame()
    asyncio.run(game.run())