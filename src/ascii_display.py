"""
ASCII Display System for Terminal Quest: Remastered
Handles loading and displaying ASCII art for computer components
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional

class ASCIIDisplay:
    def __init__(self, game_dir: Path):
        self.game_dir = Path(game_dir)
        self.ascii_file = self.game_dir / "ascii_art.json"
        self.ascii_art = {}
        
        # Load ASCII art
        self.load_ascii_art()
    
    def load_ascii_art(self):
        """Load ASCII art from JSON file"""
        try:
            with open(self.ascii_file, 'r') as f:
                self.ascii_art = json.load(f)
        except FileNotFoundError:
            print(f"Warning: ASCII art file not found at {self.ascii_file}")
            print("Creating placeholder ASCII art file...")
            self.create_placeholder_ascii()
            self.save_ascii_art()
    
    def create_placeholder_ascii(self):
        """Create placeholder ASCII art for all components"""
        self.ascii_art = {
            "cpu": {
                "art": [
                    "╔══════════════════════════════════════════════════════════╗",
                    "║                    CPU - PLACEHOLDER                     ║",
                    "║                                                          ║",
                    "║        [REPLACE WITH JPEG-TO-ASCII CONVERSION]           ║",
                    "║                                                          ║",
                    "║     Dimensions: ~60 characters wide, ~15 lines tall     ║",
                    "║                                                          ║",
                    "║              Intel Core i7 3rd Generation               ║",
                    "║                                                          ║",
                    "╚══════════════════════════════════════════════════════════╝"
                ],
                "caption": "This is your CPU - the brain of your computer! Every calculation, every decision, every program runs through this tiny chip."
            },
            
            "memory": {
                "art": [
                    "╔══════════════════════════════════════════════════════════╗",
                    "║                   MEMORY - PLACEHOLDER                   ║",
                    "║                                                          ║",
                    "║        [REPLACE WITH JPEG-TO-ASCII CONVERSION]           ║",
                    "║                                                          ║",
                    "║     Dimensions: ~60 characters wide, ~15 lines tall     ║",
                    "║                                                          ║",
                    "║                 16GB DDR3 RAM Sticks                     ║",
                    "║                                                          ║",
                    "╚══════════════════════════════════════════════════════════╝"
                ],
                "caption": "This is your RAM memory! Think of it as your computer's workspace - the bigger it is, the more things you can work on at once."
            },
            
            "gpu": {
                "art": [
                    "╔══════════════════════════════════════════════════════════╗",
                    "║                    GPU - PLACEHOLDER                     ║",
                    "║                                                          ║",
                    "║        [REPLACE WITH JPEG-TO-ASCII CONVERSION]           ║",
                    "║                                                          ║",
                    "║     Dimensions: ~60 characters wide, ~15 lines tall     ║",
                    "║                                                          ║",
                    "║               NVIDIA GeForce GTX 1650                    ║",
                    "║                                                          ║",
                    "╚══════════════════════════════════════════════════════════╝"
                ],
                "caption": "This is your graphics card! It handles all the visual processing - from displaying this text to rendering games and videos."
            },
            
            "storage": {
                "art": [
                    "╔══════════════════════════════════════════════════════════╗",
                    "║                  STORAGE - PLACEHOLDER                   ║",
                    "║                                                          ║",
                    "║        [REPLACE WITH JPEG-TO-ASCII CONVERSION]           ║",
                    "║                                                          ║",
                    "║     Dimensions: ~60 characters wide, ~15 lines tall     ║",
                    "║                                                          ║",
                    "║            500GB SSD + 2TB HDD Storage                   ║",
                    "║                                                          ║",
                    "╚══════════════════════════════════════════════════════════╝"
                ],
                "caption": "These are your storage drives! The SSD is super fast for your operating system and programs, while the HDD gives you lots of space for files."
            },
            
            "motherboard": {
                "art": [
                    "╔══════════════════════════════════════════════════════════╗",
                    "║                MOTHERBOARD - PLACEHOLDER                 ║", 
                    "║                                                          ║",
                    "║        [REPLACE WITH JPEG-TO-ASCII CONVERSION]           ║",
                    "║                                                          ║",
                    "║     Dimensions: ~60 characters wide, ~15 lines tall     ║",
                    "║                                                          ║",
                    "║           The Foundation That Connects Everything         ║",
                    "║                                                          ║",
                    "╚══════════════════════════════════════════════════════════╝"
                ],
                "caption": "This is your motherboard - the foundation that connects all your computer parts together, like the nervous system of your computer."
            },
            
            "power_supply": {
                "art": [
                    "╔══════════════════════════════════════════════════════════╗",
                    "║               POWER SUPPLY - PLACEHOLDER                 ║",
                    "║                                                          ║",
                    "║        [REPLACE WITH JPEG-TO-ASCII CONVERSION]           ║",
                    "║                                                          ║",
                    "║     Dimensions: ~60 characters wide, ~15 lines tall     ║",
                    "║                                                          ║",
                    "║              Converts AC Power to DC Power               ║",
                    "║                                                          ║",
                    "╚══════════════════════════════════════════════════════════╝"
                ],
                "caption": "This is your power supply! It converts the AC electricity from your wall outlet into the DC power that your computer components need."
            },
            
            "computer_overview": {
                "art": [
                    "╔══════════════════════════════════════════════════════════╗",
                    "║              COMPLETE COMPUTER - PLACEHOLDER             ║",
                    "║                                                          ║",
                    "║        [REPLACE WITH JPEG-TO-ASCII CONVERSION]           ║",
                    "║                                                          ║",
                    "║     Dimensions: ~60 characters wide, ~20 lines tall     ║",
                    "║                                                          ║",
                    "║            Your Desktop Computer - All Together          ║",
                    "║                                                          ║",
                    "║  CPU + RAM + GPU + Storage + Motherboard + PSU = Magic! ║",
                    "║                                                          ║",
                    "╚══════════════════════════════════════════════════════════╝"
                ],
                "caption": "Here's your complete computer system! All these components work together in harmony to create the amazing machine you're learning on right now."
            }
        }
    
    def save_ascii_art(self):
        """Save ASCII art to JSON file"""
        with open(self.ascii_file, 'w') as f:
            json.dump(self.ascii_art, f, indent=2)
    
    def show_component(self, component_name: str, clear_before: bool = False, press_key_after: bool = True):
        """Display ASCII art for a specific component"""
        if clear_before:
            os.system('clear')
        
        if component_name not in self.ascii_art:
            print(f"[ASCII] Component '{component_name}' not found in ASCII art database")
            return
        
        component = self.ascii_art[component_name]
        
        # Display the ASCII art
        print()
        for line in component["art"]:
            print(line)
        print()
        
        # Display the caption
        if "caption" in component:
            print(f"[SHELL] {component['caption']}")
        
        if press_key_after:
            self.press_any_key()
    
    def show_multiple_components(self, component_names: list, clear_between: bool = True):
        """Display multiple components in sequence"""
        for i, component_name in enumerate(component_names):
            if clear_between and i > 0:
                os.system('clear')
            
            self.show_component(component_name, clear_before=False, press_key_after=True)
    
    def press_any_key(self, message="Press any key to continue..."):
        """Wait for user input before proceeding"""
        print(f"\n{message}")
        try:
            input()
        except KeyboardInterrupt:
            return False
        return True
    
    def get_component_list(self) -> list:
        """Get list of available components"""
        return list(self.ascii_art.keys())
    
    def add_component(self, name: str, art_lines: list, caption: str):
        """Add a new component to the ASCII art database"""
        self.ascii_art[name] = {
            "art": art_lines,
            "caption": caption
        }
        self.save_ascii_art()
    
    def update_component(self, name: str, art_lines: list = None, caption: str = None):
        """Update an existing component"""
        if name in self.ascii_art:
            if art_lines is not None:
                self.ascii_art[name]["art"] = art_lines
            if caption is not None:
                self.ascii_art[name]["caption"] = caption
            self.save_ascii_art()
            print(f"[ASCII] Updated component: {name}")
        else:
            print(f"[ASCII] Component '{name}' not found")
    
    def create_art_template(self, width: int = 60, height: int = 15) -> list:
        """Create a template for ASCII art with specified dimensions"""
        template = []
        border_char = "║"
        
        # Top border
        template.append("╔" + "═" * (width - 2) + "╗")
        
        # Content lines
        for i in range(height - 2):
            if i == 0:
                title_line = "COMPONENT NAME - PLACEHOLDER"
                padding = (width - 2 - len(title_line)) // 2
                line = border_char + " " * padding + title_line + " " * (width - 2 - padding - len(title_line)) + border_char
            elif i == 2:
                instruction = "[REPLACE WITH JPEG-TO-ASCII CONVERSION]"
                padding = (width - 2 - len(instruction)) // 2
                line = border_char + " " * padding + instruction + " " * (width - 2 - padding - len(instruction)) + border_char
            elif i == 4:
                dimensions = f"Dimensions: ~{width} characters wide, ~{height} lines tall"
                padding = (width - 2 - len(dimensions)) // 2
                line = border_char + " " * padding + dimensions + " " * (width - 2 - padding - len(dimensions)) + border_char
            else:
                line = border_char + " " * (width - 2) + border_char
            template.append(line)
        
        # Bottom border
        template.append("╚" + "═" * (width - 2) + "╝")
        
        return template
    
    def display_instructions(self):
        """Display instructions for creating ASCII art"""
        instructions = """
╔══════════════════════════════════════════════════════════════════╗
║                      ASCII ART INSTRUCTIONS                     ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  To add your custom ASCII art:                                   ║
║                                                                  ║
║  1. Take photos of each computer component                       ║
║  2. Use an online JPEG to ASCII converter                        ║
║  3. Recommended size: ~60 characters wide, ~15-20 lines tall     ║
║  4. Edit the ascii_art.json file                                 ║
║  5. Replace the placeholder art arrays with your converted ASCII ║
║  6. Update captions to match your specific components            ║
║                                                                  ║
║  Components to photograph:                                       ║
║  - CPU (Intel Core i7 3rd gen)                                  ║
║  - RAM (16GB DDR3 sticks)                                        ║
║  - GPU (GTX 1650)                                                ║
║  - Storage drives (500GB SSD + 2TB HDD)                         ║
║  - Motherboard                                                   ║
║  - Power supply                                                  ║
║  - Complete assembled computer                                   ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

For best results with ASCII conversion:
- Use good lighting and clear photos
- Crop images to focus on the component
- Try different ASCII conversion settings for clarity
- Test how the ASCII looks in your terminal

The current placeholders show you the exact format needed.
"""
        print(instructions)