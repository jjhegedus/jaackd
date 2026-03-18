import re
import os

# Chapter metadata
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
    "chapter-20": "Chapter 20 — The Pause",
    "chapter-21": "Chapter 21 — Breath and Rhythm",
    "chapter-22": "Chapter 22 — The Straight Stroke",
    "chapter-23": "Chapter 23 — Acceleration and Deceleration",
    "chapter-24": "Chapter 24 — Spin and Impulse",
    "chapter-25": "Chapter 25 — Soft Shots and Slip",
    "chapter-26": "Chapter 26 — Friction",
    "chapter-27": "Chapter 27 — Seeing Through Glass",
    "general":    "General Notes",
}

# (chapter_key, weight, [regex_keywords])
RULES = [
    # Chapter 20 — The Pause
    ("chapter-20", 3, ["the pause", "pausing reopen", "pause effect", "lock-in", "lock in",
                        "no-pause", "no pause execution", "binary termination", "abandon shot",
                        "commit phase", "commit signal"]),
    ("chapter-20", 2, ["pre-shot routine", "pre shot routine", "shot routine",
                        "setup sequence", "sampling phase"]),

    # Chapter 21 — Breath and Rhythm
    ("chapter-21", 3, ["breath and rhythm", "centripetal stroke", "practice stroke",
                        "rhythm as invariant", "stroke shrinking", "stroke rhythm",
                        "timing protocol"]),
    ("chapter-21", 2, ["rhythm", "breath", "tempo", "timing"]),

    # Chapter 22 — The Straight Stroke
    ("chapter-22", 3, ["straight stroke", "inertial signal", "straight back.arm",
                        "degrees of freedom", "pendulum stroke", "fewer failure modes",
                        "angular acceleration"]),
    ("chapter-22", 2, ["straight", "pendulum", "shaft lean", "cue lean", "stroke shape"]),

    # Chapter 23 — Acceleration and Deceleration
    ("chapter-23", 3, ["acceleration and deceleration", "decelerat", "follow-through speed",
                        "fine motor control", "behavioral constraint"]),
    ("chapter-23", 2, ["acceleration", "follow.through", "speed control"]),

    # Chapter 24 — Spin and Impulse
    ("chapter-24", 3, ["spin and impulse", "sidespin", "topspin", "backspin",
                        "english", "cue tip contact"]),
    ("chapter-24", 2, ["spin", "impulse", "tip offset"]),

    # Chapter 25 — Soft Shots and Slip
    ("chapter-25", 3, ["slip stroke", "rigid coupling", "grip relaxation",
                        "finger extension", "soft shot", "lag shot", "stun shot"]),
    ("chapter-25", 2, ["slip", "grip.*relax", "relax.*grip"]),

    # Chapter 26 — Friction
    ("chapter-26", 3, ["friction", "cloth friction", "rolling resistance"]),
    ("chapter-26", 2, ["cloth", "felt"]),

    # Chapter 27 — Seeing Through Glass
    ("chapter-27", 3, ["seeing through glass", "diffuse light", "directional light",
                        "edge illusion", "shadow.*surface", "shadow.*normal"]),
    ("chapter-27", 2, ["lighting", "shadow"]),

    # Chapter 19 — Where the Eyes Go
    ("chapter-19", 3, ["where the eyes go", "wide.outcome", "widen.*acceptable",
                        "cue ball position distribution", "late visual correction"]),
    ("chapter-19", 2, ["gaze", "eyes go"]),

    # Chapter 9 — Seeing What Stays Put
    ("chapter-9",  3, ["seeing what stays put", "visual invariance", "parallax",
                        "viewpoint", "head motion.*sampling", "sampling protocol",
                        "viewpoint neighborhood", "overhead view", "down.the.line"]),
    ("chapter-9",  2, ["peripheral vision", "geometry inference", "decide with eyes",
                        "visual.*aiming"]),

    # Chapter 14 — Diagrams
    ("chapter-14", 3, ["overhead diagram", "shot diagram"]),
    ("chapter-14", 2, ["diagram"]),

    # Chapter 7 — What Counts as Practice
    ("chapter-7",  3, ["what counts as practice", "deliberate practice",
                        "counts as practice"]),
    ("chapter-7",  2, ["practice session", "drill"]),

    # Chapter 8 — The Qualifier
    ("chapter-8",  3, ["qualifier", "tournament.*qualify"]),

    # Early narrative chapters
    ("chapter-2",  3, ["marek"]),
    ("chapter-1",  3, ["university room"]),

    # General
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

# Assign to chapters
buckets = {}
for author_text, ai_text in exchanges:
    combined = author_text + " " + ai_text
    key = score_exchange(combined)
    buckets.setdefault(key, []).append((author_text, ai_text))

print("\nAssignment summary:")
for key in sorted(buckets.keys()):
    print(f"  {key}: {len(buckets[key])} exchange(s)")


def format_exchange(idx, author_text, ai_text):
    out = f"## Exchange {idx}\n\n"
    out += f"**Author:** {author_text}\n\n"
    out += f"**AI:** {ai_text}\n"
    return out


# Write chapter-x-notes.md files
written = []
for key, exlist in buckets.items():
    chapter_title = CHAPTERS.get(key, key)
    fname = f"{key}-notes.md"

    header = (
        f"# Notes: {chapter_title}\n\n"
        "*These are lightly edited transcripts of conversations between the Author and an AI "
        "assistant during the writing of this book. They are included to show the exploratory "
        "thinking behind the text.*\n\n"
        "---\n\n"
    )

    body = ""
    for idx, (a, ai) in enumerate(exlist, start=1):
        body += format_exchange(idx, a, ai) + "\n---\n\n"

    with open(fname, "w", encoding="utf-8") as f:
        f.write(header + body)
    written.append(fname)

print(f"\nWrote {len(written)} files:")
for w in sorted(written):
    print(f"  {w}")
