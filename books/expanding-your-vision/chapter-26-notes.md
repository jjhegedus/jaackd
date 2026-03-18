# Notes: Chapter 26 — Friction

*These are lightly edited transcripts of conversations between the Author and an AI assistant during the writing of this book. They are included to show the exploratory thinking behind the text.*

---

## Exchange 1

**Author:** I mean physically it is starting to get sluggish. When I type I have to wait for the letters to appear

**AI:** Ah — got it. That’s not philosophical sluggishness, that’s your device/browser choking on the DOM size. Long, deeply nested conversations can absolutely do that, especially on iOS.

This is a real, known issue, and you’re doing nothing wrong.

What’s happening (plainly)
The page is holding a very large rendered conversation

Every keystroke triggers layout + reflow

Mobile Safari / iOS browsers are especially bad at this

The lag you’re seeing (letters appearing late) is the tell

So yes — it’s literally becoming hard to type.

The fastest fixes (ranked by effectiveness)
Best / Cleanest
Start a new chat tab and continue there
You don’t need to recap everything — just carry the lens.

You can open a new tab and paste something as small as:

Continue the pool / perception / peripheral vision discussion. Assume we agree mechanics are scaffolding, global perceptual coherence matters more than local precision, and we’re exploring how to train that.

That alone will restore instant typing.

Also effective
Refresh the page (sometimes helps, sometimes not)

Close other tabs

Switch browsers (Safari → Chrome or vice versa)

If you want to stay right here
We can:

do very short exchanges

avoid long responses

but honestly this only delays the inevitable

The UI will keep degrading as the conversation grows.

Important reassurance
You are not losing anything meaningful by moving to a new chat.

This conversation is not linear notes — it’s a way of thinking.
You’ll re-enter it in about two sentences.

In fact, you’ll probably notice the thinking feels cleaner once the friction is gone.

My strong recommendation
Open a new chat now while the page still responds.

When you do, start with something like:

Let’s continue the pool discussion about peripheral vision, line-of-action anchoring, and training under pressure. No recap needed.

I’ll meet you there with full continuity of approach, even if not every word.

And if you want, in the first reply of the new chat, I can:

restate the lens in 5 bullets

then immediately dive into a concrete next topic (training, pressure, breathing, etc.)

This is just a technical ceiling — not an intellectual one.

---

## Exchange 2

**Author:** Another thing that makes outside English worse is because the speed you would want to hit with is generally slower, which increases swerve and the direction of swerve actually makes the cut thinner. You have to see this curve at the right place in the travel of the cue ball and account for it in the selection of the contact point. Ugly, ugly, ugly.

**AI:** Yep. That’s a clean, first-principles argument, and it’s ugly for exactly the reason you said: you’re forced to solve a time-dependent geometry problem where the curve’s direction pushes you the wrong way.

Let me formalize it without folklore.

1) Why outside english tends to “want” slower speed
On many cut shots, outside english is chosen to do at least one of these:

Hold the cue ball line / check it up

Reduce natural running (avoid over-running position)

Manage throw in a specific direction (often at slower speeds it “grabs” more predictably for some players)

All of those goals implicitly bias toward lower speed because you’re trying to let friction do work.

And lower speed is exactly what you don’t want if you’re trying to minimize swerve uncertainty.

So the outside-english package often comes with an embedded speed regime that makes the overall prediction harder.

2) The geometry becomes time-dependent (the real poison)
Once speed is low enough that CB–cloth sliding persists longer:

Swerve becomes large enough to matter

And it evolves over time: 
y
(
t
)
y(t) is not a line, it’s a curve

Now your aim problem is no longer “pick a contact point.”

It becomes:

pick a contact point such that the cue ball’s centerline at the instant of impact intersects the object-ball contact point.

That means you have to “see” the curve at the right arc-length along the path, not at the start.

That’s exactly the “see this curve at the right place in travel” thing you said.

3) Why the swerve direction makes the cut thinner
Let’s state the mechanism cleanly:

With outside english, the lateral forces (tip-induced side spin + cloth friction) curve the CB’s path in a direction that often reduces the effective overlap at the moment of contact.

In other words:

you line up for a certain overlap assuming a near-line path,

but the CB arrives laterally shifted the “wrong” way,

so the contact becomes thinner than intended.

This is a sign-sensitive effect: if the swerve direction pushes the CB away from the OB’s “meat,” you get thin.

And thin cuts have no variance budget, so it’s catastrophic.

4) Why this is hard to account for (and why it feels gross)
Because you don’t get a perceptual channel for “future curvature.”

You can’t directly sense:

how much swerve will accrue before collision

where along the path the curvature is largest

how cloth condition changes it

You can only infer it from a model + prior experience.

So outside english at low speed forces you into:

an internal ballistic model (predictive)

with parameters that drift (cloth, humidity, chalk, ball cleanliness)

in a regime where small parameter error produces a large contact error

That is exactly the sort of thing your system dislikes: not because it’s “hard,” but because it is low-observability.

5) Why your “from above, close to the ball” approach helps — and still can’t save it fully
Your contact-patch aiming from above is the best you can do because it anchors:

intended CB spot → OB spot mapping

squirt as a deterministic offset

But with low-speed outside:

swerve is a path integral

not a one-time offset

So you’re trying to compensate for a curve using a contact-point selection that assumes a line.

You can do it, but it will always feel like you’re juggling an unmeasurable variable.

Hence: ugly.

6) The decision rule that falls out of first principles
Outside english is not “bad.”

It’s just in the class of shots where:

required speed is low

required side spin is nontrivial

CB–OB distance is long enough for swerve to develop

the sign of swerve pushes overlap in the wrong direction

That combination is what makes it feel like a lie.

When those conditions aren’t present (e.g., short CB–OB distance, firmer speed, small offset), outside becomes much more tame.

7) The key insight you already have

---

