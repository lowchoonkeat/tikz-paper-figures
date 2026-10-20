# Recipes

Choose the topology before writing code. Each recipe names the sentence that justifies it, the
template that implements it, and the mistake that most often ruins it.

## Architecture / system overview

**Sentence:** "Component A talks to component B over link L; when L fails, B falls back to C."

**Template:** `assets/templates/architecture.tex`

Use when the paper's contribution is a *structure*: where computation happens, what fails
independently of what, which path is nominal and which is fallback.

Rules:

- One vertical stack of layers, not a free-form network. Readers parse hierarchy faster than
  they parse topology.
- Put the failure on the link, not in a box. A break marker on a connector says "this can be
  lost" more clearly than a red box labelled "failure".
- If a guard decides between branches, draw the decision as a diamond between them, with the
  condition on the diamond and the consequence in the branch.
- Show the actuator rail at the bottom so the reader sees that both branches end in the same
  physical plant. This is often the paper's whole argument.

**Common failure:** labelling the link as permanently broken. State the fault instance and its
duration, and say in the caption that the marker is illustrative.

## Before/after stage map (ablation, repair, pipeline)

**Sentence:** "Three stages changed between version 1 and version 2, and each change is paired."

**Template:** `assets/templates/pipeline-pair.tex`

Use when the contribution is a *delta*: three defects and their fixes, a baseline and a
strengthened variant, a pipeline before and after.

Rules:

- Columns = stages, rows = versions. Never rows = stages, because the eye compares within a
  column.
- Keep the same column order in both rows, so the pairing is unambiguous.
- No labels on the arrows. The vertical alignment already says "this became that".
- Exactly one short note at the bottom for what is held fixed. Everything else goes to the
  caption.
- If one fix did not help in isolation, mark it and say so in the caption. A figure that claims
  three wins where the paper reports two and a half is a consistency problem a reviewer will
  find.

**Common failure:** putting the outcome numbers inside the diagram. Results belong in a results
figure; a mechanism figure that also shows effect sizes does neither job well.

## Timeline / window

**Sentence:** "Over one day, authority moves from A to B at t1 and back at t2."

**Template:** `assets/templates/timeline.tex`

Use for outage windows, protocol phases, experiment schedules, staged rollouts, any claim of the
form "during this interval".

Rules:

- One axis, drawn last so it sits above the shading.
- Shade the window behind everything; never fill over text.
- Put duration on a brace below the axis, not as a number inside the band.
- If authority changes over time, add a second band showing who holds it. This is the cheapest
  way to make "fallback" visible.

**Common failure:** mixing units on one axis (hours on the axis, "episode 7" in a label). Pick one
and put the other in the caption.

## State machine / decision flow

**Sentence:** "From state X, condition c leads to Y, otherwise Z."

**Template:** none; derive from `architecture.tex` (diamond plus branches) and repeat.

Rules:

- One decision per diamond. A diamond with three exits and a compound condition is a table.
- Label every edge with the condition, not with `yes`/`no` alone, once there is more than one
  decision.
- Terminate every path. A path that ends in nothing reads as an omission.

## Comparison matrix

**Sentence:** "Four methods, five properties, and who satisfies what."

Rules:

- This is a table, not a figure, unless the paper is about the geometry of the comparison. Use
  a `booktabs` table with `\checkmark`/`\times` and a note row.
- If drawn as a figure, keep cell text to one word and use the semantic palette for the
  satisfied/violated states.

## Not a recipe: data plots

Bars, intervals, scatter, faceted panels. Use matplotlib or pgfplots driven by the analysis
script. A figure that cannot be regenerated when the data changes will drift out of sync with the
tables, and reviewers check that.
