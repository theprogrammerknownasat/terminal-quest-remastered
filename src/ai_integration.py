"""
AI Integration for Terminal Quest: Remastered
Handles intelligent command analysis using Ollama
"""

import requests
import json
import time
from typing import Tuple, Dict, Any

class AICommandAnalyzer:
    def __init__(self, ollama_endpoint="http://localhost:11434"):
        self.ollama_endpoint = ollama_endpoint.rstrip('/')
        self.model = "llama3.2:3b"  # Default model, can be configured
        self.max_retries = 3
        self.timeout = 10
        
        # Test connection on initialization
        self.test_connection()
    
    def test_connection(self):
        """Test if Ollama server is accessible"""
        try:
            response = requests.get(f"{self.ollama_endpoint}/api/tags", timeout=5)
            if response.status_code == 200:
                print("[AI] Connected to Ollama server successfully")
                return True
        except requests.exceptions.RequestException:
            print("[AI] Warning: Could not connect to Ollama server")
            print(f"[AI] Make sure Ollama is running at {self.ollama_endpoint}")
            print("[AI] Falling back to basic safety checks only")
            return False
        return False
    
    def analyze_command(self, command: str, current_dir: str, game_progress: int, story_context: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Analyze if a command is safe and appropriate for the current context
        
        Returns:
            Tuple[bool, str]: (is_safe, reasoning)
        """
        # Try AI analysis first
        try:
            return self._ai_analyze_command(command, current_dir, game_progress, story_context)
        except Exception as e:
            print(f"[AI] Error in AI analysis: {e}")
            # Fall back to basic analysis
            return self._basic_analyze_command(command, current_dir, game_progress, story_context)
    
    def _ai_analyze_command(self, command: str, current_dir: str, game_progress: int, story_context: Dict[str, Any]) -> Tuple[bool, str]:
        """AI-powered command analysis using Ollama"""
        
        # Build context for the AI
        context_info = {
            "command": command,
            "current_directory": current_dir,
            "game_progress": game_progress,
            "chapter": story_context.get('chapter', 1),
            "commands_learned": story_context.get('commands_learned', []),
            "lesson_context": story_context.get('lesson_context', 'general'),
            "expecting_command": story_context.get('expecting_command')
        }
        
        # Create the prompt for the AI
        prompt = self._build_safety_prompt(context_info)
        
        # Make request to Ollama
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,  # Low temperature for consistent safety decisions
                "top_p": 0.9,
                "num_predict": 200   # Limit response length
            }
        }
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    f"{self.ollama_endpoint}/api/generate",
                    json=payload,
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    ai_response = result.get('response', '').strip()
                    
                    # Parse the AI response
                    return self._parse_ai_response(ai_response)
                
            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise e
                time.sleep(1)  # Brief pause before retry
        
        # If we get here, AI analysis failed
        raise Exception("Failed to get AI analysis after retries")
    
    def _build_safety_prompt(self, context: Dict[str, Any]) -> str:
        """Build the prompt for AI safety analysis"""
        
        prompt = f"""You are a safety analyzer for an educational Linux tutorial game called Terminal Quest. A complete beginner is learning Linux commands in a controlled environment.

CONTEXT:
- Command to analyze: "{context['command']}"
- Current directory: {context['current_directory']}
- Game progress level: {context['game_progress']} (1=beginner, 5=advanced)
- Current chapter: {context['chapter']}
- Commands they've learned: {', '.join(context['commands_learned']) if context['commands_learned'] else 'none yet'}
- Current lesson context: {context['lesson_context']}
- Expected command (if any): {context.get('expecting_command', 'none')}

SAFETY RULES:
1. BLOCK dangerous commands that could harm the system (rm -rf, dd, mkfs, etc.)
2. BLOCK commands that access sensitive system areas (/etc, /sys, /proc modifications)
3. BLOCK network commands that could be risky (curl to unknown sites, wget, etc.)
4. ALLOW educational commands appropriate for their learning level
5. GENTLY REDIRECT if they're trying something too advanced for their current level
6. ENCOURAGE if they're experimenting appropriately with learned commands

LEARNING PROGRESSION:
- Level 1: pwd, ls, cd, cat, less
- Level 2: mkdir, touch, cp, mv, nano
- Level 3: chmod, find, grep, head, tail
- Level 4: ps, top, df, free, lspci
- Level 5: systemctl, journalctl (read-only system commands)

Respond with EXACTLY this format:
DECISION: SAFE/UNSAFE
REASON: [Brief explanation suitable for a beginner, staying in character as their helpful guide "Shell"]

Example responses:
DECISION: SAFE
REASON: Great! That's exactly what we need to learn right now. The 'ls' command will show you what's in this directory.

DECISION: UNSAFE
REASON: Whoa there! That command is quite advanced and could modify important system files. Let's stick to exploring with 'ls' and 'cd' for now.
"""
        
        return prompt
    
    def _parse_ai_response(self, ai_response: str) -> Tuple[bool, str]:
        """Parse the AI response into safety decision and reasoning"""
        lines = ai_response.strip().split('\n')
        
        decision = None
        reason = "I need to think about that command a bit more."
        
        for line in lines:
            line = line.strip()
            if line.startswith('DECISION:'):
                decision_text = line.replace('DECISION:', '').strip().upper()
                decision = decision_text == 'SAFE'
            elif line.startswith('REASON:'):
                reason = line.replace('REASON:', '').strip()
        
        # Default to unsafe if we can't parse the response properly
        if decision is None:
            decision = False
            reason = "I'm not sure about that command right now. Let's try something else."
        
        return decision, reason
    
    def _basic_analyze_command(self, command: str, current_dir: str, game_progress: int, story_context: Dict[str, Any]) -> Tuple[bool, str]:
        """Basic fallback analysis when AI is unavailable"""
        
        # Basic safe commands for beginners
        safe_commands = {
            1: ['pwd', 'ls', 'cd', 'cat', 'less', 'head', 'tail'],
            2: ['mkdir', 'touch', 'cp', 'mv', 'nano', 'echo'],
            3: ['find', 'grep', 'sort', 'uniq', 'wc'],
            4: ['ps', 'top', 'df', 'free', 'lspci', 'lsusb', 'uname'],
            5: ['systemctl status', 'journalctl', 'dmesg']
        }
        
        # Get base command
        base_command = command.split()[0]
        
        # Check if command is in the allowed list for their level
        allowed_commands = []
        for level in range(1, min(game_progress + 1, 6)):
            allowed_commands.extend(safe_commands.get(level, []))
        
        # Special handling for specific commands
        if base_command in ['systemctl', 'journalctl']:
            # Only allow read-only operations
            if any(dangerous in command for dangerous in ['start', 'stop', 'enable', 'disable', 'restart']):
                return False, "That's a system administration command that could affect running services. Let's stick to learning basics first."
        
        # Check for obviously dangerous patterns
        dangerous_patterns = [
            'rm -rf', 'dd if=', 'mkfs', '> /dev/', 'chmod 777 /', 
            'chown root', 'sudo rm', 'sudo dd', '://', 'curl', 'wget'
        ]
        
        for pattern in dangerous_patterns:
            if pattern in command.lower():
                return False, "That command could potentially harm your system. Let's practice with safer commands first."
        
        # Check if they're trying to leave the safe directory structure
        if base_command == 'cd':
            target = command.split()[1] if len(command.split()) > 1 else "~"
            if target.startswith('/') and not target.startswith('/home'):
                return False, "Let's stick to exploring your home directory area for now. System directories can wait until you're more experienced."
        
        # If command seems safe and appropriate for their level
        if base_command in allowed_commands:
            return True, f"Good choice! The '{base_command}' command is perfect for where you are in your learning."
        
        # Unknown command - be cautious but educational
        return False, f"I'm not familiar with '{base_command}' or it might be too advanced right now. Try using commands we've learned like: {', '.join(allowed_commands[:5])}."
    
    def update_model(self, model_name: str):
        """Update the AI model being used"""
        self.model = model_name
        print(f"[AI] Switched to model: {model_name}")
    
    def get_available_models(self):
        """Get list of available models from Ollama"""
        try:
            response = requests.get(f"{self.ollama_endpoint}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
        except requests.exceptions.RequestException:
            pass
        return []


class ShellAI:
    """
    Optional AI-powered Shell character
    Currently not used - keeping classical scripted approach
    But available if we want to experiment later
    """
    
    def __init__(self, ollama_endpoint="http://localhost:11434"):
        self.ollama_endpoint = ollama_endpoint.rstrip('/')
        self.model = "llama3.2:3b"
        
        # Shell personality prompt
        self.personality_prompt = """You are Shell, a helpful AI character in an educational Linux tutorial game. You are:

- Friendly, patient, and encouraging
- A master of Linux who loves teaching beginners
- Knowledgeable about computers but explain things simply
- Never condescending - you remember what it was like to learn
- Enthusiastic about helping users discover the power of the command line
- You use analogies and real-world comparisons to explain technical concepts
- You celebrate small victories and encourage experimentation

You're guiding a complete beginner through their first computer experience. Stay in character as Shell, and keep responses concise but warm."""
    
    def generate_response(self, user_context: str, conversation_history: list = None) -> str:
        """Generate an AI response as Shell (if we choose to use this)"""
        # Implementation would go here if we decide to make Shell AI-powered
        # For now, keeping the classical scripted approach
        pass