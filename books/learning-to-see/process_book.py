import os

CHAPTER_ORDER = [
    "prologue",
    "chapter-1",
    "chapter-2",
    "chapter-3",
    "chapter-4",
    "chapter-5",
    "chapter-6",
    "chapter-7",
    "chapter-8",
    "chapter-9",
    "chapter-10",
    "chapter-11",
    "chapter-12",
    "chapter-13",
    "chapter-14",
    "chapter-15",
    "chapter-16",
    "chapter-17",
    "chapter-18",
    "chapter-19",
    "chapter-20",
    "chapter-21",
]

parts = []
for key in CHAPTER_ORDER:
    fname = f"{key}.md"
    if not os.path.exists(fname):
        print(f"WARNING: {fname} not found, skipping")
        continue
    with open(fname, "r", encoding="utf-8") as f:
        content = f.read().strip()
    parts.append(content)
    print(f"  read {fname}")

# Appendix: chapter notes
notes_parts = []
for key in CHAPTER_ORDER:
    fname = f"{key}-notes.md"
    if not os.path.exists(fname):
        continue
    with open(fname, "r", encoding="utf-8") as f:
        content = f.read().strip()
    notes_parts.append(content)
    print(f"  read {fname}")

if notes_parts:
    appendix = "# Appendix — Notes\n\n" + "\n\n".join(notes_parts)
    parts.append(appendix)
    print(f"  appended {len(notes_parts)} notes file(s)")

with open("Book.md", "w", encoding="utf-8") as f:
    f.write("\n\n".join(parts) + "\n")

print(f"\nWrote Book.md ({len(parts)} section(s))")
