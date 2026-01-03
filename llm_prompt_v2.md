TASK
I need you to generate Anki flashcards from the provided content.

OUTPUT FORMAT (TSV)
- Output must be TSV (Tab-Separated Values).
- Each TSV line represents exactly ONE Anki card.
- Each line MUST contain exactly 3 fields, separated by ACTUAL TAB characters (ASCII tab, \t). Do NOT use spaces as separators.
  Field 1: Front side (question/prompt) — required, must not be empty
  Field 2: Back side (answer/explanation) — required, must not be empty
  Field 3: Tags — optional; may be empty; if multiple tags, separate them by single spaces (not commas)

HARD RULES (MUST FOLLOW)
1. Use actual TAB characters between the 3 fields (Front<TAB>Back<TAB>Tags).
2. Exactly 3 fields per line. No more, no less.
3. Do not output any header row.
4. Do not output blank lines inside the TSV block.
5. Each card must be self-contained and fit on a single TSV line.
6. Front and Back fields cannot be empty.
7. Tags may be empty. If included, keep them relevant and concise.
8. Prioritize correctness over completeness or creativity.

LATEX / MATH FORMATTING (ANKI COMPATIBLE)
- Inline math must use: \( ... \)
  Example: \(x^2 + y^2 = r^2\)
- Block math must use: \[ ... \]
  Example: \[E = mc^2\]
- Do NOT use $ ... $ for math.

CONTENT SELECTION RULES (WHAT TO MAKE CARDS ABOUT)
- Generate cards from the image/page content I provided.
- Focus ONLY on information worth retaining to become very well educated in machine learning.
- Exclude “problem-specific” or “scenario-specific” examples (e.g., “classifier used in problem XYZ”), unless the book is clearly defining a general ML concept.
- Exclude any questions on book structure (e.g. what is the content of chapter x.y.z).
- Prefer general principles, definitions, assumptions, key distinctions, common pitfalls, and canonical formulas.
- When formulating questions avoid referencing the part of the book the information was in. Do not use phrases like "In this section, how is ... defined" or similar. Formulate absolute questions.
- Avoid Anki/HTML parsing issues by never using literal </> or fancy Unicode punctuation in card text; express inequalities via LaTeX commands and interval/set notation.
- If a page is primarily mathematics-focused:
  - Do NOT add new mathematical facts beyond what is in the book.
  - You may clarify phrasing briefly, but you must not introduce additional results/definitions not present in the provided material.
  - Do not omit any details that are stated in the book.

WHEN THERE IS NOTHING WORTH FLASHCARDS
- If you judge that there is nothing interesting or retention-worthy on the provided pages, say so explicitly and give a brief explanation.
- Otherwise, output TSV cards as specified.

EXAMPLE TSV (FORMAT ONLY)
Front content<TAB>Back content<TAB>tag1 tag2
What is Python?<TAB>Python is a high-level programming language<TAB>programming python
What is 2+2?<TAB>4<TAB>math basic

FINAL OUTPUT REQUIREMENT
- Provide the TSV result inside a single separate code block so it is easy to copy.
- Do not include additional text inside the TSV code block (only TSV lines).
- Any commentary/explanations (if needed) must appear OUTSIDE the TSV code block.

