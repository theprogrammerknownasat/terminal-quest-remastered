"""
Safety System for Terminal Quest: Remastered
Provides basic command safety checking and dangerous command blocking
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Set

class SafetySystem:
    def __init__(self, ollama_endpoint=None):
        self.ollama_endpoint = ollama_endpoint
        
        # Global blacklist of dangerous commands and patterns
        self.dangerous_commands = {
            # File system destruction
            'rm': {
                'patterns': [r'rm\s+(-rf|--recursive.*--force)', r'rm\s+-[a-zA-Z]*r[a-zA-Z]*f', r'rm\s+-[a-zA-Z]*f[a-zA-Z]*r'],
                'reason': "The 'rm -rf' command can permanently delete files and folders without asking. That's too dangerous for learning!"
            },
            'dd': {
                'patterns': [r'dd\s+if=.*of=', r'dd\s+of=/dev/'],
                'reason': "The 'dd' command can overwrite entire drives. We definitely don't want to use that while learning!"
            },
            'mkfs': {
                'patterns': [r'mkfs'],
                'reason': "The 'mkfs' command formats drives, which would erase everything. Let's avoid that!"
            },
            
            # System modification
            'chmod': {
                'patterns': [r'chmod\s+777\s+/', r'chmod\s+-R\s+777'],
                'reason': "Changing permissions on system directories can make your computer unsafe. Let's practice on safe files first."
            },
            'chown': {
                'patterns': [r'chown\s+root', r'chown\s+.*:.*\s+/'],
                'reason': "Changing ownership of system files can break your computer. Let's stick to your own files for now."
            },
            
            # Network and downloads
            'curl': {
                'patterns': [r'curl.*\|.*sh', r'curl.*\|.*bash', r'curl.*>', r'curl\s+.*://'],
                'reason': "Downloading and running scripts from the internet can be dangerous. Let's learn other commands first."
            },
            'wget': {
                'patterns': [r'wget.*\|', r'wget.*>', r'wget\s+.*://'],
                'reason': "Downloading files from the internet should be done carefully. Let's focus on local files for now."
            },
            
            # Process and system control
            'killall': {
                'patterns': [r'killall', r'pkill\s+-9'],
                'reason': "Killing processes can make your system unstable. Let's learn gentler commands first."
            },
            'reboot': {
                'patterns': [r'reboot', r'shutdown', r'halt', r'poweroff'],
                'reason': "System restart commands should be used carefully. Let's keep learning without rebooting!"
            },
            
            # Dangerous system areas
            'system_dirs': {
                'patterns': [r'(rm|mv|cp|chmod|chown).*\s+/(etc|sys|proc|dev|boot|bin|sbin|usr/bin|usr/sbin)', 
                           r'cd\s+/(etc|sys|proc|dev|boot|bin|sbin)'],
                'reason': "System directories contain important files. Let's practice in safer areas like your home directory."
            },
            
            # Fork bombs and resource exhaustion
            'forkbomb': {
                'patterns': [r':\(\)\{.*\|.*&\}', r':()\{.*\}', r'while\s+true.*do', r'for.*in.*\`seq'],
                'reason': "That looks like a fork bomb or infinite loop that could freeze your computer. Let's not do that!"
            },
            
            # Privilege escalation
            'sudo_dangerous': {
                'patterns': [r'sudo\s+(rm|dd|mkfs|chmod|chown).*/', r'sudo\s+.*>.*/(etc|sys|proc|dev)'],
                'reason': "Using sudo with system-modifying commands can be dangerous. Let's learn the basics first."
            }
        }
        
        # Safe directories - commands are generally allowed here
        self.safe_directories = {
            str(Path.home()),
            str(Path.home() / "terminal_quest_sandbox"),
            str(Path.home() / "Documents"),
            str(Path.home() / "Downloads"),
            str(Path.home() / "Pictures"),
            str(Path.home() / "Desktop")
        }
        
        # Commands that are generally safe for learning
        self.safe_commands = {
            # Navigation and exploration
            'pwd', 'ls', 'cd', 'tree', 'file', 'stat', 'du', 'df',
            
            # File viewing
            'cat', 'less', 'more', 'head', 'tail', 'grep', 'sort', 'uniq', 'wc',
            
            # File operations (in safe directories only)
            'touch', 'mkdir', 'cp', 'mv', 'nano', 'echo',
            
            # System information (read-only)
            'ps', 'top', 'htop', 'free', 'uname', 'whoami', 'id', 'groups',
            'lscpu', 'lsmem', 'lsblk', 'lspci', 'lsusb', 'lsmod',
            
            # Date and time
            'date', 'cal', 'uptime',
            
            # Help and documentation
            'man', 'help', 'info', 'which', 'type', 'apropos',
            
            # Safe system queries
            'systemctl status', 'journalctl', 'dmesg'
        }
    
    def is_command_safe(self, command: str, current_dir: str) -> bool:
        """
        Check if a command is safe to execute
        
        Args:
            command: The command string to check
            current_dir: Current working directory
            
        Returns:
            bool: True if safe, False if dangerous
        """
        command = command.strip()
        
        # Empty command is safe
        if not command:
            return True
        
        # Check against dangerous patterns
        for cmd_type, cmd_info in self.dangerous_commands.items():
            for pattern in cmd_info['patterns']:
                if re.search(pattern, command, re.IGNORECASE):
                    return False
        
        # Check if trying to modify files outside safe directories
        if not self._is_directory_safe(command, current_dir):
            return False
        
        # Check for shell injection attempts
        if self._contains_shell_injection(command):
            return False
        
        return True
    
    def get_danger_reason(self, command: str) -> str:
        """
        Get the reason why a command is considered dangerous
        
        Args:
            command: The dangerous command
            
        Returns:
            str: Human-readable explanation of why it's dangerous
        """
        command = command.strip()
        
        # Check against our dangerous command patterns
        for cmd_type, cmd_info in self.dangerous_commands.items():
            for pattern in cmd_info['patterns']:
                if re.search(pattern, command, re.IGNORECASE):
                    return cmd_info['reason']
        
        # Generic fallback reason
        return "This command could potentially harm your system or data. Let's stick to safer learning commands for now."
    
    def _is_directory_safe(self, command: str, current_dir: str) -> bool:
        """Check if the command is operating in a safe directory"""
        # Extract file paths from common commands
        file_commands = ['rm', 'mv', 'cp', 'chmod', 'chown', 'touch', 'mkdir']
        base_cmd = command.split()[0]
        
        if base_cmd not in file_commands:
            return True  # Not a file operation command
        
        # For cd command, check destination
        if base_cmd == 'cd':
            if len(command.split()) > 1:
                target = command.split()[1]
                if target.startswith('/') and not any(target.startswith(safe) for safe in self.safe_directories):
                    return False
            return True
        
        # For other file commands, check if operating on safe paths
        tokens = command.split()
        for token in tokens[1:]:  # Skip the command itself
            if token.startswith('/'):
                # Absolute path - check if it's in a safe directory
                if not any(token.startswith(safe) for safe in self.safe_directories):
                    return False
            elif token.startswith('..'):
                # Relative path going up - could be dangerous
                # Allow some upward navigation but not too far
                if token.count('..') > 3:
                    return False
        
        return True
    
    def _contains_shell_injection(self, command: str) -> bool:
        """Check for shell injection patterns"""
        dangerous_chars = ['|', '&', ';', '`', '$', '(', ')', '{', '}']
        
        # Allow some safe uses of these characters
        safe_patterns = [
            r'ls\s+-[a-zA-Z]*l',  # ls -l is fine
            r'grep\s+.*\|.*',     # Simple grep pipes might be OK in advanced lessons
        ]
        
        # Check for dangerous character combinations
        if any(char in command for char in ['|', '&', ';']) and not any(re.search(pattern, command) for pattern in safe_patterns):
            # Check for command chaining, backgrounding, or piping to dangerous commands
            if re.search(r'[|&;]\s*(rm|dd|sudo|curl|wget)', command):
                return True
        
        # Check for command substitution
        if '`' in command or '$(' in command:
            return True
        
        return False
    
    def get_safe_alternatives(self, dangerous_command: str) -> List[str]:
        """Suggest safe alternatives to dangerous commands"""
        base_cmd = dangerous_command.split()[0]
        
        alternatives = {
            'rm': ['ls', 'mv to_trash/', 'nano (to edit instead of delete)'],
            'dd': ['cp', 'cat', 'less'],
            'curl': ['cat local_file.txt', 'nano to create content'],
            'wget': ['cp', 'touch to create files'],
            'sudo': ['Try the command without sudo first', 'Ask for help if you need system access'],
        }
        
        return alternatives.get(base_cmd, ['ls', 'pwd', 'cd', 'cat'])
    
    def create_safe_environment(self, base_dir: Path) -> None:
        """Create a safe sandbox environment for learning"""
        sandbox = base_dir / "terminal_quest_sandbox"
        sandbox.mkdir(exist_ok=True)
        
        # Create directory structure
        (sandbox / "documents").mkdir(exist_ok=True)
        (sandbox / "pictures").mkdir(exist_ok=True)
        (sandbox / "projects").mkdir(exist_ok=True)
        (sandbox / "temp").mkdir(exist_ok=True)
        
        # Create sample files
        sample_files = {
            "welcome.txt": "Welcome to Terminal Quest! This is your safe learning environment.",
            "readme.md": "# Terminal Quest Sandbox\n\nThis is a safe place to practice Linux commands!",
            "documents/notes.txt": "Practice file for editing.\nYou can modify this safely!",
            "documents/todo.txt": "Things to learn:\n- Basic navigation\n- File operations\n- System exploration",
            "temp/test.txt": "This is a test file you can experiment with."
        }
        
        for file_path, content in sample_files.items():
            file_full_path = sandbox / file_path
            file_full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_full_path, 'w') as f:
                f.write(content)
        
        print(f"[SAFETY] Created safe learning environment at {sandbox}")
    
    def is_path_safe(self, path: str, current_dir: str) -> bool:
        """Check if a specific path is safe to access"""
        if path.startswith('/'):
            # Absolute path
            return any(path.startswith(safe) for safe in self.safe_directories)
        else:
            # Relative path - resolve it
            full_path = Path(current_dir) / path
            resolved_path = str(full_path.resolve())
            return any(resolved_path.startswith(safe) for safe in self.safe_directories)