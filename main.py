#!/usr/bin/env python3
"""Main entry point for Anki Card Importer."""

import argparse
import logging
import sys
from typing import Optional

from config import Config
from parser import parse_tsv_file, ParseError
from ankiconnect_client import AnkiConnectClient, AnkiConnectError


def setup_logging(verbose: bool = False) -> None:
    """Configure logging for the application."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def main() -> int:
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Import Anki cards from a TSV file using AnkiConnect',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py cards.txt
  python main.py cards.txt --deck "My Deck"
  python main.py cards.txt --dry-run
  python main.py cards.txt --deck "Language Learning" --verbose
        """
    )
    
    parser.add_argument(
        'input_file',
        help='Path to the TSV file containing card descriptions'
    )
    
    parser.add_argument(
        '--deck', '-d',
        dest='deck_name',
        default=None,
        help='Deck name to add cards to (default: "Default")'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Parse and validate the file without adding cards to Anki'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(verbose=args.verbose)
    logger = logging.getLogger(__name__)
    
    # Parse the input file
    try:
        logger.info(f"Parsing file: {args.input_file}")
        cards = parse_tsv_file(args.input_file)
        logger.info(f"Found {len(cards)} cards to process")
    except ParseError as e:
        logger.error(f"Parse error: {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error parsing file: {e}")
        return 1
    
    # If dry-run, just validate and exit
    if args.dry_run:
        logger.info("Dry-run mode: File parsed successfully, no cards will be added")
        print(f"\n✓ Successfully parsed {len(cards)} cards")
        print("✓ File format is valid")
        print("\nRun without --dry-run to add cards to Anki")
        return 0
    
    # Create configuration
    config = Config.from_args(deck_name=args.deck_name)
    logger.info(f"Using deck: {config.default_deck_name}")
    
    # Initialize AnkiConnect client
    client = AnkiConnectClient(config)
    
    # Check connection
    logger.info("Checking AnkiConnect connection...")
    if not client.check_connection():
        logger.error(
            "Cannot connect to AnkiConnect. "
            "Make sure Anki is running and AnkiConnect add-on is installed."
        )
        return 1
    
    # Add cards
    logger.info(f"Adding {len(cards)} cards to deck '{config.default_deck_name}'...")
    
    try:
        results = client.add_notes_batch(cards, deck_name=config.default_deck_name)
        
        # Print summary
        print("\n" + "=" * 60)
        print("Import Summary")
        print("=" * 60)
        print(f"Total cards processed: {len(cards)}")
        print(f"✓ Successfully added: {results['success']}")
        print(f"⚠ Duplicates skipped: {results['duplicates']}")
        print(f"✗ Errors: {results['errors']}")
        print("=" * 60)
        
        # Return appropriate exit code
        if results['errors'] > 0:
            return 1
        return 0
    
    except AnkiConnectError as e:
        logger.error(f"AnkiConnect error: {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())

