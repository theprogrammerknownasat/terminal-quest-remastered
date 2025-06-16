#!/bin/bash

# Terminal Quest: Remastered Help Script
# Displays comprehensive help information

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

show_help() {
    cat << EOF
$(echo -e "${PURPLE}╔══════════════════════════════════════════════════════════╗${NC}")
$(echo -e "${PURPLE}║              TERMINAL QUEST: REMASTERED                  ║${NC}")
$(echo -e "${PURPLE}║                    Help Guide                            ║${NC}")
$(echo -e "${PURPLE}╚══════════════════════════════════════════════════════════╝${NC}")

$(echo -e "${CYAN}WHAT IS TERMINAL QUEST?${NC}")
Terminal Quest: Remastered is an educational adventure game that teaches
Linux command-line skills through an interactive story. Perfect for 
complete beginners who want to learn how computers really work!

$(echo -e "${CYAN}HOW TO PLAY:${NC}")
• Launch Terminal Quest from your applications menu
• Follow Shell's guidance through the story
• Learn commands by actually using them
• Explore your computer safely in the provided sandbox
• Progress from basic navigation to system administration

$(echo -e "${CYAN}GAME MODES:${NC}")

$(echo -e "${YELLOW}Tutorial Mode (First Time):${NC}")
• Complete guided learning experience
• Story-driven progression
• AI-powered safety system
• Dramatic visual effects and TTY switching
• 1-2 hours of content

$(echo -e "${YELLOW}Safe Terminal Mode (After Tutorial):${NC}")
• Practice environment with safety nets
• All learned commands available
• No story - just exploration
• Can reset tutorial anytime

$(echo -e "${CYAN}KEY FEATURES:${NC}")
• Learn 20+ essential Linux commands
• Understand computer hardware (CPU, RAM, GPU, storage)
• Explore the Linux operating system structure
• Practice in a safe, isolated environment
• AI-powered command analysis (with Ollama)
• ASCII art visualizations of computer components

$(echo -e "${CYAN}COMMANDS YOU'LL LEARN:${NC}")

$(echo -e "${YELLOW}Navigation:${NC}")          pwd, ls, cd, tree
$(echo -e "${YELLOW}File Operations:${NC}")     cat, less, head, tail, nano, touch, mkdir
$(echo -e "${YELLOW}System Information:${NC}")  free, df, ps, top, uname, lspci
$(echo -e "${YELLOW}Text Processing:${NC}")     grep, sort, wc, find
$(echo -e "${YELLOW}System Logs:${NC}")         journalctl, dmesg, systemctl status

$(echo -e "${CYAN}SAFETY FEATURES:${NC}")
• Sandbox environment for safe experimentation
• AI analysis of commands before execution
• Protection against dangerous system modifications
• Guidance away from risky operations
• Tutorial reset capability

$(echo -e "${CYAN}GETTING HELP:${NC}")
• In-game: Shell character provides guidance
• Commands: Type 'help' in Safe Terminal Mode
• Manual pages: Use 'man command_name' for any Linux command
• Reset: Use 'reset-tutorial' to start over

$(echo -e "${CYAN}TECHNICAL REQUIREMENTS:${NC}")
• Fedora Linux (or similar distribution)
• Python 3.6+
• Zenity (for visual effects)
• Optional: Ollama for AI features

$(echo -e "${CYAN}OLLAMA SETUP (OPTIONAL BUT RECOMMENDED):${NC}")
Ollama provides AI-powered command safety analysis:

1. Install Ollama: https://ollama.ai
2. Start service: ollama serve
3. Install model: ollama pull llama3.2:3b
4. Restart Terminal Quest

See OLLAMA_SETUP.md in the installation directory for detailed instructions.

$(echo -e "${CYAN}TROUBLESHOOTING:${NC}")

$(echo -e "${YELLOW}Game won't start:${NC}")
• Check that all files are in the installation directory
• Verify Python 3 and zenity are installed
• Try running directly: python3 /opt/terminal-quest/main.py

$(echo -e "${YELLOW}No visual effects:${NC}")
• Install zenity: sudo dnf install zenity
• Grant permission for TTY switching when prompted

$(echo -e "${YELLOW}AI features not working:${NC}")
• Install and start Ollama
• Check that localhost:11434 is accessible
• Game works fine without AI, just with basic safety

$(echo -e "${YELLOW}Stuck in tutorial:${NC}")
• Use 'exit' to leave safely
• Use 'reset-tutorial' to start over
• Press Ctrl+Alt+F1 to return to desktop if needed

$(echo -e "${CYAN}EDUCATIONAL PHILOSOPHY:${NC}")
Terminal Quest teaches through hands-on experience. Rather than just
reading about commands, you actually use them to solve problems and
advance the story. This builds muscle memory and confidence.

The game respects that you're intelligent but new to this domain. It
uses analogies and real-world comparisons to make technical concepts
accessible without being condescending.

$(echo -e "${CYAN}AFTER COMPLETING THE TUTORIAL:${NC}")
• Practice regularly in Safe Terminal Mode
• Explore the regular terminal (carefully!)
• Try more advanced tutorials and books
• Join Linux communities and forums
• Consider system administration or development paths

$(echo -e "${CYAN}CREDITS:${NC}")
Terminal Quest: Remastered is inspired by the original Terminal Quest
from Kano Computing. This version is expanded with modern AI features,
comprehensive hardware education, and enhanced safety systems.

$(echo -e "${GREEN}Ready to start your Linux adventure? Launch Terminal Quest now!${NC}")

EOF
}

# Display help based on argument or show full help
case "${1:-full}" in
    "quick"|"q")
        echo -e "${CYAN}Terminal Quest: Remastered - Quick Help${NC}"
        echo ""
        echo "Launch from applications menu or run:"
        echo "  /opt/terminal-quest/launch_terminal_quest.sh"
        echo ""
        echo "First time: Complete tutorial (1-2 hours)"
        echo "After tutorial: Safe practice mode available"
        echo ""
        echo "For full help: $0 full"
        ;;
    "commands"|"c")
        echo -e "${CYAN}Common Linux Commands You'll Learn:${NC}"
        echo ""
        echo -e "${YELLOW}Navigation:${NC}      pwd, ls, cd"
        echo -e "${YELLOW}Files:${NC}          cat, nano, touch, mkdir, cp, mv"
        echo -e "${YELLOW}System:${NC}         free, df, ps, top, uname"
        echo -e "${YELLOW}Search:${NC}         find, grep"
        echo -e "${YELLOW}Help:${NC}           man, help"
        ;;
    "full"|*)
        show_help
        ;;
esac