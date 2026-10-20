# Pitfalls

Every item here cost real time on a real figure. Read this before debugging.

## 1. Nested braces around `\\` break node height

**Symptom.** Text spills outside the node border. The rectangle stays at its `minimum height`
while the text keeps going.

**Cause.** A `\\` inside a nested group, as in:

```latex
\node[draw] { {A}\\[2pt] {B\\C} };     % the inner \\ is inside a group
```

TikZ measures the paragraph before the group is fully expanded, so the computed height excludes
the wrapped line.

**Fix.** Keep every `\\` at the top level of the node body, one group per line:

```latex
\node[draw] { {A}\\[2pt] {B}\\[2pt] {C} };
```

Or drop the manual breaks entirely and set `text width`, letting TikZ wrap.

## 2. A long node without `text width` explodes the bounding box

**Symptom.** The PDF is 25 cm wide. Every box looks small and the whole figure is letterboxed.
Nothing in the log warns you.

**Cause.** A node containing one long line has the width of that line. `standalone` sizes the page
to the picture, so one sentence sets the canvas.

**Fix.** Give every multi-word annotation a `text width`:

```latex
\node[align=center, text width=12.6cm] at (7.85,3.0) {...};
```

**Detect.** Never trust the viewer's zoom. Check the real size:

```bash
pdfinfo fig.pdf | grep "Page size"
python scripts/build_figure.py fig.tex --target-width 14.8   # flags this automatically
```

## 3. Hyphenation inside boxes

**Symptom.** `suc-cessors`, `be-fore`, `archi-tecture` split across lines inside a box.

**Fix.** Suppress dictionary hyphenation at the node:

```latex
execute at begin node={\hyphenpenalty=10000\relax}
```

This is already in the `box` and `stage` styles. Note it does **not** stop breaks at explicit
hyphens: `multi-pass, full-episode replay` can still overflow. If a line with a hyphen is too
wide, shorten the text or insert `\\` by hand.

## 4. Arrowheads at merge junctions

**Symptom.** Two arrows point down onto a horizontal line and stop, as if pointing at nothing.

**Fix.** Draw the merge as plain lines and put a single arrowhead on the exit:

```latex
\draw (a) -- (a |- merge);      % plain
\draw (b) -- (b |- merge);      % plain
\draw (left) -- (right);        % plain
\draw[flow] (centre |- merge) -- (below);   % one arrowhead, at the exit
```

## 5. A label colliding with an arrow that crosses its row

**Symptom.** The row title is struck through by a vertical arrow.

**Cause.** A label placed at a fixed `y` between two rows, where the connecting arrows also run.

**Fix.** Move the label out of the arrow band — into a left margin as a rotated tag, above the
first row, or into the bottom note. Rotated tags (`rotate=90`, short text) cost almost no width
and never collide.

## 6. `aspect` on a diamond changes its height, not its width

`minimum width=4.6cm, aspect=2.55` gives a diamond 4.6 cm wide and 4.6/2.55 = 1.80 cm tall. Place
connected arrows using the computed corners, not the nominal width.

## 7. MiKTeX stops for a package prompt

**Symptom.** Compilation hangs on a headless run.

**Fix.** Always `pdflatex -interaction=nonstopmode`. Add `-halt-on-error` when iterating so the
first error is the only error.

## 8. `standalone` border and `\includegraphics` trimming

Do not fight the class with `trim`/`clip` at inclusion time. Set the crop once:

```latex
\documentclass[border=6pt]{standalone}
```

and include the PDF unscaled at its natural size. Every downstream resize is a chance to break
line widths and font sizes.

## 9. Word does not accept PDF as a picture

Insert the 600 dpi PNG, not the PDF. Word's PDF handling goes through an object, not a picture,
and text rendering differs between machines. See `production.md`.

## 10. Editing the source while a stale PDF is open

Viewers cache the rendered page. If the preview looks unchanged after an edit, close and reopen
the file before concluding the change had no effect. Re-render the PNG instead; the script
overwrites it every run.
