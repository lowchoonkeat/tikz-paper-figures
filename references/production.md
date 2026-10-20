# Production and export

## Draw at final size

The single rule that prevents most export problems: **set the picture width to the width it will
occupy on the page.**

Line widths and font sizes are absolute. If a 20 cm figure is scaled to 14 cm, every 0.6 pt rule
becomes 0.42 pt and every `\scriptsize` becomes roughly 4.9 pt. Both fall below what survives
print. Scaling up is worse: the figure looks coarse and the type mismatches the body text.

Typical targets:

| Placement | Width |
|---|---|
| single column, two-column journal | 8.2–8.6 cm |
| full text width, A4 with 2.5 cm margins | 15.5–16.0 cm |
| A4 single-column journal | 14.0–15.0 cm |
| thesis, generous margins | 14.0–16.0 cm |

Verify with `pdfinfo`, never by eye.

## Export matrix

| Destination | Format | Notes |
|---|---|---|
| LaTeX submission | PDF | native vector, fonts embedded, no conversion step |
| Word submission | PNG at 600 dpi | PDF inserted as a picture loses text fidelity across machines |
| Publisher portal | TIFF or EPS at 300–600 dpi | convert from the 600 dpi PNG; keep the PDF as master |
| Preprint / web | PNG at 300 dpi | keeps file size sane |
| Slides | PDF | scales cleanly in Keynote, PowerPoint, Beamer |

Keep the `.tex` as the master. Every raster is a derived artefact and should be regenerable with
one command.

## dpi arithmetic

```
pixels = width_cm / 2.54 * dpi
```

A 14.84 cm figure at 600 dpi is 3506 px wide. At 300 dpi, 1753 px. A publisher asking for
"300 dpi at print size" means the former only if the print size is the full width; check the
requested physical width before rendering.

`pdftoppm -r 600` renders at 600 dpi relative to the PDF's own page size, which is why drawing at
final size makes this arithmetic work without rescaling.

## Fonts

- `lmodern` with `\usepackage[T1]{fontenc}` embeds Type 1 fonts, accepted by every publisher.
- If the manuscript body is Times, match it: `\usepackage{newtxtext,newtxmath}`. A figure whose
  type differs from the caption type is visible immediately.
- If the journal wants TrueType/Type 42 rather than Type 1, compile with `lualatex` instead of
  `pdflatex`; the TikZ source needs no change.
- Never outline the text. Converted-to-path figures cannot be copy-edited and some portals reject
  them.

## Minimum sizes at final print

| Element | Minimum | Practical |
|---|---|---|
| line width | 0.25 pt | 0.4 pt |
| text | 6 pt | 7–8 pt |
| arrowhead length | 1.2 mm | 2.0 mm |

The house style sits at 0.6 pt and `\scriptsize` (7 pt at a 10 pt base), which is the practical
floor for a full-width figure.

## Checklist before submitting

- [ ] canvas width equals the intended printed width, confirmed with `pdfinfo`
- [ ] no overfull boxes reported by `build_figure.py`
- [ ] PNG opened and inspected at 100 %
- [ ] greyscale conversion still readable
- [ ] fonts embedded (check `pdffonts fig.pdf` — no `Type 3`, no missing)
- [ ] caption states units, sample size, and what a marker does *not* mean
- [ ] figure number and every in-text reference to it agree after insertion
- [ ] the source `.tex` is in the repository alongside the output
