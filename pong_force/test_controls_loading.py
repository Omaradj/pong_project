# Test controls loading in actual game scenario
import pygame
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath('__file__')))

def main():
    """Test controls loading issue"""
    print("Testing Controls Loading Issue...")
    
    pygame.init()
    
    try:
        # Import GameLoop like main.py does
        from game.game_loop import GameLoop
        
        print("1. Creating GameLoop instance...")
        game = GameLoop()
        
        print("2. Testing load_custom_controls method...")
        game.load_custom_controls()
        print(f"   - Player 1 controls loaded: {game.custom_controls.get('player1', {}).get('vs_robot', {})}")
        
        print("3. Testing get_control_key method...")
        p1_up = game.get_control_key(1, "up")
        print(f"   - Player 1 up key: {p1_up} ({pygame.key.name(p1_up)})")
        
        print("4. Simulating AI mode setup...")
        game.ai_enabled = True
        game.game_state = 1  # STATE_PLAYING
        
        print("5. Controls should now be active in game")
        print("   - If DELETE key works, it should set running=False")
        print("   - Current running state:", game.running)
        
    except Exception as e:
        print(f"Error: {e}")
        
    pygame.quit()

if __name__ == "__main__":
    main()
