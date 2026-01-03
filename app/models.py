from pydantic import BaseModel, Field, field_validator
import re

class Score(BaseModel):
    username: str = Field(..., min_length=1, max_length=20)
    score: int = Field(..., ge=0, le=100)
    
    @field_validator('username')
    @classmethod
    def sanitize_username(cls, v: str) -> str:
        """
        Sanitize username to prevent XSS attacks.
        Only allows letters, numbers, spaces, hyphens, and underscores.
        """
        # Check for valid characters
        if not re.match(r'^[a-zA-Z0-9_\-\s]+$', v):
            raise ValueError('Username can only contain letters, numbers, spaces, hyphens (-), and underscores (_)')
        
        # Remove any HTML tags (defense in depth)
        v = re.sub(r'<[^>]*>', '', v)
        
        # Trim whitespace
        v = v.strip()
        
        if not v:
            raise ValueError('Username cannot be empty after sanitization')
        
        return v
