from config import Config

def validate_prompt(prompt: str) -> tuple[bool, str]:
    """
    Validate user prompt
    Returns: (is_valid, error_message)
    """
    if not prompt or len(prompt.strip()) == 0:
        return False, "Prompt cannot be empty!"

    # Basic content filtering
    banned_words = ['explicit', 'nsfw', 'nude']  # Add more as needed
    if any(word in prompt.lower() for word in banned_words):
        return False, "Inappropriate content detected!"

    return True, ""
