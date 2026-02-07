# ===== PONG FORCE - CONTROLS CONFIGURATION =====

import pygame
import sys
import json
import os
import config

class ControlsMenu:
    def __init__(self):
        """Initialize controls configuration menu"""
        pygame.init()
        
        # Create screen
        self.screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        pygame.display.set_caption(config.TITLE + " - Controls")
        
        # Menu state
        self.running = True
        self.selected_option = 0
        self.editing_player = None  # None, 1, or 2
        
        # Default controls
        self.controls = {
            "player1": {
                "multiplayer": {"up": "up", "down": "down", "force": "space"},
                "vs_robot": {"up": "up", "down": "down", "force": "space"},
                "two_player_local": {"up": "up", "down": "down", "force": "space"}
            },
            "player2": {
                "multiplayer": {"up": "w", "down": "s", "force": "shift"},
                "vs_robot": {"up": "w", "down": "s", "force": "shift"},
                "two_player_local": {"up": "z", "down": "s", "force": "a"}
            }
        }
        
        # Available keys
        self.available_keys = [
            "up", "down", "left", "right", "space", "shift",
            "w", "a", "s", "d", "z", "x", "c", "v",
            "q", "e", "r", "f", "g", "h", "y", "u", "i",
            "j", "k", "l", "m", "n", "b", "o", "p"
        ]
        
        # Colors
        self.bg_color = config.BLACK
        self.title_color = config.NEON_YELLOW
        self.selected_color = config.NEON_PINK
        self.normal_color = config.WHITE
        self.info_color = config.NEON_BLUE
        
        # Fonts
        self.title_font = pygame.font.Font(None, 48)
        self.option_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        
        # Clock
        self.clock = pygame.time.Clock()
        
        # Key mapping for display
        self.key_display_names = {
            "up": "↑", "down": "↓", "left": "←", "right": "→",
            "space": "SPACE", "shift": "SHIFT", "w": "W", "a": "A",
            "s": "S", "d": "D", "z": "Z", "x": "X", "c": "C",
            "v": "V", "q": "Q", "e": "E", "r": "R", "f": "F",
            "g": "G", "h": "H", "y": "Y", "u": "U", "i": "I",
            "j": "J", "k": "K", "l": "L", "m": "M", "n": "N",
            "b": "B", "o": "O", "p": "P"
        }
        
        # Load saved controls if exists
        self.load_controls()
        
    def load_controls(self):
        """Load controls from file if exists"""
        controls_file = "controls.json"
        if os.path.exists(controls_file):
            try:
                with open(controls_file, 'r') as f:
                    saved_controls = json.load(f)
                    self.controls.update(saved_controls)
                    print("✅ Controls loaded from file")
            except Exception as e:
                print(f"❌ Error loading controls: {e}")
    
    def save_controls(self):
        """Save controls to file"""
        controls_file = "controls.json"
        try:
            with open(controls_file, 'w') as f:
                json.dump(self.controls, f, indent=2)
                print("✅ Controls saved to file")
        except Exception as e:
            print(f"❌ Error saving controls: {e}")
    
    def run(self):
        """Run controls menu and return when done"""
        while self.running:
            self.handle_events()
            self.render()
            pygame.display.flip()
            self.clock.tick(60)
        
        # Save controls before exiting
        self.save_controls()
        return True
    
    def handle_events(self):
        """Handle menu events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if self.editing_player is None:
                    # Main menu navigation
                    if event.key == pygame.K_1 or event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % 4
                    elif event.key == pygame.K_3 or event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % 4
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        if self.selected_option == 0:  # Player 1 controls
                            self.editing_player = 1
                        elif self.selected_option == 1:  # Player 2 controls
                            self.editing_player = 2
                        elif self.selected_option == 2:  # Reset to defaults
                            self.reset_to_defaults()
                        elif self.selected_option == 3:  # Back
                            self.running = False
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                else:
                    # Editing controls - use +/- to navigate
                    if event.key == pygame.K_1 or event.key == pygame.K_LEFT:
                        self.selected_option = (self.selected_option - 1) % 3
                    elif event.key == pygame.K_3 or event.key == pygame.K_RIGHT:
                        self.selected_option = (self.selected_option + 1) % 3
                    else:
                        # Handle key assignment
                        self.handle_key_edit(event)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event)
    
    def handle_key_edit(self, event):
        """Handle key editing for player"""
        if event.key == pygame.K_ESCAPE or event.key == pygame.K_DELETE:
            self.editing_player = None
            return
        
        # Map pygame key to our control name
        key_name = self.pygame_key_to_name(event.key)
        if key_name and key_name in self.available_keys:
            if self.editing_player == 1:
                # Player 1 editing (applies to all modes)
                if self.selected_option == 0:  # Up
                    self.controls["player1"]["multiplayer"]["up"] = key_name
                    self.controls["player1"]["vs_robot"]["up"] = key_name
                    self.controls["player1"]["two_player_local"]["up"] = key_name
                elif self.selected_option == 1:  # Down
                    self.controls["player1"]["multiplayer"]["down"] = key_name
                    self.controls["player1"]["vs_robot"]["down"] = key_name
                    self.controls["player1"]["two_player_local"]["down"] = key_name
                elif self.selected_option == 2:  # Force
                    self.controls["player1"]["multiplayer"]["force"] = key_name
                    self.controls["player1"]["vs_robot"]["force"] = key_name
                    self.controls["player1"]["two_player_local"]["force"] = key_name
            
            elif self.editing_player == 2:
                # Player 2 editing (only applies to two_player_local mode)
                if self.selected_option == 0:  # Up
                    self.controls["player2"]["two_player_local"]["up"] = key_name
                elif self.selected_option == 1:  # Down
                    self.controls["player2"]["two_player_local"]["down"] = key_name
                elif self.selected_option == 2:  # Force
                    self.controls["player2"]["two_player_local"]["force"] = key_name
    
    def pygame_key_to_name(self, key):
        """Convert pygame key to our control name"""
        key_map = {
            pygame.K_UP: "up", pygame.K_DOWN: "down", pygame.K_LEFT: "left", pygame.K_RIGHT: "right",
            pygame.K_SPACE: "space", pygame.K_LSHIFT: "shift", pygame.K_RSHIFT: "shift",
            pygame.K_w: "w", pygame.K_a: "a", pygame.K_s: "s", pygame.K_d: "d",
            pygame.K_z: "z", pygame.K_x: "x", pygame.K_c: "c", pygame.K_v: "v",
            pygame.K_q: "q", pygame.K_e: "e", pygame.K_r: "r", pygame.K_f: "f",
            pygame.K_g: "g", pygame.K_h: "h", pygame.K_y: "y", pygame.K_u: "u",
            pygame.K_i: "i", pygame.K_j: "j", pygame.K_k: "k", pygame.K_l: "l",
            pygame.K_m: "m", pygame.K_n: "n", pygame.K_b: "b", pygame.K_o: "o",
            pygame.K_p: "p"
        }
        return key_map.get(key, "up")  # Default to UP if not found
    
    def handle_mouse_click(self, event):
        """Handle mouse click on control buttons"""
        mouse_x, mouse_y = event.pos
        
        # Define button areas (x, y, width, height)
        buttons = {
            "player1_up": (config.WINDOW_WIDTH//2 - 150, 200, 100, 40),
            "player1_down": (config.WINDOW_WIDTH//2 - 150, 250, 100, 40),
            "player1_force": (config.WINDOW_WIDTH//2 - 150, 300, 100, 40),
            "player2_up": (config.WINDOW_WIDTH//2 + 150, 200, 100, 40),
            "player2_down": (config.WINDOW_WIDTH//2 + 150, 250, 100, 40),
            "player2_force": (config.WINDOW_WIDTH//2 + 150, 300, 100, 40)
        }
        
        # Check which button was clicked
        for button_name, (x, y, w, h) in buttons.items():
            if x <= mouse_x <= x + w and y <= mouse_y <= y + h:
                if self.editing_player == 1:
                    # Player 1 button clicked
                    if button_name == "player1_up":
                        self.selected_option = 0  # Up
                    elif button_name == "player1_down":
                        self.selected_option = 1  # Down
                    elif button_name == "player1_force":
                        self.selected_option = 2  # Force
                elif self.editing_player == 2:
                    # Player 2 button clicked
                    if button_name == "player2_up":
                        self.selected_option = 0  # Up
                    elif button_name == "player2_down":
                        self.selected_option = 1  # Down
                    elif button_name == "player2_force":
                        self.selected_option = 2  # Force
    
    def reset_to_defaults(self):
        """Reset controls to default values"""
        self.controls = {
            "player1": {
                "multiplayer": {"up": "up", "down": "down", "force": "space"},
                "vs_robot": {"up": "up", "down": "down", "force": "space"},
                "two_player_local": {"up": "up", "down": "down", "force": "space"}
            },
            "player2": {
                "multiplayer": {"up": "w", "down": "s", "force": "shift"},
                "vs_robot": {"up": "w", "down": "s", "force": "shift"},
                "two_player_local": {"up": "z", "down": "s", "force": "a"}
            }
        }
        print("✅ Controls reset to defaults")
    
    def get_controls_for_mode(self, player, mode):
        """Get controls for specific player and mode"""
        return self.controls[f"player{player}"][mode]
    
    def render(self):
        """Render the controls menu"""
        self.screen.fill(self.bg_color)
        
        if self.editing_player is None:
            # Main menu
            self.render_main_menu()
        else:
            # Editing controls
            self.render_edit_menu()
    
    def render_main_menu(self):
        """Render main controls menu"""
        # Title
        title_text = "Controls Configuration"
        title_surface = self.title_font.render(title_text, True, self.title_color)
        title_rect = title_surface.get_rect(center=(config.WINDOW_WIDTH // 2, 80))
        self.screen.blit(title_surface, title_rect)
        
        # Menu options
        options = [
            "Configure Player 1 Controls",
            "Configure Player 2 Controls", 
            "Reset to Defaults",
            "Back to Main Menu"
        ]
        
        start_y = 180
        for i, option in enumerate(options):
            color = self.selected_color if i == self.selected_option else self.normal_color
            option_surface = self.option_font.render(option, True, color)
            option_rect = option_surface.get_rect(center=(config.WINDOW_WIDTH // 2, start_y + i * 50))
            self.screen.blit(option_surface, option_rect)
    
    def render_edit_menu(self):
        """Render control editing menu"""
        player_text = f"Player {self.editing_player} Controls"
        title_surface = self.title_font.render(player_text, True, self.title_color)
        title_rect = title_surface.get_rect(center=(config.WINDOW_WIDTH // 2, 60))
        self.screen.blit(title_surface, title_rect)
        
        # Show current controls for different modes
        modes = ["multiplayer", "vs_robot", "two_player_local"]
        mode_names = ["Multiplayer", "vs Robot", "2-Player Local"]
        
        start_y = 120
        for mode_idx, (mode, mode_name) in enumerate(zip(modes, mode_names)):
            controls = self.controls[f"player{self.editing_player}"][mode]
            
            # Mode name
            mode_surface = self.option_font.render(mode_name + ":", True, self.info_color)
            mode_rect = mode_surface.get_rect(center=(config.WINDOW_WIDTH // 2, start_y + mode_idx * 120))
            self.screen.blit(mode_surface, mode_rect)
            
            # Controls
            up_key = self.key_display_names.get(controls["up"], controls["up"].upper())
            down_key = self.key_display_names.get(controls["down"], controls["down"].upper())
            force_key = self.key_display_names.get(controls["force"], controls["force"].upper())
            
            controls_text = f"Up: {up_key}  Down: {down_key}  Force: {force_key}"
            controls_surface = self.small_font.render(controls_text, True, self.normal_color)
            controls_rect = controls_surface.get_rect(center=(config.WINDOW_WIDTH // 2, start_y + 30 + mode_idx * 120))
            self.screen.blit(controls_surface, controls_rect)
        
        # Instructions
        instructions = [
            "Use +/- to select control to change",
            "Press any key to assign to selected control",
            "Press ESC to finish editing"
        ]
        
        inst_y = config.WINDOW_HEIGHT - 120
        for instruction in instructions:
            inst_surface = self.small_font.render(instruction, True, config.GRAY)
            inst_rect = inst_surface.get_rect(center=(config.WINDOW_WIDTH // 2, inst_y))
            self.screen.blit(inst_surface, inst_rect)
            inst_y += 25
