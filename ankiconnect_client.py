"""AnkiConnect API client for adding notes to Anki."""

import json
import logging
from typing import Dict, List, Optional, Any
import requests

from config import Config

logger = logging.getLogger(__name__)


class AnkiConnectError(Exception):
    """Raised when there's an error communicating with AnkiConnect."""
    pass


class AnkiConnectClient:
    """Client for interacting with AnkiConnect API."""
    
    def __init__(self, config: Config):
        """
        Initialize the AnkiConnect client.
        
        Args:
            config: Configuration object with AnkiConnect settings
        """
        self.config = config
        self.url = config.anki_connect_url
        self.version = 6  # AnkiConnect API version
    
    def _request(self, action: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Send a request to AnkiConnect API.
        
        Args:
            action: The action to perform
            params: Optional parameters for the action
            
        Returns:
            The response result from AnkiConnect
            
        Raises:
            AnkiConnectError: If the request fails or AnkiConnect returns an error
        """
        payload = {
            "action": action,
            "version": self.version
        }
        
        if params:
            payload["params"] = params
        
        try:
            response = requests.post(self.url, json=payload, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            
            # Check for AnkiConnect errors
            if len(result) != 2:
                raise AnkiConnectError(
                    f"Invalid response format from AnkiConnect: {result}"
                )
            
            if result.get("error") is not None:
                error_msg = result.get("error", "Unknown error")
                raise AnkiConnectError(f"AnkiConnect error: {error_msg}")
            
            return result.get("result")
        
        except requests.exceptions.ConnectionError:
            raise AnkiConnectError(
                f"Could not connect to AnkiConnect at {self.url}. "
                "Make sure Anki is running and AnkiConnect add-on is installed."
            )
        except requests.exceptions.Timeout:
            raise AnkiConnectError(
                f"Request to AnkiConnect timed out. "
                "Anki may be busy or unresponsive."
            )
        except requests.exceptions.RequestException as e:
            raise AnkiConnectError(f"HTTP error communicating with AnkiConnect: {e}")
        except json.JSONDecodeError as e:
            raise AnkiConnectError(f"Invalid JSON response from AnkiConnect: {e}")
    
    def check_connection(self) -> bool:
        """
        Check if AnkiConnect is available and responding.
        
        Returns:
            True if AnkiConnect is available, False otherwise
        """
        try:
            self._request("version")
            logger.info("Successfully connected to AnkiConnect")
            return True
        except AnkiConnectError as e:
            logger.error(f"Failed to connect to AnkiConnect: {e}")
            return False
    
    def add_note(
        self,
        front: str,
        back: str,
        tags: Optional[List[str]] = None,
        deck_name: Optional[str] = None
    ) -> Optional[int]:
        """
        Add a note to Anki.
        
        Args:
            front: Front side content
            back: Back side content
            tags: Optional list of tags
            deck_name: Optional deck name (uses config default if not provided)
            
        Returns:
            Note ID if successful, None if duplicate
            
        Raises:
            AnkiConnectError: If the request fails
        """
        if deck_name is None:
            deck_name = self.config.default_deck_name
        
        if tags is None:
            tags = []
        
        note = {
            "deckName": deck_name,
            "modelName": self.config.note_type,
            "fields": {
                self.config.front_field: front,
                self.config.back_field: back
            },
            "tags": tags
        }
        
        params = {"note": note}
        
        try:
            result = self._request("addNote", params)
            
            # AnkiConnect returns None for duplicates, or the note ID if successful
            if result is None:
                logger.debug(f"Duplicate card detected: Front='{front[:50]}...'")
                return None
            
            logger.debug(f"Successfully added card with ID {result}: Front='{front[:50]}...'")
            return result
        
        except AnkiConnectError:
            # Re-raise AnkiConnect errors
            print(f"\nError adding note '{note.get('fields', {}).get(self.config.front_field, '')}'")
            raise
        except Exception as e:
            raise AnkiConnectError(f"Unexpected error adding note: {e}")
    
    def add_notes_batch(
        self,
        cards: List[Dict[str, str]],
        deck_name: Optional[str] = None
    ) -> Dict[str, int]:
        """
        Add multiple notes to Anki in batch.
        
        Args:
            cards: List of card dictionaries with 'front', 'back', and 'tags' keys
            deck_name: Optional deck name (uses config default if not provided)
            
        Returns:
            Dictionary with counts: 'success', 'duplicates', 'errors'
        """
        if deck_name is None:
            deck_name = self.config.default_deck_name
        
        results = {
            'success': 0,
            'duplicates': 0,
            'errors': 0
        }
        
        for card in cards:
            try:
                note_id = self.add_note(
                    front=card['front'],
                    back=card['back'],
                    tags=card.get('tags', []),
                    deck_name=deck_name
                )
                
                if note_id is None:
                    results['duplicates'] += 1
                else:
                    results['success'] += 1
            
            except AnkiConnectError as e:
                logger.error(f"Error adding card: {e}")
                results['errors'] += 1
        
        return results

