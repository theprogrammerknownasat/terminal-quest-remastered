#!/bin/bash

# Terminal Quest: Remastered Launcher Script
# This script handles the visual effects and TTY switching

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GAME_PYTHON="$SCRIPT_DIR/main.py"
CONFIG_FILE="$SCRIPT_DIR/config.json"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to check if we're in tutorial mode
check_tutorial_mode() {
    if [ -f "$CONFIG_FILE" ]; then
        # Check if tutorial is completed
        if grep -q '"tutorial_completed": true' "$CONFIG_FILE"; then
            return 1  # Tutorial completed
        fi
    fi
    return 0  # Tutorial mode
}

# Function to create popup windows for visual effect
create_popup_chaos() {
    echo -e "${RED}[SYSTEM] Initializing dramatic visual effects...${NC}"
    
    # Create various error popups using zenity
    zenity --error --text="CRITICAL ERROR: Graphics subsystem failure detected!" --timeout=2 &
    sleep 0.5
    
    zenity --warning --text="WARNING: Display corruption in progress..." --timeout=2 &
    sleep 0.3
    
    zenity --error --text="FATAL: Desktop environment crashed!" --timeout=2 &
    sleep 0.4
    
    zenity --info --text="DIAGNOSTIC: Attempting recovery..." --timeout=2 &
    sleep 0.6
    
    zenity --warning --text="ALERT: Falling back to emergency mode..." --timeout=2 &
    sleep 0.2
    
    zenity --error --text="ERROR: GUI services unresponsive!" --timeout=2 &
    sleep 0.7
    
    zenity --warning --text="SYSTEM: Switching to text mode..." --timeout=2 &
    sleep 0.5
    
    # Wait a moment for dramatic effect
    sleep 2
    
    echo -e "${YELLOW}[SYSTEM] Visual chaos sequence complete.${NC}"
}

# Function to show Plymouth shutdown screen
show_plymouth_shutdown() {
    echo -e "${BLUE}[SYSTEM] Initiating Plymouth shutdown sequence...${NC}"
    
    # Clear the screen
    clear
    
    # Simulate Plymouth shutdown screen
    echo -e "${CYAN}"
    echo "                    Fedora Linux 42"
    echo ""
    echo "          [████████████████████████████]"
    echo ""
    echo "                 Shutting down..."
    echo ""
    echo "              Please wait while we"
    echo "           prepare the system for you"
    echo -e "${NC}"
    
    # Animate the shutdown
    for i in {1..3}; do
        sleep 1
        echo "."
    done
    
    sleep 2
    clear
}

# Function to kill GUI and run game in text mode
kill_gui_and_launch() {
    echo -e "${GREEN}[SYSTEM] Preparing dramatic text-mode experience...${NC}"
    
    # Kill any existing popups
    pkill zenity 2>/dev/null
    
    # Save current GUI session info
    echo "$DISPLAY" > /tmp/terminal_quest_display
    echo "$DESKTOP_SESSION" > /tmp/terminal_quest_session
    
    # Create a script to run after killing GUI
    cat > /tmp/terminal_quest_textmode.sh << EOF
#!/bin/bash
# Clear the screen completely
clear
tput reset

# Show Plymouth-style shutdown
echo -e "${CYAN}"
echo "                    Fedora Linux 42"
echo ""
echo "          [████████████████████████████]"
echo ""
echo "                 Shutting down..."
echo ""
echo "              Please wait while we"
echo "           prepare the system for you"
echo -e "${NC}"

# Brief animation
for i in {1..3}; do
    sleep 1
    echo "."
done

sleep 2
clear

# Show the game banner
echo "=================================="
echo "    TERMINAL QUEST: REMASTERED"
echo "=================================="
echo ""
echo "Note: This is an educational game."
echo "Your computer is NOT actually broken!"
echo ""
echo "You can exit at any time by typing 'exit'"
echo ""
echo "=================================="
echo ""

# Run the Python game
cd "$SCRIPT_DIR"
python3 "$GAME_PYTHON" --tty-mode

# After game exits, restore GUI
echo ""
echo "=================================="
echo "Restoring your desktop environment..."
echo "Please wait a moment..."
echo "=================================="

# Restart the display manager
sudo systemctl restart gdm

exit 0
EOF

    chmod +x /tmp/terminal_quest_textmode.sh
    
    # Switch to a text console and run our script
    echo -e "${YELLOW}[SYSTEM] Switching to text mode...${NC}"
    echo -e "${YELLOW}[SYSTEM] Your desktop will be restored when you exit the game.${NC}"
    sleep 2
    
    # Kill the GUI session and switch to text mode
    sudo systemctl stop gdm
    
    # Run the game script in the current terminal
    /tmp/terminal_quest_textmode.sh
}

