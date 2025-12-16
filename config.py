"""Configuration management for Anki Card Importer."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Configuration settings for the Anki Card Importer."""
    
    # AnkiConnect settings
    anki_connect_url: str = "http://localhost:8765"
    
    # Default deck settings
    default_deck_name: str = "A_A A Probabilistic Approach (ML - Murphy)"
    
    # Note type settings
    note_type: str = "Basic"
    
    # Field names for Basic note type
    front_field: str = "Front"
    back_field: str = "Back"
    
    @classmethod
    def from_args(cls, deck_name: Optional[str] = None) -> "Config":
        """
        Create a Config instance, optionally overriding the deck name.
        
        Args:
            deck_name: Optional deck name override. If None, uses default.
            
        Returns:
            Config instance with specified settings.
        """
        config = cls()
        if deck_name:
            config.default_deck_name = deck_name
        return config

