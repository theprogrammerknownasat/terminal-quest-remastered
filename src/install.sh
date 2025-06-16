#!/bin/bash

# Terminal Quest: Remastered Installation Script
# Installs the game system-wide for easy access

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

INSTALL_DIR="/opt/terminal-quest"
DESKTOP_FILE_DIR="/usr/share/applications"
LOCAL_DESKTOP_DIR="$HOME/.local/share/applications"

print_banner() {
    echo -e "${PURPLE}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║              TERMINAL QUEST: REMASTERED                  ║${NC}"
    echo -e "${PURPLE}║                Installation Script                       ║${NC}"
    echo -e "${PURPLE}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

check_dependencies() {
    echo -e "${CYAN}[INFO] Checking dependencies...${NC}"
    
    local missing_deps=()
    
    # Check for required commands
    command -v python3 >/dev/null 2>&1 || missing_deps+=("python3")
    command -v zenity >/dev/null 2>&1 || missing_deps+=("zenity")
    
    # Check for Python modules
    python3 -c "import requests" 2>/dev/null || missing_deps+=("python3-requests")
    python3 -c "import json" 2>/dev/null || echo "JSON module available"
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        echo -e "${RED}[ERROR] Missing required dependencies:${NC}"
        printf ' - %s\n' "${missing_deps[@]}"
        echo ""
        echo -e "${YELLOW}On Fedora, install with:${NC}"
        echo "sudo dnf install python3 python3-requests zenity"
        echo ""
        echo -e "${YELLOW}On Ubuntu/Debian, install with:${NC}"
        echo "sudo apt install python3 python3-requests zenity"
        exit 1
    fi
    
    echo -e "${GREEN}[SUCCESS] All dependencies satisfied${NC}"
}

check_ollama_setup() {
    echo -e "${CYAN}[INFO] Checking Ollama setup...${NC}"
    
    if command -v ollama >/dev/null 2>&1; then
        echo -e "${GREEN}[INFO] Ollama is installed${NC}"
        
        # Check if Ollama is running
        if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
            echo -e "${GREEN}[INFO] Ollama server is running${NC}"
        else
            echo -e "${YELLOW}[WARNING] Ollama is installed but not running${NC}"
            echo -e "${YELLOW}[INFO] Start it with: ollama serve${NC}"
        fi
    else
        echo -e "${YELLOW}[WARNING] Ollama is not installed${NC}"
        echo -e "${YELLOW}[INFO] The game will work with basic safety only${NC}"
        echo -e "${YELLOW}[INFO] To get AI-powered safety, install Ollama from https://ollama.ai${NC}"
    fi
}

create_install_directory() {
    echo -e "${CYAN}[INFO] Creating installation directory...${NC}"
    
    if [ "$EUID" -eq 0 ]; then
        # Running as root - install system-wide
        mkdir -p "$INSTALL_DIR"
        echo -e "${GREEN}[SUCCESS] Created system installation directory: $INSTALL_DIR${NC}"
    else
        # Running as user - install locally
        INSTALL_DIR="$HOME/.local/share/terminal-quest"
        mkdir -p "$INSTALL_DIR"
        echo -e "${GREEN}[SUCCESS] Created user installation directory: $INSTALL_DIR${NC}"
    fi
}

copy_game_files() {
    echo -e "${CYAN}[INFO] Copying game files...${NC}"
    
    # List of files to copy
    local files=(
        "main.py"
        "story_manager.py"
        "ai_integration.py"
        "safety_system.py"
        "ascii_display.py"
        "story_content.json"
        "ascii_art.json"
        "launch_terminal_quest.sh"
        "config.json"
    )
    
    for file in "${files[@]}"; do
        if [ -f "$file" ]; then
            cp "$file" "$INSTALL_DIR/"
            echo -e "${GREEN}  ✓ Copied $file${NC}"
        else
            echo -e "${YELLOW}  ! Missing $file (creating placeholder)${NC}"
            
            # Create basic placeholder files if missing
            case "$file" in
                "config.json")
                    cat > "$INSTALL_DIR/$file" << 'EOF'
{
  "tutorial_completed": false,
  "ollama_endpoint": "http://localhost:11434",
  "tutorial_mode": true,
  "safe_mode": true
}
EOF
                    ;;
                "ascii_art.json")
                    echo '{}' > "$INSTALL_DIR/$file"
                    ;;
            esac
        fi
    done
    
    # Make scripts executable
    chmod +x "$INSTALL_DIR/launch_terminal_quest.sh" 2>/dev/null || true
    chmod +x "$INSTALL_DIR/main.py" 2>/dev/null || true
}

create_desktop_entry() {
    echo -e "${CYAN}[INFO] Creating desktop entry...${NC}"
    
    local desktop_content="[Desktop Entry]
Version=1.0
Type=Application
Name=Terminal Quest: Remastered
GenericName=Linux Learning Adventure
Comment=Learn Linux commands through an interactive adventure game
Icon=utilities-terminal
Exec=$INSTALL_DIR/launch_terminal_quest.sh
Terminal=false
Categories=Education;System;
Keywords=linux;terminal;education;learning;commands;shell;tutorial;
StartupNotify=true

[Desktop Action SafeMode]
Name=Safe Terminal Mode
Exec=$INSTALL_DIR/launch_terminal_quest.sh --safe-mode
Icon=utilities-terminal

[Desktop Action Tutorial]
Name=Restart Tutorial
Exec=$INSTALL_DIR/launch_terminal_quest.sh --reset-tutorial
Icon=help-about"

    if [ "$EUID" -eq 0 ]; then
        # System-wide installation
        echo "$desktop_content" > "$DESKTOP_FILE_DIR/terminal-quest.desktop"
        chmod 644 "$DESKTOP_FILE_DIR/terminal-quest.desktop"
        echo -e "${GREEN}[SUCCESS] Created system desktop entry${NC}"
    else
        # User installation
        mkdir -p "$LOCAL_DESKTOP_DIR"
        echo "$desktop_content" > "$LOCAL_DESKTOP_DIR/terminal-quest.desktop"
        chmod 644 "$LOCAL_DESKTOP_DIR/terminal-quest.desktop"
        echo -e "${GREEN}[SUCCESS] Created user desktop entry${NC}"
    fi
}

