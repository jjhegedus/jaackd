# Learning to See — Book Tools

A reference for the Python scripts used to manage chapters and notes for this book.

---

## create_chapter.py

Creates the next chapter file in sequence and registers it in `process_book.py` and `process_notes.py`.

**Usage:**
```
python create_chapter.py "The Title"
```

**Example:**
```
python create_chapter.py "The Final Shot"
```

Creates `chapter-20.md` with a heading, adds it to `CHAPTER_ORDER` in `process_book.py`, and adds it to `CHAPTERS` in `process_notes.py`. After writing the chapter, run `update_notes_rules.py` to generate keyword classification rules.

---

## update_notes_rules.py

Reads a chapter file, calls the Claude API to suggest regex keyword rules for notes classification, and updates `process_notes.py` after confirmation.

**Requires:** `ANTHROPIC_API_KEY` set in a `.env` file.

**Usage:**
```
python update_notes_rules.py <chapter>
```

**Examples:**
```
python update_notes_rules.py 20
python update_notes_rules.py chapter-20
```

Displays the suggested keywords and prompts for confirmation before writing to `process_notes.py`.

---

## process_notes.py

Parses a raw ChatGPT conversation export (`notes.md`) and sorts exchanges into per-chapter notes files based on keyword rules.

**Usage:**
```
python process_notes.py
```

Reads `notes.md` from the current directory and writes one `chapter-N-notes.md` file per chapter that matched any exchanges. Unmatched exchanges go to `general-notes.md`.

---

## process_book.py

Assembles all chapter files into a single `Book.md`, followed by an appendix containing all chapter notes files.

**Usage:**
```
python process_book.py
```

Reads `prologue.md` through `chapter-N.md` in order, then appends any existing `chapter-N-notes.md` files under `# Appendix — Notes`. Warns about any missing chapter files.

---

## Typical Workflow

```
# 1. Start a new chapter
python create_chapter.py "The Title"

# 2. Write the chapter in chapter-N.md

# 3. Generate keyword rules from the chapter content
python update_notes_rules.py N

# 4. Process your ChatGPT notes into per-chapter files
python process_notes.py

# 5. Assemble the full book
python process_book.py
```
