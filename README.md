# Anki Card Importer

A Python program that parses a TSV (Tab-Separated Values) file containing Anki card descriptions and automatically inserts them into your Anki deck using AnkiConnect.

## Prerequisites

1. **Anki** must be installed and running on your system
2. **AnkiConnect** add-on must be installed in Anki:
   - Open Anki
   - Go to Tools → Add-ons → Get Add-ons
   - Enter code: `2055492159`
   - Restart Anki

## Installation

1. Clone or download this repository
2. Create and activate a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Input File Format

The program expects a TSV file with the following format:

```
Front side content	Back side content	tag1 tag2 tag3
Another question	Another answer	tag4
Question 3	Answer 3	
```

**Format specification:**
- Each line represents one card
- Fields are separated by tabs (not spaces)
- Three fields: `Front`, `Back`, `Tags` (optional)
- Tags are space-separated if multiple
- Empty tags field is allowed
- File should be UTF-8 encoded
- **LaTeX support**: Use `\( ... \)` for inline math and `\[ ... \]` for block math
  - Example: `What is \(E = mc^2\)?` or `\[x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}\]`

## Usage

Make sure your virtual environment is activated:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Basic usage:
```bash
python main.py cards.txt
```

Specify a custom deck name:
```bash
python main.py cards.txt --deck "My Custom Deck"
```

Dry-run mode (parse and validate without adding cards):
```bash
python main.py cards.txt --dry-run
```

## Command-Line Options

- `input_file`: Path to the TSV file containing card descriptions (required)
- `--deck`, `-d`: Deck name to add cards to (default: "Default")
- `--dry-run`: Parse and validate the file without adding cards to Anki

## Example

1. Generate a TSV file using an LLM with the prompt from `llm_prompt.md`
2. Save the output as `my_cards.txt`
3. Activate the virtual environment: `source venv/bin/activate`
4. Run: `python main.py my_cards.txt --deck "Language Learning"`
5. Check the summary output for success/failure counts

## LaTeX Support

The program fully supports LaTeX mathematical expressions in card content. Anki will render LaTeX when properly configured.

**LaTeX Syntax:**
- Inline math: `\(formula\)` - e.g., `The formula is \(E = mc^2\)`
- Block math: `\[formula\]` - e.g., `\[ \int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2} \]`

**Important:** Use `\( ... \)` and `\[ ... \]` syntax, not `$ ... $`, as the dollar sign syntax can conflict with regular text.

When generating cards with an LLM, refer to `llm_prompt.md` for detailed LaTeX formatting instructions.

## Error Handling

The program handles various error cases:
- AnkiConnect connection failures
- Invalid file format
- Missing required fields
- Duplicate cards (reported but not added)
- Network timeouts

## Files

- `main.py` - Main entry point and CLI interface
- `parser.py` - TSV file parsing logic
- `ankiconnect_client.py` - AnkiConnect API client
- `config.py` - Configuration management
- `llm_prompt.md` - Template prompt for LLM card generation
- `example_cards.txt` - Example input file

## Troubleshooting

**"Connection refused" error:**
- Make sure Anki is running
- Verify AnkiConnect add-on is installed and enabled
- Check that AnkiConnect is listening on port 8765

**"Deck not found" error:**
- The deck will be created automatically if it doesn't exist
- Ensure the deck name doesn't contain invalid characters

**"Invalid file format" error:**
- Verify the file uses tabs (not spaces) to separate fields
- Check that each line has at least 2 fields (Front and Back)
- Ensure the file is UTF-8 encoded

