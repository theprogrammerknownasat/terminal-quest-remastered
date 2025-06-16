# Terminal Quest: Remastered

An educational Linux adventure game designed to teach complete beginners how to use the command line and understand computer systems.

## Overview

Terminal Quest: Remastered is a story-driven game that introduces newcomers to Linux through an interactive narrative. Players work with "Shell," an AI character, to solve a mysterious computer problem while learning essential command-line skills.

### Key Features

- **Story-Driven Learning**: Learn through an engaging narrative about fixing a "corrupted" computer
- **Progressive Difficulty**: Start with basic navigation, advance to system administration
- **AI-Powered Safety**: Uses Ollama for intelligent command analysis and protection
- **Hardware Education**: Learn about CPU, RAM, GPU, storage, and how they work together
- **Safe Environment**: Protected sandbox prevents dangerous operations
- **Visual Effects**: Dramatic startup sequence with TTY switching for immersion
- **Post-Tutorial Mode**: Safe practice environment after completing the story

## Installation

### Prerequisites

**Required:**
- Fedora Linux 42 (or compatible distribution)
- Python 3.6+
- zenity (for visual effects)

**Optional but Recommended:**
- Ollama (for AI-powered safety features)

### Quick Install

1. Clone or download the game files to a directory
2. Run the installation script:
   ```bash
   sudo ./install.sh
   ```
3. Launch from applications menu or run:
   ```bash
   /opt/terminal-quest/launch_terminal_quest.sh
   ```

### Manual Installation

1. Copy all Python files to your desired location
2. Make scripts executable: `chmod +x *.sh *.py`
3. Install dependencies: `sudo dnf install python3 python3-requests zenity`
4. Optionally set up Ollama (see OLLAMA_SETUP.md)

## Game Structure

### Files Overview

- **main.py** - Core game engine and command handling
- **story_manager.py** - Story progression and tutorial content
- **ai_integration.py** - Ollama integration for command analysis
- **safety_system.py** - Basic safety checks and dangerous command blocking
- **ascii_display.py** - ASCII art system for computer components
- **story_content.json** - All narrative text and tutorial content
- **ascii_art.json** - ASCII art storage (customize with your own!)
- **launch_terminal_quest.sh** - Main launcher with visual effects
- **install.sh** - Installation script
- **config.json** - Game configuration and progress tracking

### Game Flow

1. **Dramatic Opening**: Visual effects simulate system corruption
2. **Shell Introduction**: Meet your AI guide and learn basic communication
3. **Command Learning**: Progressive tutorial through essential Linux commands
4. **Hardware Exploration**: Learn about computer components with ASCII art
5. **System Investigation**: Use learned skills to "diagnose" the problem
6. **The Revelation**: Discover the truth about Shell's educational deception
7. **Safe Mode**: Continue practicing in a protected environment

## Customization

### Adding Your Own ASCII Art

1. Take high-quality photos of computer components:
   - CPU (Intel Core i7 3rd gen)
   - RAM sticks (16GB DDR3)
   - Graphics card (GTX 1650)
   - Storage drives (SSD + HDD)
   - Motherboard
   - Power supply
   - Complete assembled computer

2. Convert photos to ASCII using online converters

3. Edit `ascii_art.json` and replace placeholder art arrays

4. Recommended dimensions: ~60 characters wide, ~15-20 lines tall

### Modifying Story Content

Edit `story_content.json` to customize:
- Narrative text and dialogue
- Tutorial progression
- Command explanations
- Character personality

### Configuring Safety Settings

Edit `safety_system.py` to adjust:
- Dangerous command patterns
- Safe directory restrictions
- Educational command progression
- Error messages and guidance

## Ollama Integration

### Setup

1. Install Ollama: https://ollama.ai
2. Start the service: `ollama serve`
3. Pull a recommended model: `ollama pull llama3.2:3b`

### Configuration

The game uses `http://localhost:11434` by default. To change:

1. Edit `config.json`
2. Update the `ollama_endpoint` field
3. Restart Terminal Quest

### Remote Setup (Advanced)

For remote Ollama servers through Cloudflare tunnels:

1. Set up cloudflared tunnel
2. Configure tunnel to forward to your Ollama server
3. Update `config.json` with tunnel URL

See `OLLAMA_SETUP.md` for detailed instructions.

### Model Recommendations