# Alternative simpler approach - run in current terminal with effects
launch_with_effects() {
    echo -e "${GREEN}[SYSTEM] Launching Terminal Quest with visual effects...${NC}"
    
    # Create popup chaos
    create_popup_chaos
    
    # Clear terminal and show dramatic transition
    sleep 1
    clear
    
    # Show Plymouth-style shutdown
    echo -e "${CYAN}"
    echo "                    Fedora Linux 42"
    echo ""
    echo "          [████████████████████████████]"
    echo ""
    echo "                 Shutting down..."
    echo ""
    echo "              Please wait while we"
    echo "           prepare the system for you"
    echo -e "${NC}"
    
    # Brief animation
    for i in {1..3}; do
        sleep 1
        echo "."
    done
    
    sleep 2
    clear
    
    # Show the game banner
    echo "=================================="
    echo "    TERMINAL QUEST: REMASTERED"
    echo "=================================="
    echo ""
    echo "Note: This is an educational game."
    echo "Your computer is NOT actually broken!"
    echo ""
    echo "You can exit at any time by typing 'exit'"
    echo ""
    echo "=================================="
    echo ""
    
    # Run the Python game
    cd "$SCRIPT_DIR"
    python3 "$GAME_PYTHON" --tty-mode
}

# Function to launch safe terminal mode (post-tutorial)
launch_safe_terminal() {
    echo -e "${GREEN}[TERMINAL QUEST] Launching Safe Terminal Mode...${NC}"
    
    # Create a temporary script for the safe terminal
    cat > /tmp/safe_terminal.sh << EOF
#!/bin/bash
clear
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                    SAFE TERMINAL MODE                    ║"
echo "║                  Terminal Quest Alumni                   ║"
echo "╠══════════════════════════════════════════════════════════╣"
echo "║                                                          ║"
echo "║  [SHELL] Welcome back! You've completed the tutorial     ║"
echo "║          and earned access to Safe Terminal Mode.        ║"
echo "║                                                          ║"
echo "║  This terminal has safety guardrails to protect you      ║"
echo "║  while you practice your new skills.                     ║"
echo "║                                                          ║"
echo "║  Commands available:                                     ║"
echo "║  • reset-tutorial  - Start the tutorial over            ║"
echo "║  • help           - Show available commands             ║"
echo "║  • exit           - Close this terminal                 ║"
echo "║                                                          ║"
echo "║  Remember: You can always use the regular terminal      ║"
echo "║  too, but be careful - no safety nets there!            ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "[SHELL] Ready for your commands!"
echo ""

# Run the safe terminal version
cd "$SCRIPT_DIR"
python3 "$GAME_PYTHON" --safe-mode
EOF

    chmod +x /tmp/safe_terminal.sh
    
    # Launch in a new terminal window
    if command -v gnome-terminal >/dev/null 2>&1; then
        gnome-terminal -- /tmp/safe_terminal.sh
    elif command -v konsole >/dev/null 2>&1; then
        konsole -e /tmp/safe_terminal.sh
    elif command -v xterm >/dev/null 2>&1; then
        xterm -e /tmp/safe_terminal.sh
    else
        # Fallback to current terminal
        /tmp/safe_terminal.sh
    fi
}

