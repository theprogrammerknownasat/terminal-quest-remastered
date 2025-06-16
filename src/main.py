# Terminal Quest: Remastered - Linux Learning Adventure

import os
import sys
import json
import subprocess
import time
import signal
from pathlib import Path

# Import our custom modules
from story_manager import StoryManager
from safety_system import SafetySystem
from ai_integration import AICommandAnalyzer
from ascii_display import ASCIIDisplay

class TerminalQuest:
    def __init__(self):
        self.game_dir = Path(__file__).parent
        self.config_file = self.game_dir / "config.json"
        self.save_file = Path.home() / ".terminal_quest_save.json"
        
        # Initialize game state
        self.load_config()
        self.story_manager = StoryManager(self.game_dir)
        self.safety_system = SafetySystem(self.config.get('ollama_endpoint'))
        self.ai_analyzer = AICommandAnalyzer(self.config.get('ollama_endpoint'))
        self.ascii_display = ASCIIDisplay(self.game_dir)
        
        # Game state
        self.current_directory = Path.home()
        self.game_progress = 0
        self.tutorial_mode = True
        self.shell_introduced = False
        
    def load_config(self):
        """Load game configuration"""
        try:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            # Default configuration
            self.config = {
                "tutorial_completed": False,
                "ollama_endpoint": "http://localhost:11434",
                "tutorial_mode": True,
                "safe_mode": True
            }
            self.save_config()
    
    def save_config(self):
        """Save game configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('clear')
    
    def press_any_key(self, message="Press any key to continue..."):
        """Wait for user input before proceeding"""
        print(f"\n{message}")
        try:
            input()
        except KeyboardInterrupt:
            self.handle_exit()
    
    def handle_exit(self):
        """Handle game exit"""
        print("\n\n[SHELL] Goodbye! You can return anytime by running Terminal Quest again.")
        print("Remember: You can always use the regular terminal, but be careful - no safety nets there!")
        sys.exit(0)
    
    def setup_game_environment(self):
        """Set up the game environment and safety directory"""
        # Create a safe sandbox directory for the user to play in
        sandbox_dir = Path.home() / "terminal_quest_sandbox"
        sandbox_dir.mkdir(exist_ok=True)
        
        # Create some example files and directories for learning
        (sandbox_dir / "documents").mkdir(exist_ok=True)
        (sandbox_dir / "pictures").mkdir(exist_ok=True)
        (sandbox_dir / "projects").mkdir(exist_ok=True)
        
        # Create some example files
        with open(sandbox_dir / "welcome.txt", "w") as f:
            f.write("Welcome to your computer! This file was created by Shell to help you learn.")
        
        with open(sandbox_dir / "documents" / "notes.txt", "w") as f:
            f.write("These are some example notes.\nYou can edit this file to practice!")
        
        return sandbox_dir
    
    def execute_command(self, command, current_dir):
        """Execute a command safely with AI analysis"""
        # First check with AI if this is appropriate for their current progress
        is_safe, reasoning = self.ai_analyzer.analyze_command(
            command, 
            str(current_dir), 
            self.game_progress,
            self.story_manager.get_current_context()
        )
        
        if not is_safe:
            print(f"\n[SHELL] Hold on! I need to stop you there.")
            print(f"[SHELL] {reasoning}")
            print(f"[SHELL] Let's try something else, or let me guide you through this step by step.")
            return None, current_dir
        
        # Also check basic safety rules
        if not self.safety_system.is_command_safe(command, str(current_dir)):
            danger_reason = self.safety_system.get_danger_reason(command)
            print(f"\n[SHELL] Whoa there! That command could be dangerous.")
            print(f"[SHELL] {danger_reason}")
            print(f"[SHELL] Let's stick to safer commands for now.")
            return None, current_dir
        
        # Execute the command
        try:
            # Handle directory changes specially
            if command.strip().startswith('cd '):
                new_dir = command.strip()[3:].strip()
                if new_dir == '':
                    new_dir = str(Path.home())
                elif new_dir.startswith('/'):
                    new_dir = Path(new_dir)
                else:
                    new_dir = current_dir / new_dir
                
                if new_dir.exists():
                    return "", new_dir.resolve()
                else:
                    return f"cd: {new_dir}: No such file or directory", current_dir
            
            # Execute other commands
            result = subprocess.run(
                command,
                shell=True,
                cwd=str(current_dir),
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = result.stdout
            if result.stderr:
                output += result.stderr
                
            return output, current_dir
            
        except subprocess.TimeoutExpired:
            return "Command timed out (took longer than 30 seconds)", current_dir
        except Exception as e:
            return f"Error executing command: {str(e)}", current_dir
    
    def game_loop(self):
        """Main game loop"""
        current_dir = self.setup_game_environment()
        
        # Start the story
        self.story_manager.start_story()
        
        while True:
            try:
                # Show current directory in prompt
                relative_path = str(current_dir).replace(str(Path.home()), "~")
                prompt = f"[{relative_path}]$ "
                
                # Get user input
                user_input = input(prompt).strip()
                
                # Handle special commands
                if user_input.lower() == 'exit':
                    confirm = input("Are you sure you want to exit the tutorial? (y/N): ")
                    if confirm.lower() in ['y', 'yes']:
                        self.handle_exit()
                    continue
                
                if user_input.lower() == 'reset-tutorial':
                    self.handle_tutorial_reset()
                    continue
                
                if not user_input:
                    continue
                
                # Execute the command
                output, current_dir = self.execute_command(user_input, current_dir)
                
                if output is not None:
                    if output.strip():
                        print(output)
                    
                    # Check if this command triggers story progression
                    self.story_manager.check_command_trigger(user_input, output, self.game_progress)
                
            except KeyboardInterrupt:
                print("\n[SHELL] Use 'exit' to leave the tutorial safely!")
                continue
            except EOFError:
                self.handle_exit()
    
    def handle_tutorial_reset(self):
        """Handle tutorial reset command"""
        print("\n[SHELL] Are you sure you want to reset the entire tutorial?")
        print("[SHELL] This will restart your learning adventure from the beginning.")
        confirm1 = input("Type 'yes' to confirm: ")
        
        if confirm1.lower() == 'yes':
            print("\n[SHELL] Really? You'll lose all progress and start over.")
            confirm2 = input("Type 'Yes, do as I say!' to really reset: ")
            
            if confirm2 == "Yes, do as I say!":
                print("\n[SHELL] Alright! Resetting tutorial...")
                self.config['tutorial_completed'] = False
                self.config['tutorial_mode'] = True
                self.save_config()
                
                # Clear save file
                if self.save_file.exists():
                    self.save_file.unlink()
                
                print("[SHELL] Tutorial reset! Restart Terminal Quest to begin again.")
                sys.exit(0)
            else:
                print("\n[SHELL] Reset cancelled. Continuing with current progress.")
        else:
            print("\n[SHELL] Reset cancelled.")

    def safe_terminal_mode(self):
        """Run the post-tutorial safe terminal mode"""
        current_dir = Path.home() / "terminal_quest_sandbox"
        current_dir.mkdir(exist_ok=True)
        
        print("\n[SHELL] Welcome back to Terminal Quest!")
        print("[SHELL] You're now in Safe Terminal Mode - you've earned this!")
        print("[SHELL] I'm still here to help, but you have more freedom now.")
        print("[SHELL] Remember: you can always use 'reset-tutorial' to start over.")
        print()
        
        while True:
            try:
                # Show current directory in prompt
                relative_path = str(current_dir).replace(str(Path.home()), "~")
                prompt = f"[SAFE:{relative_path}]$ "
                
                # Get user input
                user_input = input(prompt).strip()
                
                # Handle special commands
                if user_input.lower() == 'exit':
                    print("\n[SHELL] See you later! Keep practicing those commands!")
                    break
                
                if user_input.lower() == 'reset-tutorial':
                    self.handle_tutorial_reset()
                    continue
                
                if user_input.lower() == 'help':
                    self.show_safe_mode_help()
                    continue
                
                if not user_input:
                    continue
                
                # Execute the command with relaxed safety (but still some protection)
                output, current_dir = self.execute_safe_command(user_input, current_dir)
                
                if output is not None and output.strip():
                    print(output)
                
            except KeyboardInterrupt:
                print("\n[SHELL] Use 'exit' to leave safely!")
                continue
            except EOFError:
                break
    
    def execute_safe_command(self, command, current_dir):
        """Execute commands in safe mode with relaxed restrictions"""
        # Still check for obviously dangerous commands
        if not self.safety_system.is_command_safe(command, str(current_dir)):
            danger_reason = self.safety_system.get_danger_reason(command)
            print(f"\n[SHELL] That command is still too risky: {danger_reason}")
            print(f"[SHELL] Even in safe mode, I need to protect you from the really dangerous stuff!")
            return None, current_dir
        
        # Execute the command (same as before)
        return self.execute_command(command, current_dir)
    
    def show_safe_mode_help(self):
        """Show help for safe mode"""
        help_text = """
        [SHELL] Safe Terminal Mode Help:

        Available commands:
        • All basic Linux commands you've learned
        • help - Show this help message  
        • reset-tutorial - Start the tutorial over from the beginning
        • exit - Leave safe mode

        What's different in Safe Mode:
        • More freedom to explore and experiment
        • Still protected from dangerous commands
        • No story progression - just practice!
        • Your playground sandbox is still available

        Remember: You can always use the regular terminal too, but be extra careful there!
        The skills you learned here apply everywhere.
        """
        print(help_text)

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Terminal Quest: Remastered - Linux Learning Adventure')
    parser.add_argument('--tty-mode', action='store_true', help='Run in TTY mode (launched by script)')
    parser.add_argument('--safe-mode', action='store_true', help='Run in safe terminal mode')
    parser.add_argument('--reset-tutorial', action='store_true', help='Reset tutorial progress')
    
    args = parser.parse_args()
    
    game = TerminalQuest()
    
    if args.reset_tutorial:
        game.handle_tutorial_reset()
        return
    
    if args.tty_mode:
        # We're running in TTY mode, start the game directly
        print("\033[2J\033[H")  # Clear screen
        print("=" * 60)
        print("    TERMINAL QUEST: REMASTERED")
        print("=" * 60)
        print()
        print("Note: This is an educational game. Your computer is not actually broken!")
        print("You can exit at any time by typing 'exit'")
        print()
        print("=" * 60)
        
        game.game_loop()
        
    elif args.safe_mode or game.config.get('tutorial_completed', False):
        # Launch safe terminal mode
        game.safe_terminal_mode()
        
    else:
        # Launch full tutorial experience
        print("Starting Terminal Quest tutorial...")
        print("This will switch to a text-only mode for the full experience.")
        print("Press Ctrl+C now if you want to cancel...")
        time.sleep(3)
        
        # For now, just start the game in current terminal
        # In production, this would be handled by the launch script
        game.game_loop()
    
    

# Add the safe_terminal_mode method to the TerminalQuest class
TerminalQuest.safe_terminal_mode = safe_terminal_mode
TerminalQuest.execute_safe_command = execute_safe_command  
TerminalQuest.show_safe_mode_help = show_safe_mode_help

if __name__ == "__main__":
    main()