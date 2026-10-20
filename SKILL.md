---
name: tikz-paper-figures
description: Produce publication-quality TikZ schematic figures for papers and theses — system architecture, pipeline or repair maps, timelines, process and mechanism diagrams — under a fixed house style with a compile-inspect-iterate loop and journal-ready export. Use when a manuscript needs a schematic figure, when existing figures must be redrawn to a consistent style, or when a figure must be exported as vector PDF or 300/600 dpi raster for Word, LaTeX, or a publisher submission system.
agent_created: true
---

# TikZ Paper Figures

Build figures that survive peer review: aligned by construction, consistent across a whole
manuscript, drawn at final printed size, and verified by looking at the rendered output rather
than trusting the source code.

This skill is a production workflow, not an example library. For a catalogue of standalone TikZ
examples, see `references/exemplars.md`. The value here is the style contract, the failure
modes, and the export rules.

## Scope

Use for:

- architecture, deployment, or system-overview schematics
- before/after pipeline diagrams, defect-to-fix maps, ablation layouts
- timelines with shaded windows and brace annotations
- state machines, decision trees, mechanism or process diagrams
- redrawing an existing figure so it matches the rest of the manuscript

Do **not** use for data plots (bars, intervals, scatter, faceted panels). Those belong in
matplotlib or pgfplots, driven by the analysis script, because the figure must regenerate when
the data changes. Hand-positioned TikZ coordinates encode data into geometry and cannot be
re-run.

## Workflow

### 1. Fix the topology in words first

Write the figure as a sentence with explicit counts before touching code: "three columns, two
rows, each cell has a category line, a bold claim, and two detail lines; vertical arrows map row
one onto row two." Ambiguous requests ("draw the architecture") produce ambiguous geometry.
Confirm the node count, the grouping, and which pairs are linked.

### 2. Set the target width before drawing

Ask, or infer from the manuscript: single column (~8.4 cm), full text width (~14–16 cm), or
double-column span. Draw at that width. Never draw at 20 cm and scale down — scaling shrinks
line widths and font sizes proportionally and breaks the minimums in
`references/production.md`.

### 3. Copy the style and a template

```bash
cp assets/tikz-house-style.tex <project>/figures/
cp assets/templates/architecture.tex <project>/figures/fig_name.tex
```

The template expects `\input{tikz-house-style}` in the same directory. Keep both files together.

### 4. Build a skeleton that compiles

Emit boxes and arrows with placeholder labels first. Compile. Only then add text, colour rules,
annotations, and footnote lines. A skeleton that compiles localises every later error to the
increment that introduced it.

### 5. Compile, render, and actually look at the image

```bash
python scripts/build_figure.py figures/fig_name.tex --target-width 14.8
```

The script compiles, reports the true page size, flags overfull boxes, renders PNG at 300 and
600 dpi, and warns when the canvas is wider than the target. **Open the PNG and inspect it.**
Source code that compiles is not a figure that reads correctly. Check, in this order:

1. every label sits inside its box
2. no arrowhead lands on a T-junction with nothing to point at
3. no label overlaps an arrow that crosses its row
4. text is centred vertically in boxes of equal height
5. nothing is hyphenated mid-word

### 6. Iterate one change at a time

Change one thing, recompile, re-inspect. Batch edits make a regression impossible to attribute.

### 7. Export and caption

Produce the export set described in `references/production.md`, then write the caption. State in
the caption what the figure cannot say: units, sample size, what a symbol means, what the reader
must not infer. Move any sentence longer than a noun phrase out of the figure and into the
caption.

## House style

Defined in `assets/tikz-house-style.tex`; the rationale is in `references/style-guide.md`.

- **Palette is semantic, not decorative.** primary = nominal system, secondary = repaired or
  accepted state, accent = alternative branch, alert = defect or fault, neutral = infrastructure.
  The same meaning keeps the same colour across every figure in the manuscript.
- **Three-level type scale.** category (`\scriptsize\itshape`), claim (`\footnotesize\bfseries`),
  detail (`\scriptsize`). Never invent a fourth size.
- **Every box in a row has the same height and the same line count.** Pad the detail block with a
  short second line rather than letting one box grow.
- **0.6 pt structural lines, 0.7–0.9 pt for flow, 1.4 pt for rails.** Nothing thinner.
- **Centre the figure on a fixed x.** Asymmetric columns read as a mistake, not a decision.

## Failure modes

Read `references/pitfalls.md` before debugging. It documents the traps that cost the most time:

- nested brace groups containing `\\` make TikZ miscalculate node height, so text spills outside
  the border
- a long text node without `text width` silently expands the bounding box and shrinks every other
  element when the figure is scaled to fit
- default hyphenation splits words inside boxes
- arrowheads at merge junctions point at nothing

## Files

| Path | Purpose |
|---|---|
| `assets/tikz-house-style.tex` | palette, node styles, type-scale macros |
| `assets/templates/architecture.tex` | layered system schematic with a guard and two branches |
| `assets/templates/pipeline-pair.tex` | before/after stage map with defect and fix rows |
| `assets/templates/timeline.tex` | axis, shaded window, brace annotation |
| `references/style-guide.md` | why the rules exist; grayscale and colour-vision checks |
| `references/recipes.md` | which topology to use for which figure type |
| `references/pitfalls.md` | LaTeX and TikZ traps with fixes |
| `references/production.md` | export matrix, dpi arithmetic, line-width floor |
| `references/exemplars.md` | external example libraries and what to take from each |
| `scripts/build_figure.py` | compile, measure, render, check |
| `examples/` | two complete figures with source and output |

## Toolchain

Requires a TeX distribution with `pdflatex` and `pdfinfo`/`pdftoppm` (MiKTeX, TeX Live, or poppler
on macOS/Linux). Compile with `-interaction=nonstopmode` so a missing package fails instead of
waiting on a prompt.
