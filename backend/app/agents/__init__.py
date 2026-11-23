"""
Itihasa Saga Autonomous Multi-Agent Subsystem:
1. ScriptwriterAgent - Enforces 60-90s narrative arcs, 5-act structures, explicit character motives.
2. ProductionDirectorAgent - Enforces strict scriptural iconography, negative prompt filters, overlay design.
3. SocialMediaManagerAgent - Monitors, validates, and certifies multi-platform publishing across YouTube, Instagram, and Facebook.
"""

from .scriptwriter_agent import ScriptwriterAgent
from .director_agent import ProductionDirectorAgent
from .social_media_manager_agent import SocialMediaManagerAgent

__all__ = ["ScriptwriterAgent", "ProductionDirectorAgent", "SocialMediaManagerAgent"]
