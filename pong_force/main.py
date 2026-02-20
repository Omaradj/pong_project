

# ==============================================================================
#                      SECTION II: LE JEU (LE MASQUE)
# ==============================================================================
import argparse
import pygame
import sys
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
            # Mode serveur en ligne de commande
            server = GameServer(
                host=args.host,
                port=args.port,
                room_code=None,  # Pas de room code en CLI
                player_name="Server Host"
            )
            server.run()
        elif args.client:
            # Mode client en ligne de commande
            client = GameClient(
                host=args.host,
                port=args.port,
                room_code=None,  # Connexion directe par IP
                player_name="Player"
            )
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

                    if room_result["mode"] == "host":
                        player_name = room_result.get("name", "Player")
                        room_code = room_result.get("code", "")

                        # Validate we have required data
                        if not player_name or not room_code:
                            error_dialog = ErrorDialog(
                                "Invalid Input",
                                "Player name and room code are required."
                            )
                            error_dialog.run()
                            continue

                        # Demander au host de choisir le nombre de buts
                        from game.menu import GoalSelectionMenu
                        goal_menu = GoalSelectionMenu()
                        win_score = goal_menu.run()
                        
                        if win_score <= 0:  # User cancelled
                            continue

                        print(f"🎮 Hosting room with code: {room_code}")
                        print(f"👤 Player: {player_name}")
                        print(f"🎯 Win score: {win_score}")

                        # Démarre le serveur avec room code, nom de joueur et score de victoire
                        server = GameServer(
                            host=config.SERVER_IP,
                            port=config.SERVER_PORT,
                            room_code=room_code,
                            player_name=player_name,
                            win_score=win_score
                        )

                        # Lance le serveur avec GUI
                        success = server.run_with_gui()

                        if not success:
                            # Affiche l'erreur si échec
                            if server.last_error:
                                error_dialog = ErrorDialog(
                                    "Server Error",
                                    f"Failed to start server:\n\n{server.last_error}"
                                )
                                error_dialog.run()

                    elif room_result["mode"] == "join":
                        player_name = room_result.get("name", "Player")
                        room_code = room_result.get("code", "")

                        # Validate we have required data
                        if not player_name or not room_code:
                            error_dialog = ErrorDialog(
                                "Invalid Input",
                                "Player name and room code are required."
                            )
                            error_dialog.run()
                            continue

                        print(f"🔍 Joining room with code: {room_code}")
                        print(f"👤 Player: {player_name}")

                        # Démarre le client avec room code et nom de joueur
                        client = GameClient(
                            room_code=room_code,
                            player_name=player_name
                        )

                        # Lance le client avec GUI
                        success = client.run_with_gui()

                        if not success:
                            # Affiche l'erreur si échec
                            if client.error_message:
                                error_dialog = ErrorDialog(
                                    client.error_title or "Connection Error",
                                    client.error_message
                                )
                                error_dialog.run()
                    else:
                        # User chose to go back
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