# Style guide

The rules exist so that nine figures drawn over four months still look like one manuscript.
Every rule below is enforceable from `assets/tikz-house-style.tex`.

## 1. Colour is semantic

Pick a role, not a shade.

| Role | Colour | Use for |
|---|---|---|
| primary | blue `62,98,148` | the nominal system, the path under study, the baseline |
| secondary | green `78,112,86` | repaired, fallback, accepted, corrected |
| accent | amber `176,116,60` | alternative branch, learned component, the thing being varied |
| alert | red `168,60,50` | defect, fault, failure, break |
| neutral | grey `96,102,110` | infrastructure, rails, axes, background structure |

Consequences:

- A reader who learns "red = the broken thing" in Figure 1 reads Figure 6 correctly without a
  legend. Do not spend the same colour on a second meaning later in the paper.
- If a figure needs a sixth colour, the figure is carrying two ideas. Split it.
- Fill and border of the same role come from the same hue. Never a blue border on an amber fill.

## 2. Three type sizes, no more

| Level | Macro | Size | Content |
|---|---|---|---|
| category | `\figcat{}` | `\scriptsize` italic | what kind of thing this box is (`controller`, `fitted-Q target`) |
| claim | `\figclaim{}` | `\footnotesize` bold | the one thing the box asserts |
| detail | `\figdetail{}` | `\scriptsize` | at most two short lines of qualification |

A fourth size signals that the figure is trying to hold a paragraph. Move that content to the
caption.

## 3. Equal cells

Within a row, every box gets the same width and the same number of text lines. Unequal heights
read as an error, and the reader spends attention on the layout instead of the content.

- Fixed `text width` on every cell in a row.
- Fixed `minimum height`, and enough detail text that the tallest cell does not grow past it.
- If one cell has less to say, write a shorter but still true second line. Do not leave it blank.

## 4. Symmetry on a fixed axis

Centre the figure on one x value and place branches symmetrically about it. An arrow that leaves
a diamond at x=4.0 should land on a box centred at x=3.0 with the mirror box at x=9.6 for a
centre of 6.3.

Asymmetric margins read as a mistake even when they are deliberate.

## 5. Line widths

| Element | Width |
|---|---|
| box borders, thin connectors | 0.6 pt |
| flow arrows, emphasis | 0.7–0.9 pt |
| rails, buses, timeline axes | 1.4 pt |

Nothing below 0.4 pt at final printed size. At 300 dpi, 0.4 pt is under two pixels and disappears
in print. If the figure will be scaled down, thicken everything proportionally — see
`production.md`.

## 6. Figure text is not prose

A box holds a noun phrase. A caption holds the sentence.

| In the figure | In the caption |
|---|---|
| `heartbeat look-ahead` | "The controller could observe arrivals before their physical timestamp." |
| `fault F3, 18:30--20:30` | "The break symbol marks a fault instance, not a permanent link loss." |
| `6 of 50 shown` | "Six of the 50 load groups are drawn for legibility." |

Any time the figure needs a footnote, ask whether the footnote belongs in the caption. It usually
does — but a marker (`†`, `*`) inside the figure is worth keeping when it prevents a wrong
inference, because readers who skim skip captions.

## 7. Checks before delivery

1. **Grayscale.** Convert to greyscale. If two roles become the same grey, they need different
   fills or different border weights, not just different hues.
2. **Colour vision.** Deuteranopia merges the red and green roles. They are already distinguished
   by position (above/below, left/right) in every template, which is why the pair is safe.
3. **Thumbnail.** View at 25 % zoom. The topology should still be legible; if only the text
   disappears, the structure is sound.
4. **Print size.** View at 100 % at the intended printed width. Any text you have to lean in to
   read is too small.