- **llama3.2:3b** - Fast and efficient (recommended)
- **qwen2.5:7b** - More capable but slower
- **phi3:mini** - Microsoft's efficient model

## Educational Philosophy

Terminal Quest teaches through **experiential learning**:

- **Learn by doing**: Actually execute commands rather than just reading about them
- **Contextual teaching**: Commands are introduced when needed for story progression
- **Progressive complexity**: Start simple, build to advanced concepts
- **Safe experimentation**: Protected environment encourages exploration
- **Real-world analogies**: Technical concepts explained through familiar comparisons

### Skills Taught

**Basic Navigation:**
- `pwd`, `ls`, `cd` - Understanding file system hierarchy
- Directory structure and path concepts

**File Operations:**
- `cat`, `less`, `head`, `tail` - Reading files
- `nano` - Text editing
- `touch`, `mkdir`, `cp`, `mv` - Creating and organizing

**System Information:**
- `free`, `df` - Memory and storage monitoring
- `ps`, `top` - Process management
- `uname`, `lspci` - Hardware identification

**Advanced Concepts:**
- `systemctl`, `journalctl` - System service management
- `grep`, `find` - Text searching and file location
- Kernel, operating system architecture
- Hardware components and their functions

## Safety Features

### Multi-Layer Protection

1. **Global Blacklist**: Known dangerous commands blocked universally
2. **Context Analysis**: Commands evaluated based on current directory and progress
3. **AI Analysis**: Ollama evaluates command safety and educational appropriateness
4. **Sandbox Environment**: Dedicated practice area isolated from system files
5. **Progressive Permissions**: More commands unlocked as skills develop

### Dangerous Patterns Blocked

- File system destruction (`rm -rf`, `dd`, `mkfs`)
- System modification (`chmod 777 /`, `chown root`)
- Network exploitation (`curl | sh`, malicious downloads)
- Process interference (`killall`, signal bombing)
- Privilege escalation (dangerous `sudo` usage)
- Resource exhaustion (fork bombs, infinite loops)

## Troubleshooting

### Common Issues

**Game won't start:**
- Verify Python 3 installation: `python3 --version`
- Install zenity: `sudo dnf install zenity`
- Check file permissions: `chmod +x launch_terminal_quest.sh`

**No visual effects:**
- Install zenity for popup windows
- Grant sudo access when prompted for TTY switching

**AI features not working:**
- Install and start Ollama: `ollama serve`
- Verify accessibility: `curl http://localhost:11434/api/tags`
- Game functions with basic safety if AI unavailable

**Stuck in tutorial:**
- Type `exit` to leave safely
- Use `reset-tutorial` command to restart
- Press `Ctrl+Alt+F1` to return to desktop

### Getting Help

- **In-game**: Shell character provides contextual guidance
- **Commands**: Type `help` in Safe Terminal Mode
- **Documentation**: Use `man command_name` for detailed command info
- **Reset**: Use `reset-tutorial` to start the adventure over

## Development Notes

### Architecture

The game uses a modular architecture:

- **Game Engine** (`main.py`): Command execution, safety integration, user interface
- **Story Manager**: Narrative progression, tutorial content, character responses
- **AI Integration**: Ollama communication, prompt engineering, response parsing
- **Safety System**: Multi-layer command analysis and protection
- **Display System**: ASCII art rendering, visual presentation

### Extending the Game

To add new content:

1. **New Commands**: Add to `story_content.json` tutorials section
2. **Story Chapters**: Extend the chapters object with new sections
3. **Safety Rules**: Update patterns in `safety_system.py`
4. **AI Prompts**: Modify prompt templates in `ai_integration.py`
5. **Visual Elements**: Add ASCII art to `ascii_art.json`

### Contributing

Contributions welcome! Focus areas:

- Additional tutorial content
- Improved safety analysis
- Better ASCII art
- Accessibility features
- Support for other distributions

## Credits

Inspired by the original Terminal Quest from Kano Computing. This remastered version adds:

- Modern AI-powered safety analysis
- Comprehensive hardware education
- Enhanced visual presentation
- Advanced safety systems
- Post-tutorial practice environment

## License

Educational use encouraged. Modify and distribute freely for learning purposes.

---

**Ready to start your Linux adventure?**

Launch Terminal Quest: Remastered and discover the power hidden beneath your computer's graphical interface!