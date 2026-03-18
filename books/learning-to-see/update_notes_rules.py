"""
Reads a chapter file, calls the Claude API to suggest regex keyword rules
for notes classification, and updates process_notes.py after confirmation.

Usage:
    python update_notes_rules.py chapter-20
    python update_notes_rules.py 20
"""
import argparse
import ast
import os
import re
import sys

from dotenv import load_dotenv

load_dotenv()  # searches cwd and walks up to find .env


def load_chapter(key):
    fname = f"{key}.md"
    if not os.path.exists(fname):
        raise FileNotFoundError(f"{fname} not found")
    with open(fname, "r", encoding="utf-8") as f:
        return f.read()


def get_chapter_title(key):
    with open("process_notes.py", "r", encoding="utf-8") as f:
        src = f.read()
    m = re.search(rf'"{key}":\s*"([^"]+)"', src)
    return m.group(1) if m else key


def suggest_keywords(key, title, chapter_text):
    import anthropic
    client = anthropic.Anthropic()

    prompt = f"""You are helping build a keyword classification system for a book about billiards/pool called "Learning to See".

The system routes excerpts from ChatGPT writing sessions into per-chapter notes files using Python regex keyword matching.

Here is the chapter:

---
{chapter_text}
---

Generate a Python list of regex keyword strings that would identify conversation excerpts relevant to this chapter.

Requirements:
- 4 to 8 keywords or short phrases
- Use regex syntax where useful (e.g. "cue.ball" matches "cue ball" or "cue-ball", "aim.*line" matches "aiming line")
- Focus on specific concepts, terms, character names, or situations that are distinctive to this chapter
- Avoid generic words that would match many chapters
- Return ONLY a valid Python list literal, e.g.: ["term one", "another.term", "specific phrase"]
"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip()


def rules_exist(key):
    with open("process_notes.py", "r", encoding="utf-8") as f:
        return f'("{key}"' in f.read()


def remove_existing_rules(src, key):
    # Remove a block like:
    #     # Chapter N — Title\n    ("chapter-N", ..., [...]),\n
    return re.sub(
        rf"\n    # Chapter \d+[^\n]*\n    \(\"{re.escape(key)}\"[^\n]*\),\n",
        "\n",
        src,
    )


def apply_rules(key, title, keywords):
    with open("process_notes.py", "r", encoding="utf-8") as f:
        src = f.read()

    if rules_exist(key):
        answer = input(f"  Rules for {key} already exist. Overwrite? [y/N] ").strip().lower()
        if answer != "y":
            print("  Skipped.")
            return
        src = remove_existing_rules(src, key)

    chapter_num = key.split("-")[1]
    new_block = (
        f"\n    # Chapter {chapter_num} \u2014 {title}\n"
        f"    (\"{key}\", 3, {repr(keywords)}),\n"
        f"\n    # General\n"
    )
    marker = "\n    # General\n"
    if marker not in src:
        print("  WARNING: could not find # General in RULES — aborting")
        return

    src = src.replace(marker, new_block)
    with open("process_notes.py", "w", encoding="utf-8") as f:
        f.write(src)
    print("  Updated process_notes.py RULES.")


def main():
    parser = argparse.ArgumentParser(description="Generate notes classification rules from a chapter file.")
    parser.add_argument("chapter", help="Chapter key or number, e.g. 'chapter-20' or '20'")
    args = parser.parse_args()

    key = args.chapter if args.chapter.startswith("chapter-") else f"chapter-{args.chapter}"

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set. Add it to your .env file.")
        sys.exit(1)

    print(f"Reading {key}.md ...")
    chapter_text = load_chapter(key)

    title = get_chapter_title(key)
    print(f"Chapter: {title}")
    print("Calling Claude API ...")

    raw = suggest_keywords(key, title, chapter_text)
    print(f"\nSuggested keywords:\n  {raw}\n")

    try:
        keywords = ast.literal_eval(raw)
        if not isinstance(keywords, list):
            raise ValueError
    except (ValueError, SyntaxError):
        print("Could not parse response as a Python list.")
        manual = input("Enter keywords as a comma-separated list: ")
        keywords = [k.strip() for k in manual.split(",") if k.strip()]

    confirm = input("Apply these rules to process_notes.py? [Y/n] ").strip().lower()
    if confirm in ("", "y"):
        apply_rules(key, title, keywords)
        print("Done.")
    else:
        print("Aborted.")


if __name__ == "__main__":
    main()
