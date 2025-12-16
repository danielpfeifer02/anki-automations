"""Parser module for reading and parsing TSV files containing Anki card descriptions."""

import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class ParseError(Exception):
    """Raised when there's an error parsing the input file."""
    pass


def parse_tsv_file(file_path: str) -> List[Dict[str, str]]:
    """
    Parse a TSV file containing Anki card descriptions.
    
    Expected format:
    - Each line represents one card
    - Fields separated by tabs: Front, Back, Tags (optional)
    - Tags are space-separated if multiple
    - Empty lines are skipped
    - Empty tags field is allowed
    
    Args:
        file_path: Path to the TSV file to parse
        
    Returns:
        List of dictionaries, each containing:
        - 'front': Front side content
        - 'back': Back side content
        - 'tags': List of tags (may be empty)
        
    Raises:
        ParseError: If the file cannot be read or has invalid format
        FileNotFoundError: If the file doesn't exist
    """
    cards = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, start=1):
                # Strip whitespace and skip empty lines
                line = line.strip()
                if not line:
                    continue
                
                # Split by tab character
                parts = line.split('\t')
                
                # Validate minimum required fields (Front and Back)
                if len(parts) < 2:
                    logger.warning(
                        f"Line {line_num}: Expected at least 2 fields (Front, Back), "
                        f"found {len(parts)}. Skipping."
                    )
                    continue
                
                # Extract fields
                front = parts[0].strip()
                back = parts[1].strip()
                
                # Validate that front and back are not empty
                if not front or not back:
                    logger.warning(
                        f"Line {line_num}: Front or Back field is empty. Skipping."
                    )
                    continue
                
                # Extract tags (optional third field)
                tags_str = parts[2].strip() if len(parts) > 2 else ""
                tags = [tag.strip() for tag in tags_str.split() if tag.strip()]
                
                # Create card dictionary
                card = {
                    'front': front,
                    'back': back,
                    'tags': tags
                }
                
                cards.append(card)
                logger.debug(f"Parsed card {len(cards)}: Front='{front[:50]}...'")
    
    except FileNotFoundError:
        raise ParseError(f"File not found: {file_path}")
    except UnicodeDecodeError as e:
        raise ParseError(
            f"Encoding error in file {file_path}: {e}. "
            "Please ensure the file is UTF-8 encoded."
        )
    except Exception as e:
        raise ParseError(f"Error reading file {file_path}: {e}")
    
    if not cards:
        raise ParseError(f"No valid cards found in file {file_path}")
    
    logger.info(f"Successfully parsed {len(cards)} cards from {file_path}")
    return cards