create_uninstaller() {
    echo -e "${CYAN}[INFO] Creating uninstaller...${NC}"
    
    cat > "$INSTALL_DIR/uninstall.sh" << EOF
#!/bin/bash
# Terminal Quest Uninstaller

echo "Uninstalling Terminal Quest: Remastered..."

# Remove installation directory
rm -rf "$INSTALL_DIR"

# Remove desktop entry
if [ -f "$DESKTOP_FILE_DIR/terminal-quest.desktop" ]; then
    rm -f "$DESKTOP_FILE_DIR/terminal-quest.desktop"
fi

if [ -f "$LOCAL_DESKTOP_DIR/terminal-quest.desktop" ]; then
    rm -f "$LOCAL_DESKTOP_DIR/terminal-quest.desktop"
fi

# Remove user save files (optional)
read -p "Remove save files and user data? (y/N): " -n 1 -r
echo
if [[ \$REPLY =~ ^[Yy]$ ]]; then
    rm -f "\$HOME/.terminal_quest_save.json"
    rm -rf "\$HOME/terminal_quest_sandbox"
    echo "User data removed"
fi

echo "Terminal Quest: Remastered has been uninstalled"
EOF

    chmod +x "$INSTALL_DIR/uninstall.sh"
    echo -e "${GREEN}[SUCCESS] Created uninstaller at $INSTALL_DIR/uninstall.sh${NC}"
}

setup_ollama_instructions() {
    cat > "$INSTALL_DIR/OLLAMA_SETUP.md" << 'EOF'
# Ollama Setup for Terminal Quest

Terminal Quest uses Ollama for AI-powered command safety analysis. This is optional but recommended for the best experience.

## Installation

1. Install Ollama from https://ollama.ai
2. Start the Ollama service: `ollama serve`
3. Install a recommended model: `ollama pull llama3.2:3b`

## Configuration

The game is configured to use `http://localhost:11434` by default. If you need to change this:

1. Edit `config.json` in the Terminal Quest directory
2. Update the `ollama_endpoint` field
3. Restart Terminal Quest

## Cloudflare Tunnel Setup (Advanced)

If you want to use a remote Ollama server through Cloudflare tunnel:

1. Install cloudflared: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/
2. Authenticate: `cloudflared tunnel login`
3. Create tunnel: `cloudflared tunnel create terminal-quest-ollama`
4. Configure tunnel to forward to your Ollama server
5. Run tunnel: `cloudflared tunnel run terminal-quest-ollama`
6. Update `config.json` with your tunnel URL

## Model Recommendations

- **llama3.2:3b** - Fast and efficient, recommended for most setups
- **qwen2.5:7b** - Larger but more capable
- **phi3:mini** - Microsoft's efficient model

Choose based on your hardware capabilities.
EOF

    echo -e "${GREEN}[INFO] Created Ollama setup guide at $INSTALL_DIR/OLLAMA_SETUP.md${NC}"
}

post_install_info() {
    echo ""
    echo -e "${PURPLE}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║                   INSTALLATION COMPLETE                 ║${NC}"
    echo -e "${PURPLE}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${GREEN}Terminal Quest: Remastered has been installed successfully!${NC}"
    echo ""
    echo -e "${CYAN}Installation directory:${NC} $INSTALL_DIR"
    echo ""
    echo -e "${YELLOW}How to run:${NC}"
    echo "• Look for 'Terminal Quest: Remastered' in your applications menu"
    echo "• Or run directly: $INSTALL_DIR/launch_terminal_quest.sh"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo "1. Optionally set up Ollama for AI features (see OLLAMA_SETUP.md)"
    echo "2. Add your custom ASCII art to ascii_art.json"
    echo "3. Launch the game and start learning!"
    echo ""
    echo -e "${CYAN}For uninstalling:${NC} Run $INSTALL_DIR/uninstall.sh"
    echo ""
}

# Main installation process
main() {
    print_banner
    
    # Check if running from correct directory
    if [ ! -f "main.py" ]; then
        echo -e "${RED}[ERROR] Please run this script from the Terminal Quest directory${NC}"
        echo -e "${YELLOW}[INFO] The main.py file should be in the same directory as this script${NC}"
        exit 1
    fi
    
    check_dependencies
    check_ollama_setup
    create_install_directory
    copy_game_files
    create_desktop_entry
    create_uninstaller
    setup_ollama_instructions
    post_install_info
}

# Handle script interruption
trap 'echo -e "\n${YELLOW}[SYSTEM] Installation interrupted.${NC}"; exit 1' INT

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo -e "${YELLOW}[WARNING] Running as root - installing system-wide${NC}"
    echo -e "${YELLOW}[INFO] All users will have access to Terminal Quest${NC}"
else
    echo -e "${CYAN}[INFO] Running as user - installing locally${NC}"
    echo -e "${CYAN}[INFO] Only current user will have access${NC}"
fi

echo ""
read -p "Continue with installation? (Y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Nn]$ ]]; then
    echo "Installation cancelled"
    exit 0
fi

main "$@"