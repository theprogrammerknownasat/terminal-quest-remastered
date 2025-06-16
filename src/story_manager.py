"""
Story Manager for Terminal Quest: Remastered
Handles story progression, tutorial content, and narrative flow
"""

import json
import os
import time
from pathlib import Path
from ascii_display import ASCIIDisplay

class StoryManager:
    def __init__(self, game_dir):
        self.game_dir = Path(game_dir)
        self.story_file = self.game_dir / "story_content.json"
        self.ascii_display = ASCIIDisplay(game_dir)
        
        # Story state
        self.current_chapter = 0
        self.current_section = 0
        self.story_progress = {}
        self.commands_learned = []
        
        # Load story content
        self.load_story_content()
    
    def load_story_content(self):
        """Load story content from JSON file"""
        try:
            with open(self.story_file, 'r') as f:
                self.story_data = json.load(f)
        except FileNotFoundError:
            print(f"Error: Could not find story content file at {self.story_file}")
            print("Please make sure story_content.json exists in the game directory.")
            raise
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('clear')
    
    def press_any_key(self, message="Press any key to continue..."):
        """Wait for user input before proceeding"""
        print(f"\n{message}")
        try:
            input()
        except KeyboardInterrupt:
            return False
        return True
    
    def display_text_with_pauses(self, text, clear_after=False):
        """Display text with pauses between paragraphs"""
        paragraphs = text.split('\n\n')
        
        for i, paragraph in enumerate(paragraphs):
            if paragraph.strip():
                print(paragraph.strip())
                
                # Add pause after each paragraph except the last
                if i < len(paragraphs) - 1:
                    if not self.press_any_key():
                        return False
                    print()  # Add spacing
        
        # Final pause
        if not self.press_any_key():
            return False
        
        if clear_after:
            self.clear_screen()
        
        return True
    
    def start_story(self):
        """Start the story from the beginning"""
        self.clear_screen()
        
        # Introduction sequence
        print("*" * 70)
        print("                    SYSTEM INITIALIZING...")
        print("*" * 70)
        time.sleep(2)
        
        print("\nLoading...")
        for i in range(3):
            time.sleep(1)
            print(".")
        
        self.clear_screen()
        
        # Show the "awakening" message
        intro_text = """
You slowly regain consciousness, your vision blurry and unfocused.
The familiar glow of your computer screen is gone, replaced by stark white text on a black background.

Something is very wrong.

Where is your desktop? Where are your icons? Where is... everything?

Suddenly, text begins to appear on the screen, as if someone is typing directly to you...
        """
        
        if not self.display_text_with_pauses(intro_text, clear_after=True):
            return
        
        # Shell's introduction
        self.introduce_shell()
    
    def introduce_shell(self):
        """Introduce the Shell character"""
        shell_intro = """
[SHELL] Hello there! You're finally awake.

[SHELL] Don't panic - I know this looks scary, but I'm here to help you.
My name is Shell, and I'm a part of your computer that you've never met before.

[SHELL] Something has happened to your computer's visual interface - what you might call the "desktop" with all the pretty icons and windows. A mysterious digital storm has corrupted it completely.

[SHELL] But don't worry! I can help you navigate your computer without all those visual elements. 
In fact, this might be the perfect opportunity to show you how computers REALLY work underneath all those pretty graphics.

[SHELL] The truth is, everything you can do with a mouse and clicking, you can do much more powerfully with words - with commands. I'll teach you how.

[SHELL] First things first - you need to learn how to talk to me. 
When you see the prompt with the $ symbol, that's me waiting for your instructions.
        """
        
        if not self.display_text_with_pauses(shell_intro):
            return
        
        # First command tutorial
        self.teach_first_commands()
    
    def teach_first_commands(self):
        """Teach the first basic commands"""
        print("\n" + "="*50)
        print("           LESSON 1: BASIC COMMUNICATION")
        print("="*50)
        
        lesson_text = """
[SHELL] Let's start with the most basic command: asking where you are.

[SHELL] In the visual world, you might see a folder icon and know you're in your "Documents" folder.
Here, we use a command called 'pwd' - which stands for "Print Working Directory".

[SHELL] Try typing: pwd

[SHELL] Go ahead, type 'pwd' and press Enter. I'll wait!
        """
        
        print(lesson_text)
        # The actual command execution will be handled by the main game loop
        # We just set up the expectation here
        
        self.current_chapter = 1
        self.current_section = 1
        self.story_progress['expecting_command'] = 'pwd'
        self.story_progress['lesson_context'] = 'first_pwd'
    
    def check_command_trigger(self, command, output, game_progress):
        """Check if a command triggers story progression"""
        expecting = self.story_progress.get('expecting_command')
        context = self.story_progress.get('lesson_context')
        
        if expecting and command.strip() == expecting:
            self.handle_expected_command(command, output, context)
        elif command.strip() in ['pwd', 'ls', 'cd', 'cat', 'nano', 'mkdir', 'touch']:
            self.acknowledge_command(command, output)
    
    def handle_expected_command(self, command, output, context):
        """Handle when the user enters an expected command"""
        if context == 'first_pwd':
            self.after_first_pwd(output)
        elif context == 'first_ls':
            self.after_first_ls(output)
        elif context == 'exploring_directories':
            self.continue_exploration()
        # Add more contexts as needed
    
    def after_first_pwd(self, output):
        """Response after the first pwd command"""
        response = f"""
[SHELL] Excellent! You can see that you're currently in: {output.strip()}

[SHELL] The 'pwd' command shows you your current location in the computer's file system.
Think of it like asking "Where am I?" in a big building.

[SHELL] Now let's see what's around you. The command 'ls' will list everything in your current location.
It's like looking around a room to see what's there.

[SHELL] Try typing: ls
        """
        
        print(response)
        self.story_progress['expecting_command'] = 'ls'
        self.story_progress['lesson_context'] = 'first_ls'
        self.commands_learned.append('pwd')
    
    def after_first_ls(self, output):
        """Response after the first ls command"""
        response = f"""
[SHELL] Great! You can see all the files and folders in your current location.

[SHELL] In the visual world, folders would appear as little folder icons, and files would have different icons based on their type. Here, we see their names directly.

[SHELL] Let's explore a bit. You can move into a different folder using the 'cd' command - which stands for "Change Directory".

[SHELL] I can see there's a folder called 'terminal_quest_sandbox' that I prepared for you to practice in.

[SHELL] Try typing: cd terminal_quest_sandbox
        """
        
        print(response)
        self.story_progress['expecting_command'] = 'cd terminal_quest_sandbox'
        self.story_progress['lesson_context'] = 'exploring_directories'
        self.commands_learned.append('ls')
    
    def continue_exploration(self):
        """Continue the exploration phase"""
        response = """
[SHELL] Perfect! You've moved into the practice area I set up for you.

[SHELL] Notice how your prompt changed? It now shows you're in the terminal_quest_sandbox folder.

[SHELL] Let's look around this new location. Try 'ls' again to see what's here.
        """
        
        print(response)
        self.story_progress['expecting_command'] = None  # Free exploration for now
        self.commands_learned.append('cd')
        
        # Start the next phase of learning
        self.begin_system_exploration()
    
    def begin_system_exploration(self):
        """Begin teaching about the computer system"""
        time.sleep(2)
        
        system_intro = """
[SHELL] You're doing great! You're already navigating like a pro.

[SHELL] But I'm starting to realize something... you seem completely new to all of this.
Have you ever used a computer like this before?

[SHELL] Actually, let me ask you something more important: 
Do you know what a computer actually IS? I mean, really, truly know what's inside this machine you're using?

[SHELL] I think before we go any further, I should show you around your own computer.
After all, how can you fix something if you don't know how it works?

[SHELL] Let me show you what's inside this magical box...
        """
        
        if not self.display_text_with_pauses(system_intro, clear_after=True):
            return
        
        self.show_computer_components()
    
    def show_computer_components(self):
        """Show and explain computer components"""
        print("="*60)
        print("              COMPUTER EXPLORATION")
        print("="*60)
        print()
        
        # CPU Section
        cpu_text = """
[SHELL] Let's start with the brain of your computer - the CPU (Central Processing Unit).

[SHELL] Your computer has an Intel Core i7 3rd generation processor.
Think of the CPU like the conductor of an orchestra - it coordinates everything else and does the actual "thinking".

[SHELL] Every single thing you do - clicking, typing, running programs - gets processed by this little chip no bigger than a postage stamp!
        """
        
        if not self.display_text_with_pauses(cpu_text):
            return
        
        # Show CPU ASCII art
        self.ascii_display.show_component("cpu")
        
        # Continue with other components...
        self.show_memory_components()
    
    def show_memory_components(self):
        """Show memory components"""
        memory_text = """
[SHELL] Next, let's talk about your computer's memory - the RAM (Random Access Memory).

[SHELL] You have 16 gigabytes of DDR3 RAM. Think of RAM like your desk workspace.
The bigger your desk, the more projects you can have spread out and work on at the same time.

[SHELL] When you open a program, it gets loaded from storage into RAM so the CPU can work with it quickly.
It's like taking a book from a bookshelf and putting it on your desk to read.

[SHELL] Let me check your memory right now...
        """
        
        if not self.display_text_with_pauses(memory_text):
            return
        
        # Show memory ASCII art
        self.ascii_display.show_component("memory")
        
        print("\n[SHELL] Try this command to see your memory: free -h")
        self.story_progress['expecting_command'] = 'free -h'
        self.story_progress['lesson_context'] = 'memory_check'
    
    def acknowledge_command(self, command, output):
        """Acknowledge when the user tries commands on their own"""
        acknowledgments = {
            'pwd': "[SHELL] Good! You're checking where you are. That's always smart.",
            'ls': "[SHELL] Excellent! Always good to see what's around you.",
            'cd': "[SHELL] Nice navigation! You're getting comfortable moving around.",
            'cat': "[SHELL] Reading files directly - you're becoming quite the explorer!",
            'nano': "[SHELL] Ah, editing files! That's getting more advanced.",
            'mkdir': "[SHELL] Creating directories? You're really taking control now!",
            'touch': "[SHELL] Creating files! You're becoming quite the computer user."
        }
        
        base_command = command.split()[0]
        if base_command in acknowledgments:
            print(f"\n{acknowledgments[base_command]}")
    
    def get_current_context(self):
        """Get current story context for AI analysis"""
        return {
            'chapter': self.current_chapter,
            'section': self.current_section,
            'commands_learned': self.commands_learned,
            'lesson_context': self.story_progress.get('lesson_context', 'general'),
            'expecting_command': self.story_progress.get('expecting_command')
        }
    
    def get_commands_for_level(self, level):
        """Get appropriate commands for the current learning level"""
        command_progression = {
            1: ['pwd', 'ls', 'cd'],
            2: ['cat', 'less', 'head', 'tail'],
            3: ['mkdir', 'touch', 'cp', 'mv'],
            4: ['nano', 'grep', 'find'],
            5: ['chmod', 'chown', 'ps', 'top'],
            6: ['systemctl', 'journalctl', 'lspci', 'lsusb']
        }
        
        allowed_commands = []
        for i in range(1, level + 1):
            allowed_commands.extend(command_progression.get(i, []))
        
        return allowed_commands