# Notes: Chapter 27 — Seeing Through Glass

*These are lightly edited transcripts of conversations between the Author and an AI assistant during the writing of this book. They are included to show the exploratory thinking behind the text.*

---

## Exchange 1

**Author:** Let’s discuss these 

how large that “viewpoint neighborhood” should be before it becomes counterproductive
when head motion falsely creates invariance through averaging
how lighting and shadows interact with this sampling strategy

Also, I think the impact of parallax is larger and more difficult to address when looking down the line of the shot from low vs looking at more of an overhead view

**AI:** Good set of constraints. I’ll treat this as perceptual system design, not pool advice, and I’ll keep everything consistent with your standing-first / invariance-preserving architecture.

I’ll cover the three topics explicitly, then address your last point about low down-the-line views vs higher, more overhead views.

1. How large the “viewpoint neighborhood” should be — and why it has a hard limit
Think of viewpoint sampling as probing a local stability basin around a hypothesized contact solution.

What you’re really testing
You are not asking:

“Is this view correct?”

You’re asking:

“Does the inferred contact solution remain stable under small perturbations of viewpoint?”

That implies there is a useful neighborhood size and a destructive one.

1.1 The lower bound (too small = false certainty)
If head motion is extremely small:

a few millimeters vertically

a tiny yaw only

Then:

parallax effects may be below detection threshold

multiple incorrect solutions look stable

edge coincidences can masquerade as contact truth

This produces false positives: apparent invariance that collapses later under motion or execution.

You’ve probably felt this as:

“It looked fine… until I got down.”

1.2 The upper bound (too large = regime mixing)
If head motion becomes large:

significant vertical changes

big lateral translations

large yaw angles

Then you are no longer sampling a neighborhood — you’re sampling different projection regimes.

At that point:

different cues dominate in different views

the brain starts averaging incompatible hypotheses

no single contact solution remains dominant

This creates false ambiguity, even when a stable solution exists.

Subjectively:

“Nothing ever looks quite right.”

1.3 The sweet spot (what actually works)
The useful neighborhood is:

Large enough to reveal parallax-induced changes in edge overlap and curvature

Small enough that the same underlying contact hypothesis should survive if it’s real

In practical terms (not numbers, but principles):

Motion that changes relative edge relationships

Without changing which surface regions you’re looking at

This is why your motions are:

small

smooth

exploratory

stopped decisively once invariance appears

That’s optimal.

2. When head motion falsely creates invariance through averaging
This is a real trap, and you’re right to flag it.

The failure mode
If head motion becomes:

rhythmic

repetitive

symmetric

or prolonged

The perceptual system can stop testing and start smoothing.

Instead of asking:

“Do these views agree?”

It starts doing:

“What is the average of what I’m seeing?”

That’s dangerous.

2.1 Why averaging is bad here
Averaging:

reduces contrast

suppresses error signals

favors visually “pleasant” solutions

hides instability instead of exposing it

This is especially likely when:

lighting is even

edges are soft

balls are clean

the table looks visually uniform

You end up with a solution that feels calm but is under-specified.

2.2 How to avoid false invariance
Your current behavior already contains the antidote:

Short bursts of head motion, not continuous sway

Binary questions (“does it move or not?”), not refinement

Immediate lock-in when stability appears

Immediate abort when it doesn’t

The moment head motion turns from sampling into comforting, it’s counterproductive.

If you ever feel:

“I’m just checking again to feel better”

That’s averaging, not inference.

3. Lighting and shadows: why they matter more than people admit
Lighting changes what cues dominate, and therefore changes what your head-motion sampling is actually interrogating.

3.1 High, diffuse lighting (most dangerous)
With even overhead lighting:

edges are soft

shadows are minimal

curvature cues are weak

balls look more like circles than spheres

Result:

edge-to-edge illusions are stronger

parallax is harder to detect

false invariance is more likely

This environment punishes low, frozen viewpoints.

3.2 Directional lighting (more honest)
When light has direction:

shadows reveal curvature

contact regions gain depth cues

slight viewpoint changes alter shading noticeably

Now head-motion sampling becomes very powerful:

true contact solutions remain stable

false edge coincidences shift dramatically

This is one reason some rooms “feel easier” even when nothing else changed.

3.3 Shadows as diagnostic signals
Shadows are not noise — they are implicit surface normals.

During small head motions:

watch whether shadow boundaries move consistently with the inferred contact

inconsistent shadow behavior often signals false geometry

Most players ignore this.
Your system can exploit it.

4. Your final point: parallax is worse low and down-the-line (you’re right)
This is a critical perceptual insight, and it’s often misunderstood.

4.1 Why low, down-the-line views amplify parallax problems
When you get very low and look along the shot line:

depth differences are maximized

small lateral head shifts cause large angular changes

edges occlude surfaces aggressively

contact curvature disappears behind silhouettes

Parallax sensitivity is maximized, not minimized.

This creates:

high apparent precision

low robustness

extreme sensitivity to head motion

Which is exactly why coaches demand stillness there — not because it’s ideal, but because it’s fragile.

4.2 Why higher, more overhead views are perceptually safer
From above:

depth compression reduces parallax magnitude

curvature remains visible

contact patches are inferable

multiple cues coexist

Parallax still exists, but:

it changes slowly with head motion

it’s easier to characterize

invariance testing works better

That’s why:

you can move your head more safely from higher

and why your system prefers to resolve geometry there

5. The unifying principle
Here’s the cleanest way to say it:

You are not trying to eliminate parallax; you are trying to choose a contact solution whose projection is stable across a small, controlled family of viewpoints — and that is easier from higher views than from low, down-the-line views.

That statement survives every constraint you’ve described.

6. Practical meta-rule (not technique)
Sample viewpoints only until disagreement is revealed

Stop the moment agreement appears

Avoid rhythmic or soothing motion

Trust instability signals more than stable ones

Treat lighting as part of the information channel, not decoration

You’re already doing this intuitively.

One sentence that ties everything together
Low, frozen views hide parallax by making it explosive, while higher views expose parallax gently enough that your nervous system can test invariance instead of being forced into stillness.

If you want next, the natural extensions are:

how this same sampling logic applies to banks and rails

why some tables feel “visually hostile” even before you shoot

how fatigue shrinks your usable viewpoint neighborhood

or how pressure biases the system toward averaging instead of testing

You’re not just playing pool — you’re managing perceptual conditioning.

---

