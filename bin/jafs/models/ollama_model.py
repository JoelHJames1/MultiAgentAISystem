"""
Ollama Model implementation for the ANUS framework.

Author   Joel Hernandez James
Current Date  3/12/2025
Class
"""

from typing import Dict, List, Any, Optional, Union, Callable
import json
import logging
import os
import requests

from anus.models.base.base_model import BaseModel

class OllamaModel(BaseModel):
    """
    Ollama language model implementation.
    
    Provides integration with Ollama's API for text generation and embeddings.
    """
    
    def __init__(
        self, 
        model_name: str = "qwq:32b", 
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
        base_url: str = "http://localhost:11434",
        **kwargs
    ):
        """
        Initialize an OllamaModel instance.
        
        Args:
            model_name: The name of the Ollama model to use.
            temperature: Controls randomness in outputs. Lower values are more deterministic.
            max_tokens: Maximum number of tokens to generate.
            base_url: Base URL for the Ollama API. Default is http://localhost:11434.
            **kwargs: Additional model-specific parameters.
        """
        super().__init__(model_name, temperature, max_tokens, **kwargs)
        
        self.base_url = base_url
        self.api_url = f"{self.base_url}/api"
        
        # Additional Ollama parameters
        self.top_p = kwargs.get("top_p", 1.0)
        self.top_k = kwargs.get("top_k", 40)
        self.repeat_penalty = kwargs.get("repeat_penalty", 1.1)
        
        # Check if the model is available
        self._check_model_availability()
    
    def _check_model_availability(self):
        """
        Check if the specified model is available in Ollama.
        """
        try:
            response = requests.get(f"{self.api_url}/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [model.get("name") for model in models]
                
                if self.model_name not in model_names:
                    logging.warning(f"Model '{self.model_name}' not found in Ollama. Available models: {model_names}")
            else:
                logging.warning(f"Failed to check Ollama models: {response.status_code} {response.text}")
        except Exception as e:
            logging.warning(f"Error checking Ollama model availability: {e}")
    
    def generate(
        self, 
        prompt: str, 
        system_message: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        Generate text based on a prompt using Ollama.
        
        Args:
            prompt: The text prompt for generation.
            system_message: Optional system message for the model.
            temperature: Controls randomness in outputs. Overrides instance value if provided.
            max_tokens: Maximum number of tokens to generate. Overrides instance value if provided.
            **kwargs: Additional Ollama-specific parameters.
            
        Returns:
            The generated text response.
        """
        # Set parameters
        temp = temperature if temperature is not None else self.temperature
        tokens = max_tokens if max_tokens is not None else self.max_tokens
        
        # Prepare the request payload
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "temperature": temp,
            "top_p": kwargs.get("top_p", self.top_p),
            "top_k": kwargs.get("top_k", self.top_k),
            "repeat_penalty": kwargs.get("repeat_penalty", self.repeat_penalty),
            "stream": False
        }
        
        # Add system message if provided
        if system_message:
            payload["system"] = system_message
        
        # Add max tokens if provided
        if tokens:
            payload["num_predict"] = tokens
        
        try:
            # Make the API call
            response = requests.post(f"{self.api_url}/generate", json=payload)
            
            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                error_msg = f"Ollama API error: {response.status_code} {response.text}"
                logging.error(error_msg)
                return f"Error: {error_msg}"
        
        except Exception as e:
            logging.error(f"Error generating with Ollama: {e}")
            return f"Error: {str(e)}"
    
    def generate_with_tools(
        self, 
        prompt: str, 
        tools: List[Dict[str, Any]],
        system_message: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate text with tool calling capabilities.
        
        Note: Ollama doesn't natively support tool calling like OpenAI.
        This implementation uses a workaround by including tool descriptions
        in the prompt and parsing the response for tool calls.
        
        Args:
            prompt: The text prompt for generation.
            tools: List of tool schemas available for use.
            system_message: Optional system message for the model.
            temperature: Controls randomness in outputs. Overrides instance value if provided.
            max_tokens: Maximum number of tokens to generate. Overrides instance value if provided.
            **kwargs: Additional Ollama-specific parameters.
            
        Returns:
            A dictionary with the response and any tool calls.
        """
        # Create a modified system message that includes tool instructions
        tools_description = "Available tools:\n"
        for tool in tools:
            tools_description += f"- {tool.get('name')}: {tool.get('description')}\n"
            if "parameters" in tool:
                tools_description += "  Parameters:\n"
                for param_name, param_info in tool.get("parameters", {}).get("properties", {}).items():
                    required = "required" if param_name in tool.get("parameters", {}).get("required", []) else "optional"
                    tools_description += f"    - {param_name} ({required}): {param_info.get('description', '')}\n"
        
        tools_instructions = """
To use a tool, respond with JSON in the following format:
```json
{
  "tool_calls": [
    {
      "name": "tool_name",
      "arguments": {
        "param1": "value1",
        "param2": "value2"
      }
    }
  ]
}
```
If you don't need to use a tool, respond normally.
"""
        
        # Combine system message with tools instructions
        combined_system = ""
        if system_message:
            combined_system = system_message + "\n\n"
        combined_system += tools_description + tools_instructions
        
        # Generate response
        response_text = self.generate(
            prompt=prompt,
            system_message=combined_system,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        
        # Try to extract tool calls from the response
        tool_calls = []
        content = response_text
        
        # Look for JSON blocks in the response
        json_blocks = []
        in_json_block = False
        json_content = ""
        
        for line in response_text.split("\n"):
            if line.strip() == "```json" or line.strip() == "```":
                if in_json_block:
                    in_json_block = False
                    json_blocks.append(json_content)
                    json_content = ""
                else:
                    in_json_block = True
            elif in_json_block:
                json_content += line + "\n"
        
        # Also try to parse the entire response as JSON
        if not json_blocks:
            try:
                json_data = json.loads(response_text)
                json_blocks.append(json.dumps(json_data))
            except:
                pass
        
        # Process each JSON block
        for json_block in json_blocks:
            try:
                data = json.loads(json_block)
                if "tool_calls" in data:
                    for tool_call in data["tool_calls"]:
                        normalized_tool_call = {
                            "id": f"call_{len(tool_calls)}",
                            "name": tool_call.get("name", ""),
                            "arguments": tool_call.get("arguments", {})
                        }
                        tool_calls.append(normalized_tool_call)
                    
                    # Remove the JSON block from the content
                    content = content.replace(f"```json\n{json_block}\n```", "")
                    content = content.replace(f"```\n{json_block}\n```", "")
            except:
                continue
        
        return {
            "content": content.strip(),
            "tool_calls": tool_calls
        }
    
    def extract_json(
        self, 
        prompt: str, 
        schema: Dict[str, Any],
        system_message: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Extract structured JSON data based on a prompt.
        
        Args:
            prompt: The text prompt for extraction.
            schema: JSON schema describing the expected structure.
            system_message: Optional system message for the model.
            temperature: Controls randomness in outputs. Overrides instance value if provided.
            max_tokens: Maximum number of tokens to generate. Overrides instance value if provided.
            **kwargs: Additional Ollama-specific parameters.
            
        Returns:
            The extracted JSON data.
        """
        # Set default system message if not provided
        if not system_message:
            system_message = "Extract the requested information and respond only with a valid JSON object according to the specified schema. Do not include any other text."
        
        # Add schema to the prompt
        schema_prompt = f"Schema: {json.dumps(schema)}\n\nPrompt: {prompt}\n\nRespond with a valid JSON object only."
        
        # Generate response
        response_text = self.generate(
            prompt=schema_prompt,
            system_message=system_message,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        
        # Try to extract JSON from the response
        try:
            # First, try to parse the entire response as JSON
            return json.loads(response_text)
        except json.JSONDecodeError:
            # If that fails, look for JSON blocks
            for line in response_text.split("\n"):
                if line.strip().startswith("{") and line.strip().endswith("}"):
                    try:
                        return json.loads(line.strip())
                    except:
                        continue
            
            # If still no valid JSON, look for code blocks
            json_blocks = []
            in_json_block = False
            json_content = ""
            
            for line in response_text.split("\n"):
                if line.strip() == "```json" or line.strip() == "```":
                    if in_json_block:
                        in_json_block = False
                        json_blocks.append(json_content)
                        json_content = ""
                    else:
                        in_json_block = True
                elif in_json_block:
                    json_content += line + "\n"
            
            for json_block in json_blocks:
                try:
                    return json.loads(json_block)
                except:
                    continue
            
            # If all else fails, return an error
            logging.error(f"Failed to parse JSON from response: {response_text}")
            return {"error": "Failed to parse JSON response"}
    
    def get_embedding(self, text: str, **kwargs) -> List[float]:
        """
        Generate an embedding vector for the given text.
        
        Args:
            text: The text to embed.
            **kwargs: Additional Ollama-specific parameters.
            
        Returns:
            The embedding vector as a list of floats.
        """
        try:
            # Prepare the request payload
            payload = {
                "model": self.model_name,
                "prompt": text,
            }
            
            # Make the API call
            response = requests.post(f"{self.api_url}/embeddings", json=payload)
            
            if response.status_code == 200:
                return response.json().get("embedding", [])
            else:
                logging.error(f"Ollama API error: {response.status_code} {response.text}")
                return []
        
        except Exception as e:
            logging.error(f"Error generating embedding with Ollama: {e}")
            return []
