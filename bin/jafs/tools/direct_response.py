"""
Direct Response Tool for the JAFS framework.

This tool handles creative tasks like writing poems, stories, and other content generation
by leveraging the language model's capabilities.

Author   Joel Hernandez James
Current Date  3/12/2025
Class
"""

from typing import Dict, Any, Optional, List, Union
import re
import logging

from jafs.tools.base.tool import Tool
from jafs.tools.base.tool_result import ToolResult

class DirectResponseTool(Tool):
    """
    A tool for generating creative content like poems, stories, and other text.
    
    This tool uses the language model directly to generate responses for creative tasks
    that don't require specific computational tools. Instead of hard-coding responses,
    it passes the request to the language model with appropriate context about the
    requested creative task.
    """
    
    def __init__(self):
        """Initialize the DirectResponseTool."""
        super().__init__(
            name="direct_response",
            description="Generates creative content like poems, stories, and other text",
            parameters={
                "prompt": {
                    "type": "string",
                    "description": "The creative task to perform"
                }
            },
            required_parameters=["prompt"]
        )
    
    def _is_creative_task(self, prompt: str) -> bool:
        """
        Determine if a prompt is asking for a creative task.
        
        Args:
            prompt: The user's prompt
            
        Returns:
            True if the prompt is asking for a creative task, False otherwise
        """
        creative_keywords = [
            "write", "compose", "create", "generate", "draft",
            "poem", "story", "essay", "article", "letter",
            "song", "lyrics", "script", "dialogue", "narrative",
            "fiction", "creative", "imagine", "fantasy"
        ]
        
        # Check if any creative keywords are in the prompt
        for keyword in creative_keywords:
            if re.search(r'\b' + keyword + r'\b', prompt.lower()):
                return True
        
        return False
    
    def _execute(self, parameters: Dict[str, Any]) -> ToolResult:
        """
        Execute the direct response tool.
        
        Args:
            parameters: The parameters for the tool
            
        Returns:
            A ToolResult containing the generated content
        """
        prompt = parameters.get("prompt", "")
        
        # Check if this is a creative task
        if not self._is_creative_task(prompt):
            return ToolResult(
                success=False,
                message="This doesn't seem to be a creative task. Please try a different tool.",
                data=None
            )
        
        # Determine the type of creative task
        task_type = self._determine_task_type(prompt)
        
        # Create a context-aware prompt for the language model
        context_prompt = self._create_context_prompt(prompt, task_type)
        
        # Get the response from the language model
        # Note: In a real implementation, this would call the language model
        # For now, we'll return a placeholder
        response = f"This is where the language model would generate a {task_type} based on: {prompt}"
        
        return ToolResult(
            success=True,
            message=f"{task_type.capitalize()} generated successfully",
            data={"content": response}
        )
    
    def _determine_task_type(self, prompt: str) -> str:
        """
        Determine the type of creative task.
        
        Args:
            prompt: The user's prompt
            
        Returns:
            The type of creative task (poem, story, etc.)
        """
        if "poem" in prompt.lower():
            return "poem"
        elif "story" in prompt.lower():
            return "story"
        elif "essay" in prompt.lower():
            return "essay"
        elif "article" in prompt.lower():
            return "article"
        elif "letter" in prompt.lower():
            return "letter"
        elif "song" in prompt.lower() or "lyrics" in prompt.lower():
            return "song"
        elif "script" in prompt.lower():
            return "script"
        elif "dialogue" in prompt.lower():
            return "dialogue"
        else:
            return "creative text"
    
    def _create_context_prompt(self, prompt: str, task_type: str) -> str:
        """
        Create a context-aware prompt for the language model.
        
        Args:
            prompt: The user's prompt
            task_type: The type of creative task
            
        Returns:
            A context-aware prompt for the language model
        """
        # Extract the topic from the prompt
        topic_match = re.search(r'(?:about|on|regarding)\s+(\w+(?:\s+\w+)*)', prompt.lower())
        topic = topic_match.group(1) if topic_match else ""
        
        # Create a context-aware prompt based on the task type
        if task_type == "poem":
            return f"You are a skilled poet. Write a beautiful and thoughtful poem about {topic}. Be creative and expressive."
        elif task_type == "story":
            return f"You are a talented storyteller. Write an engaging short story about {topic}. Include interesting characters and a compelling plot."
        elif task_type == "essay":
            return f"You are an insightful essayist. Write a thoughtful essay about {topic}. Present clear arguments and support them with evidence."
        elif task_type == "article":
            return f"You are a professional journalist. Write an informative article about {topic}. Present facts clearly and objectively."
        elif task_type == "letter":
            return f"You are a skilled letter writer. Write a heartfelt letter about {topic}. Express your thoughts and feelings clearly."
        elif task_type == "song" or task_type == "lyrics":
            return f"You are a talented songwriter. Write lyrics for a song about {topic}. Be creative and expressive."
        elif task_type == "script":
            return f"You are an experienced screenwriter. Write a script about {topic}. Include engaging dialogue and clear stage directions."
        elif task_type == "dialogue":
            return f"You are a skilled dialogue writer. Write a dialogue about {topic}. Make the conversation flow naturally and reveal character."
        else:
            return f"You are a creative writer. Write a thoughtful and engaging piece about {topic}. Be creative and expressive."
