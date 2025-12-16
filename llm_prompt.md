# LLM Prompt Template for Anki Card Generation

Use this prompt template when asking an LLM to generate Anki card descriptions in the required format.

## Prompt Template

```
I need you to generate Anki flashcard descriptions from the following content. 
Please format the output as a TSV (Tab-Separated Values) file where each line 
represents one card.

FORMAT REQUIREMENTS:
- Each line must contain exactly 3 fields separated by TAB characters (not spaces)
- Field 1: Front side of the card (the question or prompt)
- Field 2: Back side of the card (the answer or explanation)
- Field 3: Tags (optional, space-separated if multiple, can be empty)

IMPORTANT RULES:
1. Use actual TAB characters to separate fields, not spaces
2. Each line represents one complete card
3. Front and Back fields are required and cannot be empty
4. Tags are optional - include relevant tags when appropriate, or leave empty
5. Do not include a header row
6. Ensure the content is clear and suitable for spaced repetition learning
7. For LaTeX/mathematical expressions, use Anki's LaTeX syntax:
   - Inline math: \( ... \) (e.g., \(x^2 + y^2 = r^2\))
   - Block math: \[ ... \] (e.g., \[E = mc^2\])
   - Do NOT use $ ... $ as it may conflict with regular dollar signs

EXAMPLE FORMAT:
Front content	Back content	tag1 tag2
What is Python?	Python is a high-level programming language	programming python
What is 2+2?	4	math basic

Now, please generate data for Anki cards from the image data that I have also provided you. 
Please only focus on any information that I will need to retain if I want to become very well educated in the field of machine learning. Make sure to exclude any specific examples (e.g. what classifiers are used in problem xyz) since that is unlikely to be very useful to know as an ML researcher. Only consider actual ML specifics - not problem details. If you don't deem anything interesting on the provided pages feel free to tell me and provide an explanation. Otherwise create cards as described above as close as possible to the contents of the provided data.

Remember:
- Use TAB characters between fields
- Make cards clear and concise
- Include appropriate tags when relevant
- Each card should be on a single line
- Make sure to use a separate block in the output for the result to allow easy copying.
```

## Detailed Format Specification

### Field Structure

1. **Front Field** (Required)
   - The question, prompt, or cue that appears on the front of the card
   - Should be clear and specific
   - Can contain multiple sentences if needed

2. **Back Field** (Required)
   - The answer, explanation, or information that appears on the back
   - Should provide complete information to answer the front
   - Can include formatting hints (though actual HTML formatting will depend on Anki settings)

3. **Tags Field** (Optional)
   - Space-separated list of tags for categorization
   - Useful for organizing cards by topic, difficulty, source, etc.
   - Can be left empty if no tags are needed
   - Common tag examples: subject names, difficulty levels, source material

### Character Encoding

- Use UTF-8 encoding
- Supports international characters (accented letters, Chinese, Japanese, etc.)
- Special characters in content are fine, but avoid using tabs within fields

### Edge Cases

**Empty Lines:**
- Empty lines in the file will be skipped automatically
- Don't worry about extra blank lines

**Tabs in Content:**
- Avoid using tab characters within the Front or Back fields
- If tabs are necessary, the parser may split incorrectly

**Long Content:**
- Cards can contain multiple sentences or paragraphs
- There's no strict length limit, but keep cards focused for effective learning

**Special Characters:**
- Quotes, commas, and other punctuation are fine
- HTML tags may be preserved if Anki is configured to render HTML

**LaTeX/Math Expressions:**
- Anki supports LaTeX rendering for mathematical expressions
- Use `\( ... \)` for inline math: `The formula is \(E = mc^2\)`
- Use `\[ ... \]` for block/display math: `\[ \int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2} \]`
- Do NOT use `$ ... $` syntax as it can conflict with regular dollar signs
- LaTeX expressions will be rendered by Anki if LaTeX is properly configured

## Example Use Cases

### Language Learning
```
Front: Bonjour	Back: Hello (French greeting)	french greetings basic
Front: Comment allez-vous?	Back: How are you? (formal)	french greetings formal
```

### Programming
```
Front: What is a list comprehension in Python?	Back: A concise way to create lists using a single line of code, e.g., [x*2 for x in range(10)]	python syntax
Front: Explain the difference between == and === in JavaScript	Back: == performs type coercion, === checks both value and type without coercion	javascript operators
```

### Science
```
Front: What is photosynthesis?	Back: The process by which plants convert light energy into chemical energy, producing glucose and oxygen from carbon dioxide and water	biology plants
Front: What is the speed of light?	Back: Approximately 299,792,458 meters per second in a vacuum	physics constants
```

### Mathematics (with LaTeX)
```
Front: What is the quadratic formula?	Back: For \(ax^2 + bx + c = 0\), the solutions are: \[x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}\]	math algebra
Front: What is Euler's identity?	Back: \(e^{i\pi} + 1 = 0\)	math complex-numbers
Front: What is the derivative of \(x^2\)?	Back: \(2x\)	math calculus
```

## Tips for LLM Generation

1. **Clarity**: Make sure each card has a clear, unambiguous answer
2. **Brevity**: Keep cards focused - one concept per card is ideal
3. **Tags**: Use consistent tag naming (e.g., all lowercase, use hyphens for multi-word tags)
4. **Context**: Include enough context in the Back field to make the card useful
5. **Variety**: Generate cards at different difficulty levels if appropriate
6. **LaTeX**: When generating math or scientific content, always use Anki's LaTeX syntax:
   - Inline: `\(formula\)` 
   - Block: `\[formula\]`
   - Preserve LaTeX syntax exactly as it appears in the source material

## Validation Checklist

Before using the generated file, verify:
- [ ] Each line has exactly 3 fields (Front, Back, Tags)
- [ ] Fields are separated by tabs, not spaces
- [ ] Front and Back fields are not empty
- [ ] No header row is included
- [ ] File is saved as UTF-8
- [ ] Tags are space-separated (not comma-separated)
- [ ] LaTeX expressions use `\( ... \)` for inline and `\[ ... \]` for block math

## Testing the Output

After generating the file, you can test it using:
```bash
python main.py your_cards.txt --dry-run
```

This will validate the format without adding cards to Anki.

