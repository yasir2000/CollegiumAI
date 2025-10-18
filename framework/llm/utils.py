"""
LLM Utilities
=============

Utility functions for working with LLM requests, responses, and conversations.
"""

import re
import tiktoken
from typing import List, Dict, Any, Optional, Union
from datetime import datetime

from .providers import LLMMessage, LLMRequest, ModelCapability

def create_system_message(content: str, metadata: Optional[Dict[str, Any]] = None) -> LLMMessage:
    """Create a system message"""
    return LLMMessage(
        role="system",
        content=content,
        metadata=metadata or {}
    )

def create_user_message(content: str, name: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> LLMMessage:
    """Create a user message"""
    return LLMMessage(
        role="user",
        content=content,
        name=name,
        metadata=metadata or {}
    )

def create_assistant_message(content: str, 
                           function_call: Optional[Dict[str, Any]] = None,
                           metadata: Optional[Dict[str, Any]] = None) -> LLMMessage:
    """Create an assistant message"""
    return LLMMessage(
        role="assistant",
        content=content,
        function_call=function_call,
        metadata=metadata or {}
    )

def create_function_message(name: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> LLMMessage:
    """Create a function result message"""
    return LLMMessage(
        role="function",
        content=content,
        name=name,
        metadata=metadata or {}
    )

def create_chat_request(messages: List[LLMMessage],
                       model: Optional[str] = None,
                       temperature: float = 0.7,
                       max_tokens: Optional[int] = None,
                       **kwargs) -> LLMRequest:
    """Create a standardized chat request"""
    return LLMRequest(
        messages=messages,
        model=model or "gpt-3.5-turbo",
        temperature=temperature,
        max_tokens=max_tokens,
        **kwargs
    )

def estimate_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """
    Estimate the number of tokens in a text string using tiktoken.
    Falls back to a simple character-based estimation if tiktoken fails.
    """
    try:
        # Map model names to tiktoken encodings
        encoding_map = {
            "gpt-4": "cl100k_base",
            "gpt-4-turbo": "cl100k_base", 
            "gpt-4-turbo-preview": "cl100k_base",
            "gpt-3.5-turbo": "cl100k_base",
            "text-davinci-003": "p50k_base",
            "text-davinci-002": "p50k_base",
            "code-davinci-002": "p50k_base"
        }
        
        encoding_name = encoding_map.get(model, "cl100k_base")
        encoding = tiktoken.get_encoding(encoding_name)
        
        return len(encoding.encode(text))
        
    except Exception:
        # Fallback to character-based estimation (roughly 4 chars per token)
        return len(text) // 4

def estimate_request_tokens(request: LLMRequest) -> int:
    """Estimate total tokens for a request"""
    total_tokens = 0
    
    for message in request.messages:
        # Base tokens for message structure
        total_tokens += 4  # Role, content wrapper, etc.
        
        # Content tokens
        total_tokens += estimate_tokens(message.content, request.model)
        
        # Name tokens if present
        if message.name:
            total_tokens += estimate_tokens(message.name, request.model)
    
    # Additional tokens for request overhead
    total_tokens += 2
    
    return total_tokens

def format_conversation(messages: List[LLMMessage], 
                       include_metadata: bool = False,
                       timestamp_format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format a conversation for display or logging"""
    formatted_lines = []
    
    for i, message in enumerate(messages):
        # Role indicator
        role_indicators = {
            "system": "🖥️ System",
            "user": "👤 User", 
            "assistant": "🤖 Assistant",
            "function": "⚙️ Function"
        }
        
        role_indicator = role_indicators.get(message.role, f"❓ {message.role.title()}")
        
        # Message header
        header = f"{role_indicator}"
        if message.name:
            header += f" ({message.name})"
        
        if include_metadata and message.metadata:
            timestamp = message.metadata.get("timestamp")
            if timestamp:
                if isinstance(timestamp, datetime):
                    time_str = timestamp.strftime(timestamp_format)
                else:
                    time_str = str(timestamp)
                header += f" [{time_str}]"
        
        formatted_lines.append(f"{header}:")
        
        # Message content
        content_lines = message.content.strip().split('\n')
        for line in content_lines:
            formatted_lines.append(f"  {line}")
        
        # Function call if present
        if message.function_call:
            formatted_lines.append(f"  📞 Function Call: {message.function_call.get('name', 'unknown')}")
            if message.function_call.get('arguments'):
                formatted_lines.append(f"     Arguments: {message.function_call['arguments']}")
        
        # Add separator between messages (except last)
        if i < len(messages) - 1:
            formatted_lines.append("")
    
    return '\n'.join(formatted_lines)

def truncate_conversation(messages: List[LLMMessage], 
                         max_tokens: int,
                         model: str = "gpt-3.5-turbo",
                         keep_system: bool = True) -> List[LLMMessage]:
    """
    Truncate conversation to fit within token limit while preserving important context
    """
    if not messages:
        return messages
    
    # Separate system messages from conversation
    system_messages = [msg for msg in messages if msg.role == "system"]
    conversation_messages = [msg for msg in messages if msg.role != "system"]
    
    # Calculate tokens for system messages
    system_tokens = sum(estimate_tokens(msg.content, model) + 4 for msg in system_messages)
    
    if keep_system and system_tokens >= max_tokens:
        # If system messages alone exceed limit, truncate them
        truncated_system = []
        tokens_used = 0
        
        for msg in system_messages:
            msg_tokens = estimate_tokens(msg.content, model) + 4
            if tokens_used + msg_tokens <= max_tokens:
                truncated_system.append(msg)
                tokens_used += msg_tokens
            else:
                break
        
        return truncated_system
    
    # Available tokens for conversation
    available_tokens = max_tokens - (system_tokens if keep_system else 0)
    
    # Keep most recent messages that fit in available tokens
    truncated_conversation = []
    tokens_used = 0
    
    # Process messages in reverse order (most recent first)
    for msg in reversed(conversation_messages):
        msg_tokens = estimate_tokens(msg.content, model) + 4
        if tokens_used + msg_tokens <= available_tokens:
            truncated_conversation.insert(0, msg)
            tokens_used += msg_tokens
        else:
            break
    
    # Combine system messages and truncated conversation
    if keep_system:
        return system_messages + truncated_conversation
    else:
        return truncated_conversation

def extract_code_blocks(text: str) -> List[Dict[str, str]]:
    """Extract code blocks from text with language detection"""
    code_blocks = []
    
    # Pattern for fenced code blocks
    pattern = r'```(\w+)?\n(.*?)\n```'
    matches = re.finditer(pattern, text, re.DOTALL)
    
    for match in matches:
        language = match.group(1) or "text"
        code = match.group(2).strip()
        
        code_blocks.append({
            "language": language,
            "code": code,
            "start": match.start(),
            "end": match.end()
        })
    
    return code_blocks

def clean_response_content(content: str) -> str:
    """Clean and normalize response content"""
    if not content:
        return ""
    
    # Remove excessive whitespace
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    # Trim leading/trailing whitespace
    content = content.strip()
    
    # Normalize quotes
    content = content.replace('"', '"').replace('"', '"')
    content = content.replace(''', "'").replace(''', "'")
    
    return content

def parse_function_call(content: str) -> Optional[Dict[str, Any]]:
    """Parse function call from response content"""
    # Look for JSON-like function calls
    patterns = [
        r'```json\s*(\{.*?\})\s*```',
        r'```\s*(\{.*?\})\s*```',
        r'(\{[^{}]*"name"[^{}]*"arguments"[^{}]*\})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            try:
                import json
                function_call = json.loads(match.group(1))
                if "name" in function_call and "arguments" in function_call:
                    return function_call
            except json.JSONDecodeError:
                continue
    
    return None

def calculate_cost_estimate(input_tokens: int, 
                          output_tokens: int,
                          model_pricing: Dict[str, float]) -> float:
    """Calculate cost estimate for token usage"""
    input_cost = (input_tokens / 1000) * model_pricing.get("input", 0)
    output_cost = (output_tokens / 1000) * model_pricing.get("output", 0)
    return input_cost + output_cost

def validate_message_sequence(messages: List[LLMMessage]) -> List[str]:
    """Validate message sequence and return any issues found"""
    issues = []
    
    if not messages:
        issues.append("Empty message list")
        return issues
    
    # Check for proper alternating pattern (after system messages)
    conversation_messages = [msg for msg in messages if msg.role != "system"]
    
    if not conversation_messages:
        issues.append("No conversation messages found")
        return issues
    
    # First conversation message should be from user
    if conversation_messages[0].role != "user":
        issues.append(f"First conversation message should be from user, got: {conversation_messages[0].role}")
    
    # Check for proper alternation
    for i in range(1, len(conversation_messages)):
        current_role = conversation_messages[i].role
        previous_role = conversation_messages[i-1].role
        
        if current_role == previous_role and current_role in ["user", "assistant"]:
            issues.append(f"Consecutive messages from same role at position {i}: {current_role}")
    
    # Check for empty content
    for i, msg in enumerate(messages):
        if not msg.content and not msg.function_call:
            issues.append(f"Empty message content at position {i}")
    
    return issues

def merge_conversations(conversations: List[List[LLMMessage]], 
                       separator: Optional[str] = None) -> List[LLMMessage]:
    """Merge multiple conversations into one"""
    if not conversations:
        return []
    
    if len(conversations) == 1:
        return conversations[0]
    
    merged = []
    
    for i, conversation in enumerate(conversations):
        if i > 0 and separator:
            # Add separator message
            merged.append(create_system_message(separator))
        
        merged.extend(conversation)
    
    return merged

# Fix the typo in create_chat_request function parameter
def create_chat_request(messages: List[LLMMessage],  # Fixed typo: LLLMessage -> LLMMessage
                       model: Optional[str] = None,
                       temperature: float = 0.7,
                       max_tokens: Optional[int] = None,
                       **kwargs) -> LLMRequest:
    """Create a standardized chat request"""
    return LLMRequest(
        messages=messages,
        model=model or "gpt-3.5-turbo",
        temperature=temperature,
        max_tokens=max_tokens,
        **kwargs
    )