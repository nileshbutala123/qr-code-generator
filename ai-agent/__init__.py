# AI Agent Module
"""
AI Agent for automated code generation from requirements
"""

# Legacy modules (for backward compatibility)
from .agent import AIAgent
from .requirements_reader import RequirementsReader
from .planner import Planner
from .coder import Coder
from .pr_creator import PRCreator

# New intelligent agent modules
from .intelligent_agent import IntelligentAgent
from .codebase_analyzer import CodebaseAnalyzer
from .claude_codegen import ClaudeCodeGen
from .enhanced_pr_creator import EnhancedPRCreator

__all__ = [
    # Legacy
    'AIAgent',
    'RequirementsReader',
    'Planner',
    'Coder',
    'PRCreator',
    # New intelligent components
    'IntelligentAgent',
    'CodebaseAnalyzer',
    'ClaudeCodeGen',
    'EnhancedPRCreator',
]