# Function to request sudo access upfront
request_sudo() {
    echo -e "${YELLOW}[SYSTEM] Terminal Quest needs temporary administrator access${NC}"
    echo -e "${YELLOW}         for TTY switching and visual effects.${NC}"
    echo ""
    echo "This is required to:"
    echo "  • Switch to a text-only screen for the full experience"
    echo "  • Create dramatic visual effects"
    echo "  • Return you safely to your desktop when done"
    echo ""
    
    # Use pkexec for GUI authentication if available
    if command -v pkexec >/dev/null 2>&1; then
        echo -e "${GREEN}[SYSTEM] Please authenticate in the popup window...${NC}"
        if ! pkexec bash -c "echo 'Authentication successful'"; then
            echo -e "${RED}[ERROR] Authentication failed. Cannot launch full experience.${NC}"
            echo -e "${YELLOW}[INFO] You can still run in basic mode with: python3 main.py${NC}"
            exit 1
        fi
    else
        # Fallback to sudo
        echo -e "${GREEN}[SYSTEM] Please enter your password:${NC}"
        if ! sudo -v; then
            echo -e "${RED}[ERROR] Authentication failed. Cannot launch full experience.${NC}"
            echo -e "${YELLOW}[INFO] You can still run in basic mode with: python3 main.py${NC}"
            exit 1
        fi
    fi
    
    echo -e "${GREEN}[SYSTEM] Authentication successful!${NC}"
}

# Main execution
main() {
    echo -e "${PURPLE}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║              TERMINAL QUEST: REMASTERED                  ║${NC}"
    echo -e "${PURPLE}║           An Educational Linux Adventure                ║${NC}"
    echo -e "${PURPLE}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    # Check if Python script exists
    if [ ! -f "$GAME_PYTHON" ]; then
        echo -e "${RED}[ERROR] Game files not found at $GAME_PYTHON${NC}"
        echo -e "${YELLOW}[INFO] Make sure you're running this from the game directory.${NC}"
        exit 1
    fi
    
    # Check tutorial status
    if check_tutorial_mode; then
        echo -e "${CYAN}[INFO] Tutorial mode detected - launching full experience...${NC}"
        echo ""
        
        # Request authentication
        request_sudo
        
        echo -e "${GREEN}[SYSTEM] Starting Terminal Quest experience...${NC}"
        echo ""
        echo -e "${YELLOW}Choose your experience:${NC}"
        echo "1. Full immersion (kills desktop temporarily) - Most dramatic!"
        echo "2. Current terminal with effects - Safer option"
        echo ""
        read -p "Enter choice (1 or 2): " -n 1 -r
        echo ""
        
        case $REPLY in
            1)
                echo -e "${CYAN}[INFO] Full immersion mode selected${NC}"
                echo -e "${YELLOW}[WARNING] This will temporarily shut down your desktop${NC}"
                echo -e "${YELLOW}[INFO] It will be restored automatically when you exit the game${NC}"
                echo ""
                read -p "Continue? (y/N): " -n 1 -r
                echo ""
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    kill_gui_and_launch
                else
                    echo "Falling back to safer option..."
                    launch_with_effects
                fi
                ;;
            2|*)
                echo -e "${CYAN}[INFO] Terminal effects mode selected${NC}"
                launch_with_effects
                ;;
        esac
        
    else
        echo -e "${CYAN}[INFO] Tutorial completed - launching Safe Terminal Mode...${NC}"
        echo ""
        launch_safe_terminal
    fi
}

# Handle script interruption
trap 'echo -e "\n${YELLOW}[SYSTEM] Launch interrupted. Cleaning up...${NC}"; pkill zenity 2>/dev/null; exit 1' INT

# Check dependencies
check_dependencies() {
    local missing_deps=()
    
    # Check for required commands
    command -v python3 >/dev/null 2>&1 || missing_deps+=("python3")
    command -v zenity >/dev/null 2>&1 || missing_deps+=("zenity")
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        echo -e "${RED}[ERROR] Missing required dependencies:${NC}"
        printf ' - %s\n' "${missing_deps[@]}"
        echo ""
        echo -e "${YELLOW}On Fedora, install with:${NC}"
        echo "sudo dnf install python3 zenity"
        exit 1
    fi
}

# Check dependencies and run main function
check_dependencies
main "$@"