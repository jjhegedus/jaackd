"""
Usage:
    python create_chapter.py "The Title"

Creates the next chapter-N.md and updates process_book.py and process_notes.py.
Run update_notes_rules.py after writing the chapter to generate keyword rules.
"""
import argparse
import os


def next_chapter_number():
    n = 1
    while os.path.exists(f"chapter-{n}.md"):
        n += 1
    return n


def create_chapter_file(n, title):
    fname = f"chapter-{n}.md"
    if os.path.exists(fname):
        raise FileExistsError(f"{fname} already exists")
    with open(fname, "w", encoding="utf-8") as f:
        f.write(f"# Chapter {n} \u2014 {title}\n")
    print(f"  created {fname}")


def update_process_book(n):
    with open("process_book.py", "r", encoding="utf-8") as f:
        src = f.read()

    old = f'    "chapter-{n - 1}",'
    new = f'    "chapter-{n - 1}",\n    "chapter-{n}",'
    if old not in src:
        print(f"  WARNING: could not find {old!r} in process_book.py — skipping")
        return
    with open("process_book.py", "w", encoding="utf-8") as f:
        f.write(src.replace(old, new, 1))
    print("  updated process_book.py CHAPTER_ORDER")


def update_process_notes(n, title):
    with open("process_notes.py", "r", encoding="utf-8") as f:
        src = f.read()

    key = f"chapter-{n}"
    general_entry = '    "general":    "General Notes",'
    new_chapter_entry = f'    "{key}": "Chapter {n} \u2014 {title}",\n{general_entry}'
    if general_entry not in src:
        print("  WARNING: could not find general entry in CHAPTERS — skipping")
    else:
        src = src.replace(general_entry, new_chapter_entry)

    with open("process_notes.py", "w", encoding="utf-8") as f:
        f.write(src)
    print("  updated process_notes.py CHAPTERS")


def main():
    parser = argparse.ArgumentParser(description="Create the next chapter in sequence.")
    parser.add_argument("title", help="Chapter title, e.g. 'The Final Shot'")
    args = parser.parse_args()

    n = next_chapter_number()
    print(f"Creating chapter-{n}: {args.title}")
    create_chapter_file(n, args.title)
    update_process_book(n)
    update_process_notes(n, args.title)
    print(f"Done. Run 'python update_notes_rules.py {n}' after writing the chapter.")


if __name__ == "__main__":
    main()
