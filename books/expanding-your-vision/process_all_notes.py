"""
Produces processed_notes.md — all exchanges from notes.md in their original
chronological order, cleaned up and formatted, with a chapter label as a
footnote on each exchange.
"""
import re
import os

# Chapter metadata (same as process_notes.py)
CHAPTERS = {
    "prologue":   "Prologue — The Game He Didn't Get to Play",
    "chapter-1":  "Chapter 1 — The Room",
    "chapter-2":  "Chapter 2 — Marek",
    "chapter-3":  "Chapter 3 — Paul's First Tournament",
    "chapter-4":  "Chapter 4 — The Question That Followed Him Home",
    "chapter-5":  "Chapter 5 — The Table They Could Afford",
    "chapter-6":  "Chapter 6 — Making a Choice",
    "chapter-7":  "Chapter 7 — What Counts as Practice",
    "chapter-8":  "Chapter 8 — The Qualifier",
    "chapter-9":  "Chapter 9 — Seeing What Stays Put",
    "chapter-10": "Chapter 10 — After the Noise",
    "chapter-11": "Chapter 11 — Counting Backward",
    "chapter-12": "Chapter 12 — Still There",
    "chapter-13": "Chapter 13 — Being Seen",
    "chapter-14": "Chapter 14 — Diagrams",
    "chapter-15": "Chapter 15 — The Book",
    "chapter-16": "Chapter 16 — The Glass House Shatters",
    "chapter-17": "Chapter 17 — Blind",
    "chapter-18": "Chapter 18 — Other Rooms",
    "chapter-19": "Chapter 19 — Where the Eyes Go",
    "chapter-20": "Chapter 20 — Kevin",
    "chapter-21": "Chapter 21 — The Pinnacle",
    "chapter-22": "Chapter 22 — The Aftermath",
    "general":    "General Notes",
}

RULES = [
    ("chapter-19", 3, ["where the eyes go", "wide.outcome", "widen.*acceptable",
                        "cue ball position distribution", "late visual correction"]),
    ("chapter-19", 2, ["gaze", "eyes go"]),
    ("chapter-9",  3, ["seeing what stays put", "visual invariance", "parallax",
                        "viewpoint", "head motion.*sampling", "sampling protocol",
                        "viewpoint neighborhood", "overhead view", "down.the.line"]),
    ("chapter-9",  2, ["peripheral vision", "geometry inference", "decide with eyes",
                        "visual.*aiming"]),
    ("chapter-14", 3, ["overhead diagram", "shot diagram"]),
    ("chapter-14", 2, ["diagram"]),
    ("chapter-7",  3, ["what counts as practice", "deliberate practice",
                        "counts as practice"]),
    ("chapter-7",  2, ["practice session", "drill"]),
    ("chapter-8",  3, ["qualifier", "tournament.*qualify"]),
    ("chapter-2",  3, ["marek"]),
    ("chapter-1",  3, ["university room"]),
    ("chapter-20", 3, ['Kevin', 'bar.table', 'runout', 'put.*(away|them)', 'crush.*ego',
                        'Empire.Billiards', 'four.rails', 'gambling.*pool']),
    ("chapter-21", 3, ['Jerry|Kitty.?Cat.?Lounge', 'Mishawaka', 'break.*nothing|dead.?break',
                        'roll.*table|table.?roll', 'side.?bet', 'will.*faltered|moment.*will',
                        'hook.*shot|curve.*around', 'five.?hundred.*dollars|eighteen.?games']),
    ("chapter-22", 3, ['pool.hall', 'Paul|Kevin', 'corner.*chair', 'set.of.balls',
                        'table.*nearby', 'wired|tired.*excited', 'well.earned.rest',
                        'until.next.time']),
    ("general",    2, ["standardiz", "converge", "modern pool", "pro pool",
                        "shane van boening", "snooker", "note.taking",
                        "context seed", "fact seed", "lens seed",
                        "compressing conversation"]),
]


def score_exchange(text):
    text_lower = text.lower()
    scores = {}
    for chapter_key, weight, keywords in RULES:
        for kw in keywords:
            if re.search(kw, text_lower):
                scores[chapter_key] = scores.get(chapter_key, 0) + weight
    if not scores:
        return "general"
    return max(scores, key=lambda k: scores[k])


# Parse raw file
with open("notes.md", "r", encoding="utf-8") as f:
    raw = f.read()

raw = re.sub(r"^Skip to content\s*\nChat history\s*\n", "", raw, flags=re.MULTILINE)
raw = re.sub(r"^\s*https?://\S+\s*$", "", raw, flags=re.MULTILINE)
raw = re.sub(r"^\s*\d+\s*$", "", raw, flags=re.MULTILINE)
raw = re.sub(r"\n{3,}", "\n\n", raw)

parts = re.split(r"(You said:|ChatGPT said:)", raw)

exchanges = []
i = 1
while i < len(parts):
    tag = parts[i].strip()
    body = parts[i + 1] if i + 1 < len(parts) else ""
    if tag == "You said:":
        author_text = body.strip()
        ai_text = ""
        if i + 2 < len(parts) and parts[i + 2].strip() == "ChatGPT said:":
            ai_text = parts[i + 3].strip() if i + 3 < len(parts) else ""
            i += 4
        else:
            i += 2
        if author_text or ai_text:
            exchanges.append((author_text, ai_text))
    else:
        i += 2

print(f"Total exchanges parsed: {len(exchanges)}")

# Build output in original order
intro = ""
if os.path.exists("notes-intro.md"):
    with open("notes-intro.md", "r", encoding="utf-8") as f:
        intro = f.read().strip() + "\n\n---\n\n"
    print("  included notes-intro.md")

body = ""
for idx, (author_text, ai_text) in enumerate(exchanges, start=1):
    chapter_key = score_exchange(author_text + " " + ai_text)
    chapter_label = CHAPTERS.get(chapter_key, chapter_key)

    body += f"## Exchange {idx}\n\n"
    body += f"**Author:** {author_text}\n\n"
    body += f"**AI:** {ai_text}\n\n"
    body += f"*Related chapter: {chapter_label}*\n\n"
    body += "---\n\n"

with open("processed_notes.md", "w", encoding="utf-8") as f:
    f.write(intro + body)

print(f"Wrote processed_notes.md ({len(exchanges)} exchanges)")
